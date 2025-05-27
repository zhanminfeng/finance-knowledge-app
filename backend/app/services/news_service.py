from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from fastapi import HTTPException
from datetime import datetime

from app.models.news import NewsItem, NewsList
from app.core.logging import logger
from app.models.db.news import News
from app.services.xueqiu_client import xueqiu_client, XueqiuClient
from app.core.config import settings


class NewsService:
    """新闻服务"""
    
    async def get_all(self, db: AsyncSession, category: Optional[str] = None) -> NewsList:
        """获取所有新闻"""
        try:
            query = select(News)
            if category:
                # 查找分类（存储为JSON）中包含该分类的新闻
                query = query.filter(News.categories.contains(category))
            
            # 按发布日期降序排序
            query = query.order_by(desc(News.publish_date))
            
            result = await db.execute(query)
            items = result.scalars().all()
            
            # 转换为Pydantic模型
            pydantic_items = []
            for item in items:
                # 使用Property Getter获取列表
                tags = item.tags_list
                categories = item.categories_list
                
                pydantic_items.append(NewsItem(
                    id=item.id,
                    title=item.title,
                    content=item.content,
                    summary=item.summary,
                    source=item.source,
                    publishDate=item.publish_date.isoformat() if item.publish_date else None,
                    category=categories[0] if categories else None,
                    tags=tags,
                    imageUrl=item.image_url,
                    url=item.url,
                    is_xueqiu=XueqiuClient.is_xueqiu_news_id(item.id)
                ))
            
            return NewsList(items=pydantic_items, total=len(pydantic_items))
        except Exception as e:
            logger.error(f"获取新闻列表失败: {e}")
            raise HTTPException(status_code=500, detail=f"获取新闻列表失败: {str(e)}")
    
    async def get_by_id(self, news_id: str, db: AsyncSession) -> NewsItem:
        """根据ID获取新闻详情"""
        try:
            query = select(News).where(News.id == news_id)
            result = await db.execute(query)
            item = result.scalar_one_or_none()
            
            if not item:
                return None
            
            # 使用Property Getter获取列表
            tags = item.tags_list
            categories = item.categories_list
            
            # 如果是雪球新闻且尚未生成AI解释，可以在这里添加生成逻辑
            
            return NewsItem(
                id=item.id,
                title=item.title,
                content=item.content,
                summary=item.summary,
                source=item.source,
                publishDate=item.publish_date.isoformat() if item.publish_date else None,
                category=categories[0] if categories else None,
                tags=tags,
                imageUrl=item.image_url,
                url=item.url,
                is_xueqiu=XueqiuClient.is_xueqiu_news_id(item.id)
            )
        except Exception as e:
            logger.error(f"获取新闻ID={news_id}失败: {e}")
            raise HTTPException(status_code=500, detail=f"获取新闻详情失败: {str(e)}")
    
    async def search(self, keyword: str, db: AsyncSession) -> NewsList:
        """搜索新闻"""
        try:
            query = select(News).where(
                or_(
                    News.title.ilike(f"%{keyword}%"),
                    News.content.ilike(f"%{keyword}%"),
                    News.summary.ilike(f"%{keyword}%")
                )
            )
            
            # 按发布日期降序排序
            query = query.order_by(desc(News.publish_date))
            
            result = await db.execute(query)
            items = result.scalars().all()
            
            # 转换为Pydantic模型
            pydantic_items = []
            for item in items:
                # 使用Property Getter获取列表
                tags = item.tags_list
                categories = item.categories_list
                
                pydantic_items.append(NewsItem(
                    id=item.id,
                    title=item.title,
                    content=item.content,
                    summary=item.summary,
                    source=item.source,
                    publishDate=item.publish_date.isoformat() if item.publish_date else None,
                    category=categories[0] if categories else None,
                    tags=tags,
                    imageUrl=item.image_url,
                    url=item.url,
                    is_xueqiu=XueqiuClient.is_xueqiu_news_id(item.id)
                ))
            
            return NewsList(items=pydantic_items, total=len(pydantic_items))
        except Exception as e:
            logger.error(f"搜索新闻失败, 关键词={keyword}: {e}")
            raise HTTPException(status_code=500, detail=f"搜索新闻失败: {str(e)}")
    
    async def get_xueqiu_categories(self) -> List[str]:
        """获取可用的雪球新闻分类"""
        return ["全部", "股市", "美股", "宏观", "外汇", "商品", "基金", "私募", "房产"]
    
    async def fetch_latest_xueqiu(self, category: str = "全部", db: AsyncSession = None) -> int:
        """
        立即获取最新雪球新闻
        
        Args:
            category: 新闻分类
            db: 数据库会话，如果提供则使用已有会话
            
        Returns:
            获取到的新闻数量
        """
        if not settings.XUEQIU_API_ENABLED:
            return 0
            
        # 获取新闻
        try:
            news_items = await xueqiu_client.get_hot_news(category=category)
            logger.info(f"从雪球获取了 {len(news_items)} 条实时新闻")
            
            # 如果没有数据库会话，这里只是获取新闻但不保存
            if not db:
                return len(news_items)
                
            saved_count = 0
            for item in news_items:
                # 检查是否已存在
                query = select(News).where(News.id == item["id"])
                result = await db.execute(query)
                if result.scalar_one_or_none():
                    continue
                    
                # 创建新闻对象
                news = News(
                    id=item["id"],
                    title=item["title"],
                    summary=item["summary"],
                    content=item["content"],
                    source=item["source"],
                    url=item.get("url", ""),
                    publish_date=datetime.strptime(item["date"], "%Y-%m-%d") if "date" in item else datetime.now(),
                    image_url=item.get("imageUrl", "")
                )
                
                # 设置标签和分类
                news.categories_list = [item["category"]] if item.get("category") else []
                news.tags_list = item.get("tags", [])
                
                db.add(news)
                saved_count += 1
            
            if saved_count > 0:
                await db.commit()
                logger.info(f"成功保存了 {saved_count} 条新雪球新闻")
                
            return saved_count
        except Exception as e:
            logger.error(f"获取雪球新闻时出错: {str(e)}")
            if db:
                await db.rollback()
            return 0


# 创建服务实例
news_service = NewsService() 
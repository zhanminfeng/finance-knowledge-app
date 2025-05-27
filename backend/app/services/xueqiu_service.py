import asyncio
import json
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc

from app.core.config import settings
from app.core.database import get_async_db
from app.models.db.news import News
from app.services.xueqiu_client import xueqiu_client
from app.core.logging import logger


class XueqiuNewsService:
    """雪球新闻服务，负责定期获取雪球新闻并保存到数据库"""
    
    def __init__(self):
        """初始化雪球新闻服务"""
        self.is_running = False
        self.fetch_task = None
    
    async def start_fetch_task(self):
        """启动定期获取新闻的任务"""
        if not settings.XUEQIU_API_ENABLED:
            logger.info("雪球API未启用，不启动定期获取任务")
            return
            
        if self.is_running:
            logger.warning("雪球新闻获取任务已在运行")
            return
            
        self.is_running = True
        self.fetch_task = asyncio.create_task(self._periodic_fetch())
        logger.info(f"已启动雪球新闻定期获取任务，间隔: {settings.XUEQIU_FETCH_INTERVAL}秒")
    
    async def stop_fetch_task(self):
        """停止获取新闻的任务"""
        if not self.is_running or not self.fetch_task:
            return
            
        self.is_running = False
        self.fetch_task.cancel()
        try:
            await self.fetch_task
        except asyncio.CancelledError:
            pass
        logger.info("已停止雪球新闻定期获取任务")
    
    async def _periodic_fetch(self):
        """定期获取新闻的循环任务"""
        while self.is_running:
            try:
                await self.fetch_and_save_news()
            except Exception as e:
                logger.error(f"雪球新闻定期获取任务出错: {str(e)}")
                
            # 等待下一次执行
            await asyncio.sleep(settings.XUEQIU_FETCH_INTERVAL)
    
    async def fetch_and_save_news(self, categories=None):
        """
        获取并保存雪球新闻
        
        Args:
            categories: 要获取的新闻分类列表，None表示获取全部
            
        Returns:
            保存的新闻数量
        """
        if not settings.XUEQIU_API_ENABLED:
            logger.warning("雪球API未启用，跳过获取新闻")
            return 0
            
        if not categories:
            categories = ["全部"]
            
        # 获取数据库会话
        db_generator = get_async_db()
        db = await anext(db_generator)
        
        saved_count = 0
        try:
            # 获取每个分类的新闻并保存
            for category in categories:
                news_items = await xueqiu_client.get_hot_news(category=category)
                logger.info(f"从雪球获取了 {len(news_items)} 条[{category}]分类新闻")
                
                # 保存新闻到数据库
                for item in news_items:
                    # 检查是否已存在
                    existing = await self._check_news_exists(item["id"], db)
                    if existing:
                        continue
                        
                    # 创建新闻对象
                    news = News(
                        id=item["id"],
                        title=item["title"],
                        summary=item["summary"],
                        content=item["content"],
                        source=item["source"],
                        url=item.get("url", ""),
                        publish_date=datetime.strptime(item["date"], "%Y-%m-%d"),
                        image_url=item.get("imageUrl", "")
                    )
                    
                    # 设置标签和分类
                    news.categories_list = [item["category"]] if item.get("category") else []
                    news.tags_list = item.get("tags", [])
                    
                    db.add(news)
                    saved_count += 1
                
                # 提交事务
                if saved_count > 0:
                    await db.commit()
                    logger.info(f"成功保存了 {saved_count} 条新雪球新闻")
        except Exception as e:
            await db.rollback()
            logger.error(f"保存雪球新闻时出错: {str(e)}")
            raise
        finally:
            await db.close()
            
        return saved_count
    
    async def _check_news_exists(self, news_id: str, db: AsyncSession) -> bool:
        """
        检查新闻是否已存在
        
        Args:
            news_id: 新闻ID
            db: 数据库会话
            
        Returns:
            是否存在
        """
        query = select(News).where(News.id == news_id)
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None


# 创建单例
xueqiu_service = XueqiuNewsService() 
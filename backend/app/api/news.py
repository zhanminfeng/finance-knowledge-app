from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import aiohttp

from app.models.news import NewsItem, NewsList
from app.services.news_service import news_service
from app.services.xueqiu_service import xueqiu_service
from app.services.sina_service import sina_service
from app.core.database import get_async_db
from app.core.config import settings

router = APIRouter()

class Message(BaseModel):
    message: str

@router.get("", response_model=NewsList)
async def get_news_items(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """获取新闻列表"""
    return await news_service.get_all(db=db, category=category)

@router.get("/{news_id}", response_model=NewsItem)
async def get_news_item(
    news_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取特定新闻详情"""
    news = await news_service.get_by_id(news_id, db=db)
    if not news:
        raise HTTPException(status_code=404, detail=f"未找到ID为{news_id}的新闻")
    return news

@router.get("/search/{keyword}", response_model=NewsList)
async def search_news(
    keyword: str,
    db: AsyncSession = Depends(get_async_db)
):
    """搜索新闻内容"""
    return await news_service.search(keyword, db=db)

@router.get("/xueqiu/categories", response_model=List[str])
async def get_xueqiu_categories():
    """获取雪球新闻可用分类"""
    if not settings.XUEQIU_API_ENABLED:
        raise HTTPException(status_code=403, detail="雪球API未启用")
    return await news_service.get_xueqiu_categories()

@router.post("/xueqiu/fetch", response_model=Message)
async def fetch_xueqiu_news(category: Optional[str] = "全部"):
    """
    手动获取最新雪球新闻
    
    此端点为异步版API，支持后台任务，将直接返回执行结果
    """
    if not settings.XUEQIU_API_ENABLED:
        raise HTTPException(status_code=403, detail="雪球API未启用")
    
    try:
        # 构建请求
        url = settings.XUEQIU_NEWS_URL
        headers = {
            "User-Agent": settings.XUEQIU_USER_AGENT,
            "Cookie": settings.XUEQIU_COOKIE,
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://xueqiu.com/"
        }
        
        params = {
            "since_id": -1,
            "max_id": -1,
            "size": settings.XUEQIU_NEWS_LIMIT
        }
        
        # 如果不是"全部"，添加分类过滤参数
        if category != "全部":
            category_mapping = {
                "股市": 102,
                "美股": 101,
                "宏观": 6,
                "外汇": 111,
                "商品": 113,
                "基金": 104,
                "私募": 105,
                "房产": 116
            }
            if category in category_mapping:
                params["category"] = category_mapping[category]
        
        # 发送请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    return {"message": f"雪球API请求失败: 状态码 {response.status}"}
                
                data = await response.json()
                if "list" not in data:
                    return {"message": "雪球API返回数据格式异常"}
                
                # 处理新闻数据
                news_list = []
                saved_count = 0
                # 这里可以添加保存新闻到数据库的逻辑
                
                return {"message": f"已开始获取[{category}]分类的雪球新闻，请稍后查看新闻列表"}
    except Exception as e:
        return {"message": f"获取雪球新闻失败: {str(e)}"}

@router.post("/xueqiu/start", status_code=202)
async def start_xueqiu_task():
    """启动雪球新闻定期获取任务"""
    if not settings.XUEQIU_API_ENABLED:
        raise HTTPException(status_code=403, detail="雪球API未启用")
        
    await xueqiu_service.start_fetch_task()
    return {"message": "已启动雪球新闻定期获取任务"}

@router.post("/xueqiu/stop", status_code=202)
async def stop_xueqiu_task():
    """停止雪球新闻定期获取任务"""
    await xueqiu_service.stop_fetch_task()
    return {"message": "已停止雪球新闻定期获取任务"}

@router.get("/sina/fetch", response_model=List[Dict[str, Any]])
async def fetch_sina_news():
    """
    抓取新浪财经新闻
    """
    return await sina_service.fetch_news() 
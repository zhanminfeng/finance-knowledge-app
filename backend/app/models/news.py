from typing import List, Optional
from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime

from app.models.db.news import News as NewsModel

# Pydantic模型 - 用于API请求和响应
class NewsBase(PydanticBaseModel):
    """新闻基础模型"""
    title: str
    summary: str
    source: str
    publishDate: str  # 作为ISO格式字符串传输
    category: Optional[str] = None  # 主分类
    tags: Optional[List[str]] = None

class NewsCreate(NewsBase):
    """创建新闻请求模型"""
    content: str
    imageUrl: Optional[str] = None
    url: Optional[str] = None
    aiInterpretation: Optional[str] = None
    categories: Optional[List[str]] = None  # 所有分类

class NewsUpdate(PydanticBaseModel):
    """更新新闻请求模型"""
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    source: Optional[str] = None
    publishDate: Optional[str] = None
    category: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    imageUrl: Optional[str] = None
    url: Optional[str] = None
    aiInterpretation: Optional[str] = None

class NewsItem(NewsBase):
    """新闻响应模型"""
    id: str
    content: str
    imageUrl: Optional[str] = None
    url: Optional[str] = None
    aiInterpretation: Optional[str] = None
    is_xueqiu: Optional[bool] = False  # 是否来自雪球
    
    class Config:
        from_attributes = True

class NewsList(PydanticBaseModel):
    """新闻列表响应模型"""
    items: List[NewsItem]
    total: int 

class News(PydanticBaseModel):
    """新闻模型"""
    title: str
    summary: str
    content: str
    source: str
    url: Optional[str] = None
    publish_date: Optional[datetime] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime 
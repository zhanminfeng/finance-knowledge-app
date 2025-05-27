import json
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.models.base import BaseModel


class News(BaseModel):
    """新闻数据库模型"""
    __tablename__ = "news"
    __table_args__ = {'extend_existing': True}
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    publish_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    @property
    def tags_list(self) -> List[str]:
        """获取标签列表"""
        if not self.tags:
            return []
        return json.loads(self.tags) if isinstance(self.tags, str) else self.tags

    @tags_list.setter
    def tags_list(self, value: List[str]):
        """设置标签列表"""
        self.tags = json.dumps(value)

    @property
    def categories_list(self) -> List[str]:
        """获取分类列表"""
        if not self.category:
            return []
        return [self.category]

    @categories_list.setter
    def categories_list(self, value: List[str]):
        """设置分类列表"""
        self.category = value[0] if value else None

    @classmethod
    async def create_test_data(cls, db: AsyncSession) -> None:
        """插入测试数据"""
        test_news = [
            cls(
                id=str(uuid.uuid4()),
                title="测试新闻1",
                summary="这是一条测试新闻摘要",
                content="这是一条测试新闻内容",
                source="测试来源",
                url="http://example.com/test1",
                publish_date=datetime.now(),
                category="财经",
                image_url="http://example.com/test1.jpg",
                tags=json.dumps(["测试", "财经"]),
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            cls(
                id=str(uuid.uuid4()),
                title="测试新闻2",
                summary="这是另一条测试新闻摘要",
                content="这是另一条测试新闻内容",
                source="测试来源",
                url="http://example.com/test2",
                publish_date=datetime.now(),
                category="科技",
                image_url="http://example.com/test2.jpg",
                tags=json.dumps(["测试", "科技"]),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        for news in test_news:
            db.add(news)
        await db.commit() 
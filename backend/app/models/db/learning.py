import json
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
import uuid

from app.models.base import BaseModel


class Learning(BaseModel):
    """学习内容数据库模型"""
    __tablename__ = "learning"
    __table_args__ = {'extend_existing': True}
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    short_description: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_items: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    @property
    def tags_list(self) -> List[str]:
        """将标签从JSON字符串转换为列表"""
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except json.JSONDecodeError:
            return []
    
    @tags_list.setter
    def tags_list(self, value: List[str]) -> None:
        """将标签列表转换为JSON字符串"""
        if not value:
            self.tags = None
        else:
            self.tags = json.dumps(value)
    
    @property
    def related_items_list(self) -> List[str]:
        """将相关项目从JSON字符串转换为列表"""
        if not self.related_items:
            return []
        try:
            return json.loads(self.related_items)
        except json.JSONDecodeError:
            return []
    
    @related_items_list.setter
    def related_items_list(self, value: List[str]) -> None:
        """将相关项目列表转换为JSON字符串"""
        if not value:
            self.related_items = None
        else:
            self.related_items = json.dumps(value) 
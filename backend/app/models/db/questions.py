import json
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional

from app.models.base import BaseModel


class Question(BaseModel):
    """问题数据库模型"""
    __tablename__ = "questions"
    __table_args__ = {'extend_existing': True}
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    answer_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_questions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
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
    def related_questions_list(self) -> List[str]:
        """将相关问题从JSON字符串转换为列表"""
        if not self.related_questions:
            return []
        try:
            return json.loads(self.related_questions)
        except json.JSONDecodeError:
            return []
    
    @related_questions_list.setter
    def related_questions_list(self, value: List[str]) -> None:
        """将相关问题列表转换为JSON字符串"""
        if not value:
            self.related_questions = None
        else:
            self.related_questions = json.dumps(value) 
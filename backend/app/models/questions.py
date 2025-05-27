from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Table
from pydantic import BaseModel as PydanticBaseModel, Field
import json

from app.models.base import BaseModel

# 数据库模型
class Question(BaseModel):
    """问题数据库模型"""
    __tablename__ = "questions"
    __table_args__ = {'extend_existing': True}  # 解决重复表定义问题
    
    question = Column(String(500), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, index=True)
    categories = Column(Text, nullable=False, default='[]')  # 存储为JSON字符串
    tags = Column(Text, nullable=False, default='[]')  # 存储为JSON字符串
    related_questions = Column(Text, nullable=True)  # 存储为JSON字符串
    view_count = Column(Integer, nullable=False, default=0)  # 浏览次数
    
    @property
    def categories_list(self) -> List[str]:
        """获取分类列表"""
        if not self.categories:
            return []
        try:
            return json.loads(self.categories)
        except:
            return []
    
    @categories_list.setter
    def categories_list(self, value: List[str]):
        """设置分类列表"""
        self.categories = json.dumps(value)
    
    @property
    def tags_list(self) -> List[str]:
        """获取标签列表"""
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except:
            return []
    
    @tags_list.setter
    def tags_list(self, value: List[str]):
        """设置标签列表"""
        self.tags = json.dumps(value)
    
    @property
    def related_questions_list(self) -> List[str]:
        """获取相关问题列表"""
        if not self.related_questions:
            return []
        try:
            return json.loads(self.related_questions)
        except:
            return []
    
    @related_questions_list.setter
    def related_questions_list(self, value: List[str]):
        """设置相关问题列表"""
        self.related_questions = json.dumps(value)

# Pydantic模型 - 用于API请求和响应
class QuestionBase(PydanticBaseModel):
    """问题基础模型"""
    question: str
    answer: str
    difficulty: str
    categories: List[str]
    tags: List[str]

class QuestionCreate(QuestionBase):
    """创建问题请求模型"""
    relatedQuestions: Optional[List[str]] = None

class QuestionUpdate(PydanticBaseModel):
    """更新问题请求模型"""
    question: Optional[str] = None
    answer: Optional[str] = None
    difficulty: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    relatedQuestions: Optional[List[str]] = None

class QuestionItem(QuestionBase):
    """问题响应模型"""
    id: str
    viewCount: int
    relatedQuestions: Optional[List[str]] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    
    class Config:
        from_attributes = True

class QuestionList(PydanticBaseModel):
    """问题列表响应模型"""
    items: List[QuestionItem]
    total: int 
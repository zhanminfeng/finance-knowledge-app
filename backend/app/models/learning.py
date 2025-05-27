from typing import List, Optional
from sqlalchemy import Column, String, Text
from pydantic import BaseModel as PydanticBaseModel
import json

from app.models.base import BaseModel

# 数据库模型
class Learning(BaseModel):
    """学习内容数据库模型"""
    __tablename__ = "learning"
    __table_args__ = {'extend_existing': True}  # 解决重复表定义问题
    
    title = Column(String(255), nullable=False, index=True)
    short_description = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, index=True)
    tags = Column(Text, nullable=False, default='[]')  # 存储为JSON字符串
    related_items = Column(Text, nullable=True)  # 存储为JSON字符串
    
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
    def related_items_list(self) -> List[str]:
        """获取相关项目列表"""
        if not self.related_items:
            return []
        try:
            return json.loads(self.related_items)
        except:
            return []
    
    @related_items_list.setter
    def related_items_list(self, value: List[str]):
        """设置相关项目列表"""
        self.related_items = json.dumps(value)

# Pydantic模型 - 用于API请求和响应
class LearningBase(PydanticBaseModel):
    """学习内容基础模型"""
    title: str
    shortDescription: str
    difficulty: str
    tags: List[str]

class LearningCreate(LearningBase):
    """创建学习内容请求模型"""
    content: str
    relatedItems: Optional[List[str]] = None

class LearningUpdate(PydanticBaseModel):
    """更新学习内容请求模型"""
    title: Optional[str] = None
    shortDescription: Optional[str] = None
    content: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    relatedItems: Optional[List[str]] = None

class LearningItem(LearningBase):
    """学习内容响应模型"""
    id: str
    content: Optional[str] = None
    relatedItems: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class LearningList(PydanticBaseModel):
    """学习内容列表响应模型"""
    items: List[LearningItem]
    total: int 
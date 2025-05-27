from typing import List, Optional, Union
from pydantic import BaseModel
from enum import Enum

from .learning import LearningBase
from .news import NewsBase
from .questions import QuestionBase


class SearchCategory(str, Enum):
    """搜索类别枚举"""
    ALL = "all"
    LEARNING = "learning"
    NEWS = "news"
    QUESTIONS = "questions"


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str
    categories: Optional[List[SearchCategory]] = [SearchCategory.ALL]


class SearchResult(BaseModel):
    """搜索结果项模型"""
    id: str
    title: str
    snippet: str
    type: str  # 'learning', 'news', 或 'question'
    relevance: float = 0.0


class SearchResults(BaseModel):
    """搜索结果模型"""
    results: List[SearchResult]
    total: int 
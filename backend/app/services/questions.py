from typing import List, Optional
from app.models.questions import QuestionBase, QuestionItem, QuestionList
from app.services.data_service import DataService
from app.core.logging import logger


class QuestionsService:
    """问答服务，提供问答相关操作"""
    
    def __init__(self):
        """初始化问答服务"""
        self.data_service = DataService("questions_data.json", QuestionItem)
    
    def get_all_questions(self) -> QuestionList:
        """
        获取所有问题的简要信息
        
        Returns:
            问题列表
        """
        items = self.data_service.get_all()
        return QuestionList(items=items, total=len(items))
    
    def get_question(self, question_id: str) -> Optional[QuestionItem]:
        """
        根据ID获取问题详情
        
        Args:
            question_id: 问题ID
            
        Returns:
            问题详情
        """
        return self.data_service.get_by_id(question_id)
    
    def filter_by_category(self, category: str) -> QuestionList:
        """
        按分类筛选问题
        
        Args:
            category: 问题分类
            
        Returns:
            符合条件的问题列表
        """
        items = self.data_service.get_all()
        
        if category == "all":
            filtered_items = items
        else:
            filtered_items = [item for item in items if item.category == category]
        
        return QuestionList(items=filtered_items, total=len(filtered_items))
    
    def search_questions(self, keyword: str) -> QuestionList:
        """
        搜索问题
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            搜索结果列表
        """
        items = self.data_service.search(keyword)
        return QuestionList(items=items, total=len(items))


# 创建单例
questions_service = QuestionsService() 
from typing import List, Optional
from app.models.learning import LearningBase, LearningItem, LearningList
from app.services.data_service import DataService
from app.core.logging import logger


class LearningService:
    """学习内容服务，提供学习内容相关操作"""
    
    def __init__(self):
        """初始化学习内容服务"""
        self.data_service = DataService("learning_data.json", LearningItem)
    
    def get_all_learning_items(self) -> LearningList:
        """
        获取所有学习内容的简要信息
        
        Returns:
            学习内容列表
        """
        items = self.data_service.get_all()
        return LearningList(items=items, total=len(items))
    
    def get_learning_item(self, item_id: str) -> Optional[LearningItem]:
        """
        根据ID获取学习内容详情
        
        Args:
            item_id: 学习内容ID
            
        Returns:
            学习内容详情
        """
        return self.data_service.get_by_id(item_id)
    
    def filter_by_difficulty(self, difficulty: str) -> LearningList:
        """
        按难度筛选学习内容
        
        Args:
            difficulty: 难度级别 ('beginner', 'intermediate', 'advanced', 'all')
            
        Returns:
            符合条件的学习内容列表
        """
        items = self.data_service.get_all()
        if difficulty == "all":
            filtered_items = items
        else:
            filtered_items = [item for item in items if item.difficulty == difficulty]
        
        return LearningList(items=filtered_items, total=len(filtered_items))
    
    def search_learning_items(self, keyword: str) -> LearningList:
        """
        搜索学习内容
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            搜索结果列表
        """
        items = self.data_service.search(keyword)
        return LearningList(items=items, total=len(items))


# 创建单例
learning_service = LearningService() 
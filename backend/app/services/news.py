from typing import List, Optional
from app.models.news import NewsBase, NewsItem, NewsList
from app.services.data_service import DataService
from app.core.logging import logger


class NewsService:
    """新闻服务，提供新闻相关操作"""
    
    def __init__(self):
        """初始化新闻服务"""
        self.data_service = DataService("news_data.json", NewsItem)
    
    def get_all_news(self) -> NewsList:
        """
        获取所有新闻的简要信息
        
        Returns:
            新闻列表
        """
        items = self.data_service.get_all()
        # 按日期倒序排序
        sorted_items = sorted(items, key=lambda x: x.date, reverse=True)
        return NewsList(items=sorted_items, total=len(sorted_items))
    
    def get_news_item(self, news_id: str) -> Optional[NewsItem]:
        """
        根据ID获取新闻详情
        
        Args:
            news_id: 新闻ID
            
        Returns:
            新闻详情
        """
        return self.data_service.get_by_id(news_id)
    
    def filter_by_category(self, category: str) -> NewsList:
        """
        按分类筛选新闻
        
        Args:
            category: 新闻分类
            
        Returns:
            符合条件的新闻列表
        """
        items = self.data_service.get_all()
        
        if category == "all":
            filtered_items = items
        else:
            filtered_items = [item for item in items if item.category == category]
        
        # 按日期倒序排序
        sorted_items = sorted(filtered_items, key=lambda x: x.date, reverse=True)
        return NewsList(items=sorted_items, total=len(sorted_items))
    
    def search_news(self, keyword: str) -> NewsList:
        """
        搜索新闻
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            搜索结果列表
        """
        items = self.data_service.search(keyword)
        # 按日期倒序排序
        sorted_items = sorted(items, key=lambda x: x.date, reverse=True)
        return NewsList(items=sorted_items, total=len(sorted_items))


# 创建单例
news_service = NewsService() 
from typing import List
from app.models.search import SearchCategory, SearchRequest, SearchResultItem, SearchResults
from app.services.learning import learning_service
from app.services.news import news_service
from app.services.questions import questions_service
from app.core.logging import logger


class SearchService:
    """搜索服务，提供跨模块搜索功能"""
    
    def search(self, request: SearchRequest) -> SearchResults:
        """
        执行跨模块搜索
        
        Args:
            request: 搜索请求
            
        Returns:
            搜索结果
        """
        results = []
        
        # 判断是否搜索所有类别
        search_all = SearchCategory.ALL in request.categories or not request.categories
        
        # 搜索学习内容
        if search_all or SearchCategory.LEARNING in request.categories:
            learning_results = learning_service.search_learning_items(request.query).items
            for item in learning_results:
                results.append(SearchResultItem(type="learning", item=item))
        
        # 搜索新闻
        if search_all or SearchCategory.NEWS in request.categories:
            news_results = news_service.search_news(request.query).items
            for item in news_results:
                results.append(SearchResultItem(type="news", item=item))
        
        # 搜索问题
        if search_all or SearchCategory.QUESTIONS in request.categories:
            question_results = questions_service.search_questions(request.query).items
            for item in question_results:
                results.append(SearchResultItem(type="question", item=item))
        
        return SearchResults(results=results, total=len(results))


# 创建单例
search_service = SearchService() 
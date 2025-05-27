from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.search import SearchRequest, SearchResults, SearchResult
from app.models.db.learning import Learning
from app.models.db.news import News
from app.models.db.questions import Question
from app.core.logging import logger


class SearchService:
    """搜索服务，提供全局搜索功能"""
    
    async def search(self, request: SearchRequest, db: AsyncSession) -> SearchResults:
        """全局搜索"""
        try:
            keyword = request.query.strip()
            categories = request.categories or []
            
            # 如果关键词为空，返回错误
            if not keyword:
                raise HTTPException(status_code=400, detail="搜索关键词不能为空")
            
            results = []
            total_count = 0
            
            # 根据分类条件搜索不同类型的内容
            if not categories or "learning" in categories:
                learning_results = await self._search_learning(keyword, db)
                results.extend(learning_results)
                
            if not categories or "news" in categories:
                news_results = await self._search_news(keyword, db)
                results.extend(news_results)
                
            if not categories or "question" in categories:
                question_results = await self._search_questions(keyword, db)
                results.extend(question_results)
            
            total_count = len(results)
            
            # 按相关性排序（这里简单实现，实际可能需要更复杂的相关性计算）
            results.sort(key=lambda x: x.relevance, reverse=True)
            
            return SearchResults(results=results, total=total_count)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")
    
    async def _search_learning(self, keyword: str, db: AsyncSession) -> List[SearchResult]:
        """搜索学习内容"""
        query = select(Learning).where(
            or_(
                Learning.title.ilike(f"%{keyword}%"),
                Learning.short_description.ilike(f"%{keyword}%"),
                Learning.content.ilike(f"%{keyword}%")
            )
        )
        
        result = await db.execute(query)
        items = result.scalars().all()
        
        search_results = []
        for item in items:
            # 计算相关性分数（简单实现）
            relevance = self._calculate_relevance(keyword, item.title, item.content)
            
            # 生成摘要
            snippet = self._generate_snippet(keyword, item.content)
            
            search_results.append(SearchResult(
                id=item.id,
                title=item.title,
                snippet=snippet,
                type="learning",
                relevance=relevance
            ))
        
        return search_results
    
    async def _search_news(self, keyword: str, db: AsyncSession) -> List[SearchResult]:
        """搜索新闻"""
        query = select(News).where(
            or_(
                News.title.ilike(f"%{keyword}%"),
                News.content.ilike(f"%{keyword}%"),
                News.summary.ilike(f"%{keyword}%")
            )
        )
        
        result = await db.execute(query)
        items = result.scalars().all()
        
        search_results = []
        for item in items:
            # 计算相关性分数
            relevance = self._calculate_relevance(keyword, item.title, item.content)
            
            # 生成摘要，优先使用已有摘要
            snippet = item.summary if item.summary else self._generate_snippet(keyword, item.content)
            
            search_results.append(SearchResult(
                id=item.id,
                title=item.title,
                snippet=snippet,
                type="news",
                relevance=relevance
            ))
        
        return search_results
    
    async def _search_questions(self, keyword: str, db: AsyncSession) -> List[SearchResult]:
        """搜索问题"""
        query = select(Question).where(
            or_(
                Question.title.ilike(f"%{keyword}%"),
                Question.content.ilike(f"%{keyword}%"),
                Question.answer.ilike(f"%{keyword}%")
            )
        )
        
        result = await db.execute(query)
        items = result.scalars().all()
        
        search_results = []
        for item in items:
            # 计算相关性分数
            relevance = self._calculate_relevance(keyword, item.title, item.content)
            
            # 生成摘要
            snippet = self._generate_snippet(keyword, item.content)
            
            search_results.append(SearchResult(
                id=item.id,
                title=item.title,
                snippet=snippet,
                type="question",
                relevance=relevance
            ))
        
        return search_results
    
    def _calculate_relevance(self, keyword: str, title: str, content: str) -> float:
        """计算相关性分数（简单实现）"""
        # 标题中出现关键词的权重更高
        title_weight = 2.0
        content_weight = 1.0
        
        title_score = title.lower().count(keyword.lower()) * title_weight
        content_score = content.lower().count(keyword.lower()) * content_weight
        
        return title_score + content_score
    
    def _generate_snippet(self, keyword: str, content: str, max_length: int = 150) -> str:
        """生成包含关键词的内容摘要"""
        keyword_lower = keyword.lower()
        content_lower = content.lower()
        
        # 查找关键词位置
        pos = content_lower.find(keyword_lower)
        if pos == -1:
            # 如果没有找到关键词，返回内容开头
            return content[:max_length] + "..." if len(content) > max_length else content
        
        # 计算摘要的开始和结束位置
        start = max(0, pos - 50)
        end = min(len(content), pos + len(keyword) + 50)
        
        # 调整开始和结束位置，避免截断单词
        while start > 0 and content[start] != ' ':
            start -= 1
        
        while end < len(content) - 1 and content[end] != ' ':
            end += 1
        
        # 生成摘要
        snippet = content[start:end]
        
        # 添加省略号
        if start > 0:
            snippet = "..." + snippet
        
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet


# 创建服务实例
search_service = SearchService() 
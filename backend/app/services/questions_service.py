from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException

from app.models.questions import QuestionItem, QuestionList
from app.core.logging import logger
from app.models.db.questions import Question


class QuestionsService:
    """问题服务"""
    
    async def get_all(self, db: AsyncSession, category: Optional[str] = None) -> QuestionList:
        """获取所有问题"""
        try:
            query = select(Question)
            if category:
                query = query.where(Question.category == category)
            
            result = await db.execute(query)
            items = result.scalars().all()
            
            # 转换为Pydantic模型
            pydantic_items = []
            for item in items:
                # 使用Property Getter获取列表
                tags = item.tags_list
                related_questions = item.related_questions_list
                
                pydantic_items.append(QuestionItem(
                    id=item.id,
                    title=item.title,
                    content=item.content,
                    answer=item.answer,
                    answerCount=item.answer_count,
                    viewCount=item.view_count,
                    category=item.category,
                    tags=tags,
                    createdAt=item.created_at,
                    updatedAt=item.updated_at,
                    relatedQuestions=related_questions
                ))
            
            return QuestionList(items=pydantic_items, total=len(pydantic_items))
        except Exception as e:
            logger.error(f"获取问题列表失败: {e}")
            raise HTTPException(status_code=500, detail=f"获取问题列表失败: {str(e)}")
    
    async def get_by_id(self, question_id: str, db: AsyncSession) -> Optional[QuestionItem]:
        """根据ID获取问题详情"""
        try:
            query = select(Question).where(Question.id == question_id)
            result = await db.execute(query)
            item = result.scalar_one_or_none()
            
            if not item:
                return None
            
            # 使用Property Getter获取列表
            tags = item.tags_list
            related_questions = item.related_questions_list
            
            return QuestionItem(
                id=item.id,
                title=item.title,
                content=item.content,
                answer=item.answer,
                answerCount=item.answer_count,
                viewCount=item.view_count,
                category=item.category,
                tags=tags,
                createdAt=item.created_at,
                updatedAt=item.updated_at,
                relatedQuestions=related_questions
            )
        except Exception as e:
            logger.error(f"获取问题ID={question_id}失败: {e}")
            raise HTTPException(status_code=500, detail=f"获取问题详情失败: {str(e)}")
    
    async def search(self, keyword: str, db: AsyncSession) -> QuestionList:
        """搜索问题"""
        try:
            query = select(Question).where(
                or_(
                    Question.title.ilike(f"%{keyword}%"),
                    Question.content.ilike(f"%{keyword}%"),
                    Question.answer.ilike(f"%{keyword}%")
                )
            )
            
            result = await db.execute(query)
            items = result.scalars().all()
            
            # 转换为Pydantic模型
            pydantic_items = []
            for item in items:
                # 使用Property Getter获取列表
                tags = item.tags_list
                related_questions = item.related_questions_list
                
                pydantic_items.append(QuestionItem(
                    id=item.id,
                    title=item.title,
                    content=item.content,
                    answer=item.answer,
                    answerCount=item.answer_count,
                    viewCount=item.view_count,
                    category=item.category,
                    tags=tags,
                    createdAt=item.created_at,
                    updatedAt=item.updated_at,
                    relatedQuestions=related_questions
                ))
            
            return QuestionList(items=pydantic_items, total=len(pydantic_items))
        except Exception as e:
            logger.error(f"搜索问题失败, 关键词={keyword}: {e}")
            raise HTTPException(status_code=500, detail=f"搜索问题失败: {str(e)}")
    
    async def get_related_questions(self, question_id: str, limit: int, db: AsyncSession) -> QuestionList:
        """获取相关问题列表"""
        try:
            # 首先获取问题详情
            question = await self.get_by_id(question_id, db)
            if not question:
                raise HTTPException(status_code=404, detail=f"未找到ID为{question_id}的问题")
            
            # 如果问题没有关联问题，则返回空列表
            if not question.relatedQuestions:
                return QuestionList(items=[], total=0)
            
            # 获取关联问题
            related_items = []
            for rel_id in question.relatedQuestions[:limit]:
                rel_question = await self.get_by_id(rel_id, db)
                if rel_question:
                    related_items.append(rel_question)
            
            return QuestionList(items=related_items, total=len(related_items))
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"获取相关问题失败, 问题ID={question_id}: {e}")
            raise HTTPException(status_code=500, detail=f"获取相关问题失败: {str(e)}")


# 创建服务实例
questions_service = QuestionsService() 
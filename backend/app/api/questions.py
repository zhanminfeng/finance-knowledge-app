from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.questions import QuestionItem, QuestionList
from app.services.questions_service import questions_service
from app.core.database import get_async_db

router = APIRouter()

@router.get("", response_model=QuestionList)
async def get_questions(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """获取问题列表"""
    return await questions_service.get_all(db=db, category=category)

@router.get("/{question_id}", response_model=QuestionItem)
async def get_question(
    question_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取特定问题详情"""
    question = await questions_service.get_by_id(question_id, db=db)
    if not question:
        raise HTTPException(status_code=404, detail=f"未找到ID为{question_id}的问题")
    return question

@router.get("/search/{keyword}", response_model=QuestionList)
async def search_questions(
    keyword: str,
    db: AsyncSession = Depends(get_async_db)
):
    """搜索问题"""
    return await questions_service.search(keyword, db=db)

@router.get("/related/{question_id}", response_model=QuestionList)
async def get_related_questions(
    question_id: str, 
    limit: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_async_db)
):
    """获取相关问题列表"""
    return await questions_service.get_related_questions(question_id, limit, db=db) 
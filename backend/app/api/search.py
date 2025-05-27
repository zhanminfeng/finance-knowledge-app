from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.search import SearchRequest, SearchResults
from app.services.search_service import search_service
from app.core.database import get_async_db

router = APIRouter()

@router.post("", response_model=SearchResults)
async def search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """全局内容搜索"""
    return await search_service.search(request, db) 
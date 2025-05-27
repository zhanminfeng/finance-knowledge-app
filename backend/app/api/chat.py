from fastapi import APIRouter
from typing import List, Optional

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理AI聊天请求"""
    return await chat_service.generate_response(request) 
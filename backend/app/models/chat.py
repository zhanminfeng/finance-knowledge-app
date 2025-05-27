from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """聊天消息模型"""
    role: str  # 'user' 或 'assistant'
    content: str


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    history: Optional[List[Message]] = None


class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str 
from fastapi import APIRouter

api_router = APIRouter()

# Import and include all API routes
from app.api.learning import router as learning_router
from app.api.news import router as news_router
from app.api.questions import router as questions_router
from app.api.search import router as search_router
from app.api.chat import router as chat_router

# Include all routers
api_router.include_router(learning_router, prefix="/learning", tags=["learning"])
api_router.include_router(news_router, prefix="/news", tags=["news"])
api_router.include_router(questions_router, prefix="/questions", tags=["questions"])
api_router.include_router(search_router, prefix="/search", tags=["search"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])

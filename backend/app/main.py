from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger
from app.core.database import engine, Base, SessionLocal, async_session
import datetime
import json
from app.models.db.news import News

# 创建数据库表 (仅在需要时执行)
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="面向财经小白的知识和资讯API",
    version=settings.VERSION
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 应用启动和关闭事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("财知道API服务正在启动...")
    
    # 如果启用了雪球API，启动定期获取任务
    if settings.XUEQIU_API_ENABLED:
        from app.services.xueqiu_service import xueqiu_service
        await xueqiu_service.start_fetch_task()
        logger.info("已启动雪球新闻定期获取任务")
    
    async with async_session() as session:
        await News.create_test_data(session)
    
    logger.info("财知道API服务已启动完成！")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("财知道API服务正在关闭...")
    
    # 如果启用了雪球API，停止定期获取任务
    if settings.XUEQIU_API_ENABLED:
        from app.services.xueqiu_service import xueqiu_service
        await xueqiu_service.stop_fetch_task()
        logger.info("已停止雪球新闻定期获取任务")
    
    logger.info("财知道API服务已关闭！")

# 获取同步数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 添加API状态检查端点
@app.get("/api/status")
def check_api_status():
    """
    检查API状态是否正常
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "财知道API服务运行正常"
    }

# 同步测试端点
@app.get("/api/learning")
def test_learning(db: Session = Depends(get_db)):
    """使用同步方式获取学习内容"""
    try:
        # 使用原生SQL查询
        result = db.execute(text("SELECT id, title, short_description, difficulty, tags, related_items FROM learning"))
        rows = result.fetchall()
        
        # 转换为字典列表
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "title": row[1],
                "shortDescription": row[2],
                "difficulty": row[3]
            }
            # 解析JSON字段
            try:
                item["tags"] = json.loads(row[4]) if row[4] else []
            except:
                item["tags"] = []
                
            try:
                item["relatedItems"] = json.loads(row[5]) if row[5] else []
            except:
                item["relatedItems"] = []
                
            items.append(item)
            
        return {"items": items, "total": len(items)}
    except Exception as e:
        logger.error(f"测试端点出错: {e}")
        return {"error": str(e), "items": [], "total": 0}

@app.get("/api/news")
def test_news(db: Session = Depends(get_db)):
    """使用同步方式获取新闻内容"""
    try:
        # 使用原生SQL查询
        result = db.execute(text("SELECT id, title, summary, source, publish_date, content, image_url, category FROM news"))
        rows = result.fetchall()
        
        # 转换为字典列表
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "title": row[1],
                "summary": row[2],
                "source": row[3],
                "publishDate": row[4],
                "content": row[5],
                "imageUrl": row[6]
            }
            # 解析JSON字段
            try:
                item["categories"] = json.loads(row[7]) if row[7] else []
            except:
                item["categories"] = []
                
            items.append(item)
            
        return {"items": items, "total": len(items)}
    except Exception as e:
        logger.error(f"测试端点出错: {e}")
        return {"error": str(e), "items": [], "total": 0}

@app.get("/api/questions")
def test_questions(db: Session = Depends(get_db)):
    """使用同步方式获取问题内容"""
    try:
        # 使用原生SQL查询
        result = db.execute(text("SELECT id, title, content, answer, category, view_count, answer_count, tags, related_questions FROM questions"))
        rows = result.fetchall()
        
        # 转换为字典列表
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "question": row[1],  # 这里可以保持question作为API返回字段，但从数据库获取的是title
                "answer": row[3],
                # 移除difficulty字段或使用其他可用字段代替
            }
            # 解析JSON字段
            try:
                item["categories"] = json.loads(row[4]) if row[4] else []
            except:
                item["categories"] = []
                
            try:
                item["tags"] = json.loads(row[5]) if row[5] else []
            except:
                item["tags"] = []
                
            try:
                item["relatedQuestions"] = json.loads(row[6]) if row[6] else []
            except:
                item["relatedQuestions"] = []
                
            items.append(item)
            
        return {"items": items, "total": len(items)}
    except Exception as e:
        logger.error(f"测试端点出错: {e}")
        return {"error": str(e), "items": [], "total": 0}

# 包含API路由
from app.api import api_router
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "欢迎使用财知道API服务"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
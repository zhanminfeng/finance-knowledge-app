from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
import json
import datetime

from app.core.config import settings
from app.core.logging import logger

# 创建同步数据库引擎和会话
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title=f"{settings.APP_NAME} - 同步版",
    description="面向财经小白的知识和资讯API - 同步版",
    version=settings.VERSION
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 状态端点
@app.get("/api/status")
def check_api_status():
    """
    检查 API 状态
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "财知道API服务运行正常（同步版）"
    }

# 学习内容 API
@app.get("/api/learning")
def get_learning_items(db: Session = Depends(get_db)):
    """
    获取学习内容列表
    """
    try:
        result = db.execute(text("SELECT id, title, short_description, difficulty, tags, related_items FROM learning"))
        rows = result.fetchall()
        
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "title": row[1],
                "shortDescription": row[2],
                "difficulty": row[3]
            }
            # 解析 JSON 字段
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
        logger.error(f"获取学习内容失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取学习内容失败: {str(e)}")

@app.get("/api/learning/{item_id}")
def get_learning_item(item_id: str, db: Session = Depends(get_db)):
    """
    获取特定学习内容
    """
    try:
        result = db.execute(text("SELECT id, title, short_description, content, difficulty, tags, related_items FROM learning WHERE id = :id"), 
                            {"id": item_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的学习内容")
        
        item = {
            "id": row[0],
            "title": row[1],
            "shortDescription": row[2],
            "content": row[3],
            "difficulty": row[4]
        }
        
        # 解析 JSON 字段
        try:
            item["tags"] = json.loads(row[5]) if row[5] else []
        except:
            item["tags"] = []
            
        try:
            item["relatedItems"] = json.loads(row[6]) if row[6] else []
        except:
            item["relatedItems"] = []
            
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取学习内容ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取学习内容失败: {str(e)}")

# 新闻 API
@app.get("/api/news")
def get_news_items(db: Session = Depends(get_db)):
    """
    获取新闻列表
    """
    try:
        result = db.execute(text("SELECT id, title, summary, source, publish_date, content, image_url, categories, url FROM news"))
        rows = result.fetchall()
        
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "title": row[1],
                "summary": row[2],
                "source": row[3],
                "publishDate": str(row[4]),
                "content": row[5],
                "imageUrl": row[6],
                "url": row[8] if row[8] else ""
            }
            # 解析 JSON 字段
            try:
                item["categories"] = json.loads(row[7]) if row[7] else []
            except:
                item["categories"] = []
                
            items.append(item)
            
        return {"items": items, "total": len(items)}
    except Exception as e:
        logger.error(f"获取新闻列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取新闻列表失败: {str(e)}")

@app.get("/api/news/{item_id}")
def get_news_item(item_id: str, db: Session = Depends(get_db)):
    """
    获取特定新闻
    """
    try:
        result = db.execute(text("SELECT id, title, summary, source, publish_date, content, image_url, categories, url FROM news WHERE id = :id"),
                            {"id": item_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的新闻")
        
        item = {
            "id": row[0],
            "title": row[1],
            "summary": row[2],
            "source": row[3],
            "publishDate": str(row[4]),
            "content": row[5],
            "imageUrl": row[6],
            "url": row[8] if row[8] else ""
        }
        
        # 解析 JSON 字段
        try:
            item["categories"] = json.loads(row[7]) if row[7] else []
        except:
            item["categories"] = []
            
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取新闻ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取新闻失败: {str(e)}")

# 问题 API
@app.get("/api/questions")
def get_questions(db: Session = Depends(get_db)):
    """
    获取问题列表
    """
    try:
        result = db.execute(text("SELECT id, question, answer, difficulty, categories, tags, related_questions, view_count, created_at, updated_at FROM questions"))
        rows = result.fetchall()
        
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "question": row[1],
                "answer": row[2],
                "difficulty": row[3],
                "viewCount": row[7],
                "createdAt": str(row[8]) if row[8] else None,
                "updatedAt": str(row[9]) if row[9] else None
            }
            # 解析 JSON 字段
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
        logger.error(f"获取问题列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取问题列表失败: {str(e)}")

@app.get("/api/questions/{item_id}")
def get_question(item_id: str, db: Session = Depends(get_db)):
    """
    获取特定问题
    """
    try:
        # 更新浏览次数
        db.execute(text("UPDATE questions SET view_count = view_count + 1 WHERE id = :id"), {"id": item_id})
        db.commit()
        
        # 获取问题
        result = db.execute(text("SELECT id, question, answer, difficulty, categories, tags, related_questions, view_count, created_at, updated_at FROM questions WHERE id = :id"), 
                            {"id": item_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的问题")
        
        item = {
            "id": row[0],
            "question": row[1],
            "answer": row[2],
            "difficulty": row[3],
            "viewCount": row[7],
            "createdAt": str(row[8]) if row[8] else None,
            "updatedAt": str(row[9]) if row[9] else None
        }
        
        # 解析 JSON 字段
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
            
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取问题ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取问题失败: {str(e)}")

# 搜索 API
@app.post("/api/search")
def search(request: dict, db: Session = Depends(get_db)):
    """
    搜索内容
    """
    try:
        keyword = request.get("query", "")
        categories = request.get("categories", [])
        
        if not keyword:
            return {"results": [], "total": 0}
        
        # 搜索学习内容
        learning_items = []
        result = db.execute(text("""
            SELECT id, title, short_description, difficulty, tags 
            FROM learning 
            WHERE title LIKE :keyword OR short_description LIKE :keyword
        """), {"keyword": f"%{keyword}%"})
        
        for row in result.fetchall():
            item = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "type": "learning",
                "difficulty": row[3]
            }
            try:
                item["tags"] = json.loads(row[4]) if row[4] else []
            except:
                item["tags"] = []
            learning_items.append(item)
        
        # 搜索新闻
        news_items = []
        result = db.execute(text("""
            SELECT id, title, summary, categories
            FROM news
            WHERE title LIKE :keyword OR summary LIKE :keyword
        """), {"keyword": f"%{keyword}%"})
        
        for row in result.fetchall():
            item = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "type": "news"
            }
            try:
                item["categories"] = json.loads(row[3]) if row[3] else []
            except:
                item["categories"] = []
            news_items.append(item)
        
        # 搜索问题
        question_items = []
        result = db.execute(text("""
            SELECT id, question, categories, tags
            FROM questions
            WHERE question LIKE :keyword
        """), {"keyword": f"%{keyword}%"})
        
        for row in result.fetchall():
            item = {
                "id": row[0],
                "title": row[1],
                "description": "",
                "type": "question"
            }
            try:
                item["categories"] = json.loads(row[2]) if row[2] else []
            except:
                item["categories"] = []
                
            try:
                item["tags"] = json.loads(row[3]) if row[3] else []
            except:
                item["tags"] = []
            
            question_items.append(item)
        
        # 合并结果
        all_results = learning_items + news_items + question_items
        
        # 如果指定了分类，则过滤结果
        if categories:
            filtered_results = []
            for item in all_results:
                item_categories = item.get("categories", [])
                if any(cat in item_categories for cat in categories):
                    filtered_results.append(item)
            all_results = filtered_results
        
        return {"results": all_results, "total": len(all_results)}
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 聊天 API
@app.post("/api/chat")
def chat(request: dict):
    """
    聊天 API
    """
    try:
        message = request.get("message", "")
        
        if not message:
            return {"response": "请输入问题"}
        
        # 简化版实现，返回一些预设回答
        if "股票" in message:
            return {"response": "股票是股份公司发行的所有权凭证，持有股票代表着对公司的部分所有权。投资股票可以通过股息收益和资本增值获利，但也面临市场风险。"}
        elif "基金" in message:
            return {"response": "基金是一种集合投资工具，由基金管理公司收集众多投资者的资金，交由专业的基金经理进行投资管理，以追求资产增值。"}
        elif "债券" in message:
            return {"response": "债券是政府、金融机构、工商企业等机构直接向社会借债筹措资金时，向投资者发行，承诺按一定利率支付利息并按约定条件偿还本金的债权债务凭证。"}
        else:
            return {"response": "您好，我是财知道AI助手，有任何财经问题都可以向我提问。"}
    except Exception as e:
        logger.error(f"聊天API错误: {e}")
        raise HTTPException(status_code=500, detail=f"聊天失败: {str(e)}")

# 根路由
@app.get("/")
def root():
    return {"message": "欢迎使用财知道API（同步版）"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
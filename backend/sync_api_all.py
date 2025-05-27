#!/usr/bin/env python
"""
提供所有API端点的同步SQL版本
解决各个端点的500错误问题
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, or_
from sqlalchemy.orm import Session
import json
import datetime
from typing import List, Optional

from app.core.config import settings
from app.core.database import get_db
from app.core.logging import logger
from app.models.learning import LearningItem, LearningList
from app.models.news import NewsItem, NewsList
from app.models.questions import QuestionItem, QuestionList

# 创建FastAPI应用
app = FastAPI(
    title=f"{settings.APP_NAME} - 完全同步版",
    description="面向财经小白的知识和资讯API - 完全同步版",
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

# API状态端点
@app.get("/api/status")
def check_api_status():
    """
    检查API状态
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "财知道API服务运行正常（完全同步版）"
    }

# 学习内容API
@app.get("/api/learning", response_model=LearningList)
def get_learning_items(db: Session = Depends(get_db)):
    """
    获取学习内容列表
    """
    try:
        result = db.execute(text("SELECT id, title, short_description, difficulty, tags, related_items FROM learning"))
        rows = result.fetchall()
        
        items = []
        for row in rows:
            item = LearningItem(
                id=row[0],
                title=row[1],
                shortDescription=row[2],
                difficulty=row[3],
                tags=json.loads(row[4]) if row[4] else [],
                relatedItems=json.loads(row[5]) if row[5] else []
            )
            items.append(item)
            
        return LearningList(items=items, total=len(items))
    except Exception as e:
        logger.error(f"获取学习内容失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取学习内容失败: {str(e)}")

@app.get("/api/learning/{item_id}", response_model=LearningItem)
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
        
        return LearningItem(
            id=row[0],
            title=row[1],
            shortDescription=row[2],
            content=row[3],
            difficulty=row[4],
            tags=json.loads(row[5]) if row[5] else [],
            relatedItems=json.loads(row[6]) if row[6] else []
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取学习内容ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取学习内容失败: {str(e)}")

# 新闻API
@app.get("/api/news", response_model=NewsList)
def get_news_items(db: Session = Depends(get_db)):
    """
    获取新闻列表
    """
    try:
        result = db.execute(text("SELECT id, title, summary, source, publish_date, content, image_url, categories, url FROM news"))
        rows = result.fetchall()
        
        items = []
        for row in rows:
            item = NewsItem(
                id=row[0],
                title=row[1],
                summary=row[2],
                source=row[3],
                publishDate=str(row[4]),
                content=row[5],
                imageUrl=row[6],
                categories=json.loads(row[7]) if row[7] else [],
                url=row[8] if row[8] else ""
            )
            items.append(item)
            
        return NewsList(items=items, total=len(items))
    except Exception as e:
        logger.error(f"获取新闻列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取新闻列表失败: {str(e)}")

@app.get("/api/news/{item_id}", response_model=NewsItem)
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
        
        return NewsItem(
            id=row[0],
            title=row[1],
            summary=row[2],
            source=row[3],
            publishDate=str(row[4]),
            content=row[5],
            imageUrl=row[6],
            categories=json.loads(row[7]) if row[7] else [],
            url=row[8] if row[8] else ""
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取新闻ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取新闻失败: {str(e)}")

# 问题API
@app.get("/api/questions", response_model=QuestionList)
def get_questions(db: Session = Depends(get_db)):
    """
    获取问题列表
    """
    try:
        result = db.execute(text("SELECT id, question, answer, difficulty, categories, tags, related_questions, view_count, created_at, updated_at FROM questions"))
        rows = result.fetchall()
        
        items = []
        for row in rows:
            item = QuestionItem(
                id=row[0],
                question=row[1],
                answer=row[2],
                difficulty=row[3],
                categories=json.loads(row[4]) if row[4] else [],
                tags=json.loads(row[5]) if row[5] else [],
                relatedQuestions=json.loads(row[6]) if row[6] else [],
                viewCount=row[7],
                createdAt=str(row[8]) if row[8] else None,
                updatedAt=str(row[9]) if row[9] else None
            )
            items.append(item)
            
        return QuestionList(items=items, total=len(items))
    except Exception as e:
        logger.error(f"获取问题列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取问题列表失败: {str(e)}")

@app.get("/api/questions/{item_id}", response_model=QuestionItem)
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
        
        return QuestionItem(
            id=row[0],
            question=row[1],
            answer=row[2],
            difficulty=row[3],
            categories=json.loads(row[4]) if row[4] else [],
            tags=json.loads(row[5]) if row[5] else [],
            relatedQuestions=json.loads(row[6]) if row[6] else [],
            viewCount=row[7],
            createdAt=str(row[8]) if row[8] else None,
            updatedAt=str(row[9]) if row[9] else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取问题ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取问题失败: {str(e)}")

# 搜索API
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
                "difficulty": row[3],
                "tags": json.loads(row[4]) if row[4] else []
            }
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
                "type": "news",
                "categories": json.loads(row[3]) if row[3] else []
            }
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
                "type": "question",
                "categories": json.loads(row[2]) if row[2] else [],
                "tags": json.loads(row[3]) if row[3] else []
            }
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

# 聊天API
@app.post("/api/chat")
def chat(request: dict):
    """
    聊天API
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

# 添加雪球新闻API端点
@app.get("/api/news/xueqiu/categories", response_model=List[str])
def get_xueqiu_categories():
    """获取雪球新闻可用分类"""
    if not settings.XUEQIU_API_ENABLED:
        raise HTTPException(status_code=403, detail="雪球API未启用")
    
    return ["全部", "股市", "美股", "宏观", "外汇", "商品", "基金", "私募", "房产"]

@app.post("/api/news/xueqiu/fetch")
def fetch_xueqiu_news(category: Optional[str] = "全部"):
    """
    手动获取最新雪球新闻
    
    此端点为同步版API，不支持后台任务，将直接返回执行结果
    """
    if not settings.XUEQIU_API_ENABLED:
        raise HTTPException(status_code=403, detail="雪球API未启用")
    
    try:
        # 同步版本只能使用requests库发送请求
        import requests
        import json
        from datetime import datetime
        
        # 构建请求
        url = settings.XUEQIU_NEWS_URL
        headers = {
            "User-Agent": settings.XUEQIU_USER_AGENT,
            "Cookie": settings.XUEQIU_COOKIE,
            "Accept": "application/json, text/plain, */*"
        }
        
        params = {
            "since_id": -1,
            "max_id": -1,
            "size": settings.XUEQIU_NEWS_LIMIT
        }
        
        # 如果不是"全部"，添加分类过滤参数
        if category != "全部":
            category_mapping = {
                "股市": 102,
                "美股": 101,
                "宏观": 6,
                "外汇": 111,
                "商品": 113,
                "基金": 104,
                "私募": 105,
                "房产": 116
            }
            if category in category_mapping:
                params["category"] = category_mapping[category]
        
        # 发送请求
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            return {"message": f"雪球API请求失败: 状态码 {response.status_code}"}
        
        data = response.json()
        if "list" not in data:
            return {"message": "雪球API返回数据格式异常"}
            
        # 处理新闻数据
        news_list = []
        saved_count = 0
        
        with engine.connect() as conn:
            for item in data["list"]:
                try:
                    # 获取主要内容
                    title = item.get("title", "")
                    if not title and "text" in item:
                        # 如果没有标题，使用正文前30个字作为标题
                        title = item["text"][:30] + "..." if len(item["text"]) > 30 else item["text"]
                    
                    # 生成唯一ID (使用雪球的ID)
                    news_id = f"xueqiu-{item.get('id', '')}"
                    
                    # 检查是否已存在
                    check_result = conn.execute(
                        text("SELECT id FROM news WHERE id = :id"),
                        {"id": news_id}
                    ).fetchone()
                    
                    if check_result:
                        continue
                    
                    # 发布日期处理
                    created_at = item.get("created_at", 0)
                    if created_at:
                        publish_date = datetime.fromtimestamp(created_at / 1000)  # 雪球时间戳是毫秒
                    else:
                        publish_date = datetime.now()
                    
                    # 提取摘要 (去除HTML标签)
                    text = item.get("text", "").replace("<[^>]+>", "")
                    summary = text[:100] + "..." if len(text) > 100 else text
                    
                    # 标签和分类
                    tags = item.get("topics", [])
                    categories = [category] if category != "全部" else []
                    
                    # 保存新闻到数据库
                    conn.execute(
                        text("""
                        INSERT INTO news (
                            id, title, summary, content, source, publish_date, 
                            image_url, url, categories, tags
                        ) VALUES (
                            :id, :title, :summary, :content, :source, :publish_date,
                            :image_url, :url, :categories, :tags
                        )
                        """),
                        {
                            "id": news_id,
                            "title": title,
                            "summary": summary,
                            "content": text,
                            "source": "雪球",
                            "publish_date": publish_date.strftime("%Y-%m-%d"),
                            "image_url": item.get("user", {}).get("profile_image_url", ""),
                            "url": f"https://xueqiu.com/{item.get('user_id', '')}/{item.get('id', '')}",
                            "categories": json.dumps(categories),
                            "tags": json.dumps(tags)
                        }
                    )
                    
                    saved_count += 1
                    
                except Exception as e:
                    print(f"处理雪球新闻项时出错: {str(e)}")
                    continue
            
            # 提交事务
            conn.commit()
            
        return {"message": f"成功获取并保存 {saved_count} 条雪球新闻"}
    except Exception as e:
        return {"message": f"获取雪球新闻时出错: {str(e)}"}

# 根路由
@app.get("/")
def root():
    return {"message": "欢迎使用财知道API（完全同步版）"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
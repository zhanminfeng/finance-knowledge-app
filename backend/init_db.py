import asyncio
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db, Base, engine, async_engine
from app.models.learning import Learning
from app.models.news import News
from app.models.questions import Question
from app.core.config import settings

async def init_db():
    """初始化数据库并填充测试数据"""
    print("正在初始化数据库...")
    
    # 创建表 - 使用同步方式
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 获取异步会话
    async_session_generator = get_async_db()
    db = await anext(async_session_generator)
    
    try:
        # 加载学习内容数据
        await load_learning_data(db)
        
        # 加载新闻数据
        await load_news_data(db)
        
        # 加载问题数据
        await load_questions_data(db)
        
        await db.commit()
        print("数据库初始化完成！")
    except Exception as e:
        await db.rollback()
        print(f"初始化数据库时出错: {e}")
    finally:
        await db.close()

async def load_learning_data(db: AsyncSession):
    """加载学习内容数据"""
    data_file = settings.DATA_DIR / "learning_data.json"
    if not data_file.exists():
        print(f"警告: 找不到学习内容数据文件 {data_file}")
        return
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item_data in data:
            learning_item = Learning(
                id=item_data.get("id", None),
                title=item_data["title"],
                short_description=item_data["shortDescription"],
                content=item_data.get("fullContent", ""),  # 使用fullContent字段
                difficulty=item_data["difficulty"]
            )
            learning_item.tags_list = item_data.get("tags", [])
            learning_item.related_items_list = item_data.get("nextSteps", [])  # 使用nextSteps字段
            
            db.add(learning_item)
        
        print(f"已加载 {len(data)} 条学习内容数据")
    except Exception as e:
        print(f"加载学习内容数据时出错: {e}")
        raise

async def load_news_data(db: AsyncSession):
    """加载新闻数据"""
    data_file = settings.DATA_DIR / "news_data.json"
    if not data_file.exists():
        print(f"警告: 找不到新闻数据文件 {data_file}")
        return
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item_data in data:
            # 将日期字符串转换为datetime对象
            date_str = item_data.get("date", None)
            publish_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
            
            news_item = News(
                id=item_data.get("id", None),
                title=item_data["title"],
                source=item_data["source"],
                publish_date=publish_date,
                summary=item_data["summary"],
                content=item_data["content"],
                image_url=item_data.get("imageUrl", ""),
                url=item_data.get("url", "")
            )
            news_item.categories_list = [item_data.get("category", "")] if item_data.get("category") else []
            
            db.add(news_item)
        
        print(f"已加载 {len(data)} 条新闻数据")
    except Exception as e:
        print(f"加载新闻数据时出错: {e}")
        raise

async def load_questions_data(db: AsyncSession):
    """加载问题数据"""
    data_file = settings.DATA_DIR / "questions_data.json"
    if not data_file.exists():
        print(f"警告: 找不到问题数据文件 {data_file}")
        return
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item_data in data:
            question_item = Question(
                id=item_data.get("id", None),
                question=item_data["question"],
                answer=item_data.get("fullAnswer", item_data.get("previewAnswer", "")),
                difficulty=item_data.get("difficulty", "基础")
            )
            question_item.categories_list = [item_data.get("category", "")] if item_data.get("category") else []
            question_item.tags_list = item_data.get("tags", [])
            question_item.related_questions_list = item_data.get("relatedQuestions", [])
            
            db.add(question_item)
        
        print(f"已加载 {len(data)} 条问题数据")
    except Exception as e:
        print(f"加载问题数据时出错: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db()) 
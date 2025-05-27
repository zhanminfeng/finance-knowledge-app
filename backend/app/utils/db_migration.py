import json
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.learning import Learning
from app.models.news import News
from app.models.questions import Question
from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import logger

def load_json_data(filename):
    """从JSON文件加载数据"""
    file_path = os.path.join(settings.DATA_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载{file_path}时出错: {e}")
        return None

def init_db():
    """初始化数据库，创建表"""
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表已创建")

def migrate_learning_data(db: Session):
    """迁移学习内容数据"""
    data = load_json_data('learning_data.json')
    if not data:
        return
    
    count = 0
    for item in data:
        # 检查记录是否已存在
        existing = db.query(Learning).filter(Learning.id == item.get('id')).first()
        if existing:
            continue
        
        learning = Learning(
            id=item.get('id'),
            title=item.get('title'),
            short_description=item.get('shortDescription'),
            content=item.get('fullContent', ''),
            difficulty=item.get('difficulty'),
            tags=json.dumps(item.get('tags', [])),
            related_items=json.dumps(item.get('nextSteps', []))
        )
        db.add(learning)
        count += 1
    
    db.commit()
    logger.info(f"成功迁移了 {count} 条学习内容数据")

def migrate_news_data(db: Session):
    """迁移新闻数据"""
    data = load_json_data('news_data.json')
    if not data:
        return
    
    count = 0
    for item in data:
        # 检查记录是否已存在
        existing = db.query(News).filter(News.id == item.get('id')).first()
        if existing:
            continue
        
        # 日期处理
        date_str = item.get('date')
        try:
            date = datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            date = datetime.now()
        
        news = News(
            id=item.get('id'),
            title=item.get('title'),
            summary=item.get('summary'),
            content=item.get('content', ''),
            source=item.get('source'),
            date=date,
            category=item.get('category'),
            image_url=item.get('imageUrl'),
            tags=json.dumps(item.get('tags', [])),
            ai_explanation=item.get('aiInterpretation', '')
        )
        db.add(news)
        count += 1
    
    db.commit()
    logger.info(f"成功迁移了 {count} 条新闻数据")

def migrate_questions_data(db: Session):
    """迁移问题数据"""
    data = load_json_data('questions_data.json')
    if not data:
        return
    
    count = 0
    for item in data:
        # 检查记录是否已存在
        existing = db.query(Question).filter(Question.id == item.get('id')).first()
        if existing:
            continue
        
        question = Question(
            id=item.get('id'),
            question=item.get('question'),
            preview_answer=item.get('previewAnswer'),
            full_answer=item.get('fullAnswer', ''),
            category=item.get('category'),
            tags=json.dumps(item.get('tags', [])),
            related_questions=json.dumps(item.get('relatedQuestions', []))
        )
        db.add(question)
        count += 1
    
    db.commit()
    logger.info(f"成功迁移了 {count} 条问题数据")

def run_migration():
    """运行所有迁移"""
    from app.core.database import SessionLocal
    
    # 初始化数据库
    init_db()
    
    # 获取数据库会话
    db = SessionLocal()
    try:
        # 执行迁移
        migrate_learning_data(db)
        migrate_news_data(db)
        migrate_questions_data(db)
        logger.info("所有数据迁移完成")
    finally:
        db.close()

if __name__ == "__main__":
    run_migration() 
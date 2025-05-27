#!/usr/bin/env python
"""
学习内容同步API端点
提供独立的同步SQL版本API端点
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.logging import logger
from app.models.learning import LearningItem, LearningList

# 创建路由器
router = APIRouter(tags=["learning_sync"])

@router.get("", response_model=LearningList)
def get_learning_items_sync(db: Session = Depends(get_db)):
    """
    使用同步SQL获取学习内容列表
    """
    try:
        # 使用原生SQL查询
        result = db.execute(text("SELECT id, title, short_description, difficulty, tags, related_items FROM learning"))
        rows = result.fetchall()
        
        # 转换为Pydantic模型列表
        items = []
        for row in rows:
            # 解析JSON字段
            try:
                tags = json.loads(row[4]) if row[4] else []
            except Exception as e:
                logger.warning(f"解析标签失败: {e}")
                tags = []
                
            try:
                related_items = json.loads(row[5]) if row[5] else []
            except Exception as e:
                logger.warning(f"解析相关项目失败: {e}")
                related_items = []
            
            # 创建Pydantic模型
            item = LearningItem(
                id=row[0],
                title=row[1],
                shortDescription=row[2],
                difficulty=row[3],
                tags=tags,
                relatedItems=related_items
            )
            items.append(item)
            
        return LearningList(items=items, total=len(items))
    except Exception as e:
        logger.error(f"获取学习内容失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取学习内容失败: {str(e)}")

@router.get("/{item_id}", response_model=LearningItem)
def get_learning_item_sync(item_id: str, db: Session = Depends(get_db)):
    """
    使用同步SQL获取特定学习内容
    """
    try:
        # 使用原生SQL查询
        result = db.execute(
            text("SELECT id, title, short_description, content, difficulty, tags, related_items FROM learning WHERE id = :id"), 
            {"id": item_id}
        )
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的学习内容")
        
        # 解析JSON字段
        try:
            tags = json.loads(row[5]) if row[5] else []
        except Exception as e:
            logger.warning(f"解析标签失败: {e}")
            tags = []
            
        try:
            related_items = json.loads(row[6]) if row[6] else []
        except Exception as e:
            logger.warning(f"解析相关项目失败: {e}")
            related_items = []
        
        # 创建Pydantic模型
        item = LearningItem(
            id=row[0],
            title=row[1],
            shortDescription=row[2],
            content=row[3],
            difficulty=row[4],
            tags=tags,
            relatedItems=related_items
        )
        
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取学习内容ID={item_id}失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取学习内容失败: {str(e)}")

# 测试代码
if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI()
    app.include_router(router, prefix="/api/learning_sync")
    
    print("启动学习内容同步API服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8001) 
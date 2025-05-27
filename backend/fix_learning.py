#!/usr/bin/env python
"""
修复Learning API端点的工具
提供同步SQL版本的API端点来替代异步ORM版本
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.logging import logger
from app.models.learning import LearningItem, LearningList

# 创建路由器
router = APIRouter()

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

def apply_fix():
    """
    应用修复：替换app.api.learning中的路由处理程序
    """
    from app.api.learning import router as original_router
    
    # 替换路由处理程序
    for route in router.routes:
        for i, original_route in enumerate(original_router.routes):
            if original_route.path == route.path and original_route.methods == route.methods:
                original_router.routes[i] = route
                print(f"已替换路由: {route.path} {route.methods}")
    
    print("学习内容API修复已应用")

if __name__ == "__main__":
    # 测试路由处理程序
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI()
    app.include_router(router, prefix="/api/learning", tags=["learning"])
    
    print("启动修复版学习内容API服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8001) 
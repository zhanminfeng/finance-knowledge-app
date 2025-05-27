from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import traceback

from app.models.learning import LearningItem, LearningList, LearningCreate, LearningUpdate, Learning
from app.services.learning_service import learning_service
from app.core.database import get_async_db
from app.core.logging import logger

router = APIRouter()

@router.get("/debug", response_model=Dict[str, Any])
async def debug_learning_items(
    db: AsyncSession = Depends(get_async_db)
):
    """调试端点：获取原始学习内容列表"""
    response = {"success": False, "error": None, "items": []}
    try:
        logger.info("开始执行调试查询")
        query = select(Learning)
        logger.info(f"查询: {query}")
        
        result = await db.execute(query)
        logger.info("查询执行完成")
        
        items = result.scalars().all()
        logger.info(f"获取到 {len(items)} 条记录")
        
        # 手动转换为字典列表
        item_dicts = []
        for item in items:
            try:
                logger.info(f"处理记录ID: {item.id}")
                item_dict = {
                    "id": item.id,
                    "title": item.title,
                    "short_description": item.short_description,
                    "difficulty": item.difficulty,
                    "created_at": str(item.created_at) if item.created_at else None,
                    "updated_at": str(item.updated_at) if item.updated_at else None
                }
                
                try:
                    item_dict["tags"] = item.tags_list
                    logger.info(f"成功获取标签: {item_dict['tags']}")
                except Exception as e:
                    logger.error(f"获取标签失败: {str(e)}")
                    item_dict["tags"] = []
                    item_dict["tags_error"] = str(e)
                    
                try:
                    item_dict["related_items"] = item.related_items_list
                    logger.info(f"成功获取相关项目: {item_dict['related_items']}")
                except Exception as e:
                    logger.error(f"获取相关项目失败: {str(e)}")
                    item_dict["related_items"] = []
                    item_dict["related_items_error"] = str(e)
                    
                item_dicts.append(item_dict)
                logger.info(f"成功添加记录到结果列表")
            except Exception as e:
                logger.error(f"处理记录时出错: {str(e)}")
                item_dicts.append({"error": str(e), "traceback": traceback.format_exc()})
        
        response["success"] = True
        response["items"] = item_dicts
        logger.info("调试查询成功完成")
        return response
    except Exception as e:
        error_detail = {
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        logger.error(f"调试查询失败: {error_detail}")
        response["error"] = error_detail
        return response

@router.get("", response_model=LearningList)
async def get_learning_items(
    difficulty: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """获取学习内容列表"""
    return await learning_service.get_all(db=db, difficulty=difficulty)

@router.get("/{item_id}", response_model=LearningItem)
async def get_learning_item(
    item_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取特定学习内容详情"""
    return await learning_service.get_by_id(item_id, db=db)

@router.get("/search/{keyword}", response_model=LearningList)
async def search_learning_items(
    keyword: str,
    db: AsyncSession = Depends(get_async_db)
):
    """搜索学习内容"""
    return await learning_service.search(keyword, db=db)

@router.post("", response_model=LearningItem, status_code=201)
async def create_learning_item(
    item: LearningCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """创建新的学习内容"""
    return await learning_service.create(item, db=db)

@router.put("/{item_id}", response_model=LearningItem)
async def update_learning_item(
    item_id: str,
    item: LearningUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """更新学习内容"""
    return await learning_service.update(item_id, item, db=db)

@router.delete("/{item_id}", status_code=204)
async def delete_learning_item(
    item_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """删除学习内容"""
    await learning_service.delete(item_id, db=db)
    return None 
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import Depends, HTTPException
import json

from app.core.logging import logger
from app.models.learning import Learning, LearningItem, LearningList, LearningCreate, LearningUpdate
from app.core.database import get_async_db

class LearningService:
    """学习内容服务"""
    
    async def get_all(self, db: AsyncSession, difficulty: Optional[str] = None) -> LearningList:
        """获取所有学习内容"""
        try:
            query = select(Learning)
            if difficulty:
                query = query.where(Learning.difficulty == difficulty)
            
            result = await db.execute(query)
            items = result.scalars().all()
            
            # 转换为Pydantic模型
            pydantic_items = []
            for item in items:
                # 使用Property Getter获取列表
                tags = item.tags_list
                related_items = item.related_items_list
                
                pydantic_items.append(LearningItem(
                    id=item.id,
                    title=item.title,
                    shortDescription=item.short_description,
                    difficulty=item.difficulty,
                    tags=tags,
                    content=item.content,
                    relatedItems=related_items
                ))
            
            return LearningList(items=pydantic_items, total=len(pydantic_items))
        except Exception as e:
            logger.error(f"获取学习内容失败: {e}")
            raise HTTPException(status_code=500, detail="获取学习内容时发生错误")
    
    async def get_by_id(self, item_id: str, db: AsyncSession) -> LearningItem:
        """根据ID获取学习内容"""
        try:
            query = select(Learning).where(Learning.id == item_id)
            result = await db.execute(query)
            item = result.scalar_one_or_none()
            
            if not item:
                raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的学习内容")
            
            # 使用Property Getter获取列表
            tags = item.tags_list
            related_items = item.related_items_list
            
            return LearningItem(
                id=item.id,
                title=item.title,
                shortDescription=item.short_description,
                difficulty=item.difficulty,
                tags=tags,
                content=item.content,
                relatedItems=related_items
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"获取学习内容ID={item_id}失败: {e}")
            raise HTTPException(status_code=500, detail="获取学习内容时发生错误")
    
    async def search(self, keyword: str, db: AsyncSession) -> LearningList:
        """搜索学习内容"""
        try:
            query = select(Learning).where(
                or_(
                    Learning.title.ilike(f"%{keyword}%"),
                    Learning.short_description.ilike(f"%{keyword}%"),
                    Learning.content.ilike(f"%{keyword}%")
                )
            )
            
            result = await db.execute(query)
            items = result.scalars().all()
            
            # 转换为Pydantic模型
            pydantic_items = []
            for item in items:
                # 使用Property Getter获取列表
                tags = item.tags_list
                related_items = item.related_items_list
                
                pydantic_items.append(LearningItem(
                    id=item.id,
                    title=item.title,
                    shortDescription=item.short_description,
                    difficulty=item.difficulty,
                    tags=tags,
                    # 搜索结果不返回全文内容
                    content=None,
                    relatedItems=related_items
                ))
            
            return LearningList(items=pydantic_items, total=len(pydantic_items))
        except Exception as e:
            logger.error(f"搜索学习内容失败, 关键词={keyword}: {e}")
            raise HTTPException(status_code=500, detail="搜索学习内容时发生错误")
    
    async def create(self, item: LearningCreate, db: AsyncSession) -> LearningItem:
        """创建学习内容"""
        try:
            db_item = Learning(
                title=item.title,
                short_description=item.shortDescription,
                content=item.content,
                difficulty=item.difficulty
            )
            
            # 使用Property Setter设置列表
            db_item.tags_list = item.tags
            db_item.related_items_list = item.relatedItems or []
            
            db.add(db_item)
            await db.commit()
            await db.refresh(db_item)
            
            # 使用Property Getter获取列表
            tags = db_item.tags_list
            related_items = db_item.related_items_list
            
            return LearningItem(
                id=db_item.id,
                title=db_item.title,
                shortDescription=db_item.short_description,
                difficulty=db_item.difficulty,
                tags=tags,
                content=db_item.content,
                relatedItems=related_items
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"创建学习内容失败: {e}")
            raise HTTPException(status_code=500, detail="创建学习内容时发生错误")
    
    async def update(self, item_id: str, item: LearningUpdate, db: AsyncSession) -> LearningItem:
        """更新学习内容"""
        try:
            query = select(Learning).where(Learning.id == item_id)
            result = await db.execute(query)
            db_item = result.scalar_one_or_none()
            
            if not db_item:
                raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的学习内容")
            
            # 更新字段
            if item.title is not None:
                db_item.title = item.title
            if item.shortDescription is not None:
                db_item.short_description = item.shortDescription
            if item.content is not None:
                db_item.content = item.content
            if item.difficulty is not None:
                db_item.difficulty = item.difficulty
            if item.tags is not None:
                db_item.tags_list = item.tags
            if item.relatedItems is not None:
                db_item.related_items_list = item.relatedItems
            
            await db.commit()
            await db.refresh(db_item)
            
            # 使用Property Getter获取列表
            tags = db_item.tags_list
            related_items = db_item.related_items_list
            
            return LearningItem(
                id=db_item.id,
                title=db_item.title,
                shortDescription=db_item.short_description,
                difficulty=db_item.difficulty,
                tags=tags,
                content=db_item.content,
                relatedItems=related_items
            )
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"更新学习内容ID={item_id}失败: {e}")
            raise HTTPException(status_code=500, detail="更新学习内容时发生错误")
    
    async def delete(self, item_id: str, db: AsyncSession) -> bool:
        """删除学习内容"""
        try:
            query = select(Learning).where(Learning.id == item_id)
            result = await db.execute(query)
            db_item = result.scalar_one_or_none()
            
            if not db_item:
                raise HTTPException(status_code=404, detail=f"找不到ID为{item_id}的学习内容")
            
            await db.delete(db_item)
            await db.commit()
            
            return True
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"删除学习内容ID={item_id}失败: {e}")
            raise HTTPException(status_code=500, detail="删除学习内容时发生错误")

# 创建服务实例
learning_service = LearningService() 
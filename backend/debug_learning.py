#!/usr/bin/env python
import asyncio
import sys
import traceback
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.database import AsyncSessionLocal
from app.models.learning import Learning

async def debug_async_db():
    """测试异步数据库连接"""
    print("开始测试异步数据库连接...")
    
    try:
        # 创建异步会话
        print("创建异步数据库会话...")
        async with AsyncSessionLocal() as session:
            # 尝试执行原始SQL查询
            print("\n1. 测试原始SQL查询...")
            try:
                result = await session.execute(text("SELECT id, title FROM learning LIMIT 2"))
                rows = result.fetchall()
                print(f"SQL查询结果: {rows}")
            except Exception as e:
                print(f"原始SQL查询失败: {e}")
                print(traceback.format_exc())
            
            # 尝试使用ORM查询
            print("\n2. 测试ORM查询...")
            try:
                from sqlalchemy import select
                query = select(Learning)
                result = await session.execute(query)
                items = result.scalars().all()
                print(f"ORM查询获取到 {len(items)} 条记录")
                
                # 打印第一条记录
                if items:
                    item = items[0]
                    print(f"第一条记录: ID={item.id}, 标题={item.title}")
                    
                    # 测试JSON字段
                    print("\n3. 测试JSON字段...")
                    try:
                        tags = item.tags_list
                        print(f"标签: {tags}")
                    except Exception as e:
                        print(f"获取标签失败: {e}")
                        print(traceback.format_exc())
            except Exception as e:
                print(f"ORM查询失败: {e}")
                print(traceback.format_exc())
                
    except Exception as e:
        print(f"连接数据库失败: {e}")
        print(traceback.format_exc())

async def debug_learning_service():
    """测试学习内容服务"""
    print("\n开始测试学习内容服务...")
    
    try:
        from app.services.learning_service import learning_service
        
        # 创建异步会话
        async with AsyncSessionLocal() as session:
            try:
                result = await learning_service.get_all(db=session)
                print(f"获取到 {result.total} 条学习内容")
                
                # 打印第一条记录
                if result.items:
                    item = result.items[0]
                    print(f"第一条记录: ID={item.id}, 标题={item.title}")
                    print(f"标签: {item.tags}")
                    print(f"相关内容: {item.relatedItems}")
            except Exception as e:
                print(f"调用服务失败: {e}")
                print(traceback.format_exc())
    except Exception as e:
        print(f"导入或初始化服务失败: {e}")
        print(traceback.format_exc())

async def main():
    """主函数"""
    print("========== 学习内容异步数据库调试 ==========")
    await debug_async_db()
    await debug_learning_service()
    
if __name__ == "__main__":
    asyncio.run(main()) 
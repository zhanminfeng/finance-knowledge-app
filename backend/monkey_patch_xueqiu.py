"""
猴子补丁模块 - 替换雪球API客户端的HTTP请求实现，用于测试
使用方法：在启动API服务器前导入此模块
"""

import asyncio
import json
from datetime import datetime

# 模拟的新闻数据
MOCK_NEWS_DATA = {
    "list": [
        {
            "id": "12345",
            "title": "测试新闻标题",
            "text": "这是一条测试新闻的内容，用于测试雪球API集成功能。",
            "created_at": int(datetime.now().timestamp() * 1000),  # 当前时间的毫秒时间戳
            "user": {
                "profile_image_url": "https://example.com/avatar.jpg"
            },
            "user_id": "u9876",
            "topics": ["股市", "测试"]
        },
        {
            "id": "67890",
            "title": "另一条测试新闻",
            "text": "这是另一条测试新闻的内容。这条新闻将用于测试分类功能。",
            "created_at": int(datetime.now().timestamp() * 1000),
            "user": {
                "profile_image_url": "https://example.com/avatar2.jpg"
            },
            "user_id": "u5432",
            "topics": ["美股", "科技股"]
        }
    ]
}

# 猴子补丁函数 - 替换_make_request方法
async def mock_make_request(self, url, params=None):
    """模拟雪球API的HTTP请求，不实际发送请求"""
    print(f"[猴子补丁] 模拟请求: {url}")
    print(f"[猴子补丁] 请求参数: {params}")
    
    # 直接返回模拟数据，不进行实际请求
    return MOCK_NEWS_DATA

def apply_patches():
    """应用所有猴子补丁"""
    try:
        # 导入相关模块
        try:
            # 导入雪球客户端类
            from app.services.xueqiu_client import XueqiuClient
            
            # 为该类的_make_request方法应用补丁
            XueqiuClient._make_request = mock_make_request
            
            # 如果同步客户端存在，也为其应用补丁
            try:
                from app.services.xueqiu_client import SyncXueqiuClient
                # 为同步客户端创建同步版本的模拟请求
                def mock_sync_make_request(self, url, params=None):
                    print(f"[猴子补丁] 模拟同步请求: {url}")
                    print(f"[猴子补丁] 请求参数: {params}")
                    return MOCK_NEWS_DATA
                
                SyncXueqiuClient._make_request = mock_sync_make_request
                print("[猴子补丁] 成功应用雪球同步API客户端补丁")
            except (ImportError, AttributeError):
                pass  # 同步客户端可能不存在，忽略错误
            
            # 补丁应用成功
            print("[猴子补丁] 成功应用雪球API客户端补丁")
            
            # 可能还需要补丁news_service
            try:
                from app.services.news_service import news_service
                # 覆盖获取最新新闻的方法
                original_fetch_latest = news_service.fetch_latest_xueqiu
                
                async def patched_fetch_latest_xueqiu(category="全部", count=10):
                    print(f"[猴子补丁] 获取最新雪球新闻，分类: {category}, 数量: {count}")
                    # 如果原始方法失败，则使用模拟数据
                    try:
                        return await original_fetch_latest(category, count)
                    except Exception as e:
                        print(f"[猴子补丁] 原始方法失败，使用模拟数据: {e}")
                        # 返回模拟的结果：成功获取2条新闻
                        return 2
                
                news_service.fetch_latest_xueqiu = patched_fetch_latest_xueqiu
                print("[猴子补丁] 成功应用新闻服务补丁")
            except (ImportError, AttributeError) as e:
                print(f"[猴子补丁] 应用新闻服务补丁失败: {e}")
                
            return True
        except ImportError as e:
            print(f"[猴子补丁] 应用补丁失败: {e}")
            return False
    except Exception as e:
        print(f"[猴子补丁] 应用补丁失败: {e}")
        return False

# 自动应用补丁
if __name__ == "__main__":
    apply_patches() 
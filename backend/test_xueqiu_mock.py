import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

# 添加当前目录到Python路径，确保可以导入本地模块
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

# 设置环境变量启用雪球API
os.environ["XUEQIU_API_ENABLED"] = "True"
# 设置一个假的Cookie用于测试
os.environ["XUEQIU_COOKIE"] = "mock_cookie_for_testing"

print("已设置模拟Cookie用于测试...")

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

# 运行测试前先应用猴子补丁
def apply_patches():
    """应用猴子补丁，模拟HTTP请求"""
    # 模拟_make_request方法
    async def mock_make_request(self, url, params=None):
        print(f"模拟请求: {url}")
        print(f"请求参数: {params}")
        return MOCK_NEWS_DATA
    
    # 应用补丁
    from app.services.xueqiu_client import XueqiuClient
    XueqiuClient._make_request = mock_make_request
    
    # 模拟数据库会话
    from app.core.database import get_async_db
    
    class MockAsyncSession:
        async def execute(self, query):
            return MagicMock()
        
        async def commit(self):
            pass
        
        async def rollback(self):
            pass
        
        async def close(self):
            pass
        
        def add(self, obj):
            pass
    
    class MockResult:
        def scalar_one_or_none(self):
            return None
        
        def scalars(self):
            return MagicMock(all=lambda: [])
    
    # 应用数据库会话补丁
    async def mock_get_async_db():
        yield MockAsyncSession()
    
    # 使用补丁替换原函数
    import app.core.database
    app.core.database.get_async_db = mock_get_async_db

# 应用猴子补丁
apply_patches()

from app.services.xueqiu_client import xueqiu_client
from app.services.news_service import news_service
from app.core.config import settings

# 打印配置信息
print(f"雪球API启用状态: {settings.XUEQIU_API_ENABLED}")
print(f"雪球API URL: {settings.XUEQIU_NEWS_URL}")
print(f"Cookie已设置: {'是' if settings.XUEQIU_COOKIE else '否'}")

# 测试用例类
class XueqiuTester:
    """雪球API测试类 - 模拟版"""
    
    def __init__(self):
        self.results = {
            "测试总数": 0,
            "通过": 0,
            "失败": 0,
            "详细结果": []
        }
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("\n======= 开始雪球API集成测试 (模拟模式) =======")
        
        # 测试获取热门新闻
        await self.test_get_hot_news()
        
        # 测试获取不同分类的新闻
        await self.test_get_category_news()
        
        # 测试新闻服务功能
        await self.test_news_service()
        
        # 打印测试结果
        print("\n======= 测试结束 =======")
        print(f"测试总数: {self.results['测试总数']}")
        print(f"通过: {self.results['通过']}")
        print(f"失败: {self.results['失败']}")
        print("\n详细结果:")
        for i, result in enumerate(self.results["详细结果"], 1):
            status = "✅ 通过" if result["通过"] else "❌ 失败"
            print(f"{i}. {result['测试名称']} - {status}")
            if "错误" in result:
                print(f"   错误: {result['错误']}")
    
    def record_result(self, test_name, passed, error=None):
        """记录测试结果"""
        self.results["测试总数"] += 1
        if passed:
            self.results["通过"] += 1
        else:
            self.results["失败"] += 1
        
        result = {
            "测试名称": test_name,
            "通过": passed,
            "时间": datetime.now().isoformat()
        }
        
        if error:
            result["错误"] = str(error)
            
        self.results["详细结果"].append(result)
        
        # 打印结果
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name} - {status}")
        if error:
            print(f"错误: {error}")
    
    async def test_get_hot_news(self):
        """测试获取热门新闻"""
        try:
            news_list = await xueqiu_client.get_hot_news()
            # 验证返回的是列表且不为空
            if isinstance(news_list, list) and len(news_list) > 0:
                # 验证返回的新闻项包含必要字段
                first_item = news_list[0]
                required_fields = ["id", "title", "summary", "content", "date", "source"]
                has_all_fields = all(field in first_item for field in required_fields)
                
                if has_all_fields:
                    print(f"获取到 {len(news_list)} 条新闻")
                    self.record_result("获取热门新闻", True)
                else:
                    missing = [f for f in required_fields if f not in first_item]
                    self.record_result("获取热门新闻", False, f"新闻项缺少必要字段: {missing}")
            else:
                self.record_result("获取热门新闻", False, "返回结果为空或不是列表")
        except Exception as e:
            self.record_result("获取热门新闻", False, str(e))
    
    async def test_get_category_news(self):
        """测试获取不同分类的新闻"""
        categories = ["股市", "美股", "宏观"]
        
        for category in categories:
            try:
                news_list = await xueqiu_client.get_hot_news(category=category)
                # 验证返回的是列表
                if isinstance(news_list, list):
                    print(f"获取到 {len(news_list)} 条 [{category}] 分类新闻")
                    self.record_result(f"获取 [{category}] 分类新闻", True)
                else:
                    self.record_result(f"获取 [{category}] 分类新闻", False, "返回结果不是列表")
            except Exception as e:
                self.record_result(f"获取 [{category}] 分类新闻", False, str(e))
    
    async def test_news_service(self):
        """测试新闻服务功能"""
        try:
            # 测试获取雪球分类
            categories = await news_service.get_xueqiu_categories()
            if isinstance(categories, list) and len(categories) > 0:
                self.record_result("获取雪球分类", True)
            else:
                self.record_result("获取雪球分类", False, "分类列表为空或不是列表")
            
            # 测试获取最新新闻
            try:
                count = await news_service.fetch_latest_xueqiu(category="全部")
                self.record_result("获取最新新闻", True)
            except Exception as e:
                self.record_result("获取最新新闻", False, str(e))
                
        except Exception as e:
            self.record_result("测试新闻服务", False, str(e))

# 主函数
async def main():
    tester = XueqiuTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 
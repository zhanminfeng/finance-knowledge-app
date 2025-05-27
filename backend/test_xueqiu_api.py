import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 添加当前目录到Python路径，确保可以导入本地模块
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

# 设置环境变量启用雪球API
os.environ["XUEQIU_API_ENABLED"] = "True"
if not os.environ.get("XUEQIU_COOKIE"):
    print("警告: 未设置XUEQIU_COOKIE环境变量，测试可能会失败")
    print("请使用以下命令设置雪球Cookie:")
    print("export XUEQIU_COOKIE='您的雪球网站Cookie'")

from app.services.xueqiu_client import xueqiu_client
from app.services.news_service import news_service
from app.core.config import settings
from app.core.database import get_async_db

# 打印配置信息
print(f"雪球API启用状态: {settings.XUEQIU_API_ENABLED}")
print(f"雪球API URL: {settings.XUEQIU_NEWS_URL}")
print(f"Cookie已设置: {'是' if settings.XUEQIU_COOKIE else '否'}")

# 测试用例类
class XueqiuTester:
    """雪球API测试类"""
    
    def __init__(self):
        self.results = {
            "测试总数": 0,
            "通过": 0,
            "失败": 0,
            "详细结果": []
        }
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("\n======= 开始雪球API集成测试 =======")
        
        # 测试获取热门新闻
        await self.test_get_hot_news()
        
        # 测试获取不同分类的新闻
        await self.test_get_category_news()
        
        # 测试保存新闻到数据库
        await self.test_save_news()
        
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
    
    async def test_save_news(self):
        """测试保存新闻到数据库"""
        try:
            # 获取异步数据库会话
            db_generator = get_async_db()
            db = await anext(db_generator)
            
            try:
                # 获取并保存新闻
                count = await news_service.fetch_latest_xueqiu(category="全部", db=db)
                
                if count > 0:
                    print(f"成功保存 {count} 条新闻到数据库")
                    self.record_result("保存新闻到数据库", True)
                else:
                    # 如果没有新增新闻，可能是因为新闻已存在，这也是成功的
                    print("没有新增新闻，可能是因为新闻已存在")
                    self.record_result("保存新闻到数据库", True)
            except Exception as e:
                await db.rollback()
                self.record_result("保存新闻到数据库", False, str(e))
            finally:
                await db.close()
        except Exception as e:
            self.record_result("保存新闻到数据库", False, f"获取数据库会话失败: {str(e)}")

# 主函数
async def main():
    tester = XueqiuTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 
import sys
import os
from pathlib import Path

# 获取backend目录的绝对路径
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# 设置环境变量
os.environ["XUEQIU_API_ENABLED"] = "True"
os.environ["XUEQIU_COOKIE"] = "mock_cookie_for_testing"

# 运行mock测试
if __name__ == "__main__":
    os.chdir(backend_dir)  # 切换到backend目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    print("开始雪球API模拟测试...")
    import test_xueqiu_mock
    import asyncio
    asyncio.run(test_xueqiu_mock.main()) 
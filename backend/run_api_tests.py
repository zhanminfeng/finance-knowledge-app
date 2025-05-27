import sys
import os
from pathlib import Path

# 获取backend目录的绝对路径
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# 运行API端点测试
if __name__ == "__main__":
    os.chdir(backend_dir)  # 切换到backend目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    print("运行雪球API端点测试...")
    print("确保服务器已经启动（使用start_server.py）")
    import test_xueqiu_api_endpoints
    test_xueqiu_api_endpoints.run_all_tests() 
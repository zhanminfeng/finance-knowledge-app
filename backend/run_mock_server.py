#!/usr/bin/env python3
"""
用于测试的简单服务器启动脚本
这个脚本会启动一个完全使用猴子补丁的服务器，不会尝试连接实际的雪球API
"""
import os
import sys
from pathlib import Path

# 设置backend目录路径
backend_dir = Path(__file__).resolve().parent
os.chdir(backend_dir)  # 切换到backend目录
sys.path.insert(0, str(backend_dir))  # 将backend目录添加到Python路径

# 设置环境变量
os.environ["XUEQIU_API_ENABLED"] = "True"
os.environ["XUEQIU_COOKIE"] = "mock_cookie_for_testing"

# 导入猴子补丁模块并应用补丁
try:
    print("正在导入和应用猴子补丁...")
    from monkey_patch_xueqiu import apply_patches
    if apply_patches():
        print("✅ 雪球API猴子补丁应用成功")
    else:
        print("❌ 雪球API猴子补丁应用失败")
except Exception as e:
    print(f"❌ 导入猴子补丁失败: {e}")
    sys.exit(1)

# 启动服务器
if __name__ == "__main__":
    print("启动模拟服务器，已启用雪球API...")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    
    # 导入并配置FastAPI应用
    import uvicorn
    
    # 不使用reload，避免子进程路径问题
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8888,
        log_level="debug"
    ) 
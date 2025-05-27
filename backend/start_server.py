import os
import sys
from pathlib import Path

# 获取backend目录的绝对路径
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# 设置环境变量
os.environ["XUEQIU_API_ENABLED"] = "True"
os.environ["XUEQIU_COOKIE"] = "mock_cookie_for_testing"

# 导入并应用猴子补丁
try:
    from monkey_patch_xueqiu import apply_patches
    if apply_patches():
        print("✅ 雪球API猴子补丁应用成功")
    else:
        print("❌ 雪球API猴子补丁应用失败")
except Exception as e:
    print(f"❌ 导入猴子补丁失败: {e}")

# 导入并运行Uvicorn服务器
import uvicorn

if __name__ == "__main__":
    os.chdir(backend_dir)  # 切换到backend目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    print("启动服务器，已启用雪球API...")
    
    # 直接启动uvicorn，不使用reload模式，因为reload可能会导致路径问题
    uvicorn.run("app.main:app", host="0.0.0.0", port=8888, reload=False) 
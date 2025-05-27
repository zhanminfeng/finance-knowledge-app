#!/usr/bin/env python
"""
应用所有API修复的工具
替换异步ORM端点为同步SQL版本
解决重复表定义问题
"""
import sys
import time
import os
import subprocess
import importlib
import signal
import threading

def apply_model_fixes():
    """修复模型定义中的问题"""
    print("应用模型修复...")
    
    # 引入必要的库
    from sqlalchemy import inspect
    from app.core.database import engine, Base
    
    # 检查数据库中已存在的表
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"已存在的表: {existing_tables}")
    
    # 修复元数据，避免重复定义表
    for table_name in existing_tables:
        if table_name in Base.metadata.tables:
            print(f"表 '{table_name}' 已存在于元数据中，设置 extend_existing=True")
            Base.metadata.tables[table_name].extend_existing = True
    
    print("模型修复已应用")

def apply_learning_fix():
    """应用学习内容API修复"""
    print("应用学习内容API修复...")
    
    try:
        from fix_learning import router as fixed_router
        from app.api.learning import router as original_router
        
        # 备份原始路由
        original_routes = original_router.routes.copy()
        
        # 替换路由处理程序
        original_router.routes.clear()
        for route in fixed_router.routes:
            original_router.routes.append(route)
            print(f"已添加修复路由: {route.path} {route.methods}")
        
        print("学习内容API修复已应用")
    except Exception as e:
        print(f"应用学习内容API修复失败: {e}")

def apply_sync_api_fixes():
    """应用同步API修复"""
    print("应用同步API修复...")
    
    # 修改main.py添加同步API路由
    try:
        from app.main import app
        import fix_learning
        
        app.include_router(
            fix_learning.router,
            prefix="/api/learning_sync",
            tags=["learning_sync"]
        )
        
        print("同步API路由已添加到主应用")
    except Exception as e:
        print(f"添加同步API路由失败: {e}")

def read_process_output(process, prefix):
    """读取并打印进程的输出"""
    for line in process.stdout:
        print(f"{prefix}: {line.strip()}")

def read_process_error(process, prefix):
    """读取并打印进程的错误输出"""
    for line in process.stderr:
        print(f"{prefix} ERROR: {line.strip()}")

def run_tests():
    """运行测试以验证修复效果"""
    print("\n运行API测试...")
    
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 启动API服务器
    print("启动API服务器...")
    server_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd=current_dir
    )
    
    # 启动线程读取服务器输出
    stdout_thread = threading.Thread(target=read_process_output, args=(server_process, "SERVER"))
    stderr_thread = threading.Thread(target=read_process_error, args=(server_process, "SERVER"))
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()
    
    try:
        # 等待服务器启动
        print("等待服务器启动...")
        time.sleep(5)
        
        # 运行测试
        import requests
        
        def test_endpoint(url):
            print(f"\n测试 {url}")
            try:
                response = requests.get(url)
                print(f"状态码: {response.status_code}")
                if response.status_code == 200:
                    return "✅ 成功"
                else:
                    return f"❌ 失败 ({response.status_code})"
            except Exception as e:
                print(f"请求失败: {e}")
                return "❌ 错误"
        
        endpoints = [
            "http://localhost:8000/api/status",
            "http://localhost:8000/api/learning",
            "http://localhost:8000/api/learning_sync",
        ]
        
        results = {}
        for endpoint in endpoints:
            results[endpoint] = test_endpoint(endpoint)
        
        # 打印测试结果
        print("\n===== 测试结果 =====")
        for endpoint, result in results.items():
            print(f"{endpoint}: {result}")
            
    finally:
        # 关闭服务器
        print("\n关闭服务器...")
        try:
            os.kill(server_process.pid, signal.SIGTERM)
            server_process.wait(timeout=5)
            print("服务器已关闭")
        except Exception as e:
            print(f"关闭服务器时出错: {e}")
            # 强制终止
            try:
                os.kill(server_process.pid, signal.SIGKILL)
            except:
                pass

def main():
    """主函数"""
    print("========== 应用API修复 ==========")
    
    # 应用模型修复
    apply_model_fixes()
    
    # 应用学习内容API修复
    apply_learning_fix()
    
    # 应用同步API
    apply_sync_api_fixes()
    
    # 运行测试
    run_tests()
    
if __name__ == "__main__":
    main() 
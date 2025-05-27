#!/usr/bin/env python
"""
向主应用添加同步API路由
此脚本修改app/main.py来注册额外的同步API路由
"""

import importlib
import os
import sys
import time
import subprocess
import signal
import threading
import requests

def modify_main_app():
    """修改主应用添加同步API路由"""
    print("修改主应用添加同步API路由...")
    
    try:
        # 导入同步API路由
        import fix_learning_sync
        
        # 导入主应用
        from app.main import app
        
        # 注册同步API路由
        app.include_router(
            fix_learning_sync.router,
            prefix="/api/learning_sync"
        )
        
        print("同步API路由已添加到主应用")
        return True
    except Exception as e:
        print(f"添加同步API路由失败: {e}")
        return False

def read_process_output(process, prefix):
    """读取并打印进程的输出"""
    for line in process.stdout:
        print(f"{prefix}: {line.strip()}")

def read_process_error(process, prefix):
    """读取并打印进程的错误输出"""
    for line in process.stderr:
        print(f"{prefix} ERROR: {line.strip()}")

def test_sync_routes():
    """测试同步API路由"""
    print("\n测试同步API路由...")
    
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 启动API服务器
    print("启动API服务器...")
    server_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload"],
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
        
        # 测试同步API路由
        endpoints = [
            "http://localhost:8000/api/status",
            "http://localhost:8000/api/learning",
            "http://localhost:8000/api/learning_sync",
        ]
        
        results = {}
        for endpoint in endpoints:
            print(f"\n测试 {endpoint}")
            try:
                response = requests.get(endpoint)
                status_code = response.status_code
                print(f"状态码: {status_code}")
                if status_code == 200:
                    results[endpoint] = "✅ 成功"
                else:
                    results[endpoint] = f"❌ 失败 ({status_code})"
            except Exception as e:
                print(f"请求失败: {e}")
                results[endpoint] = "❌ 错误"
        
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
            try:
                os.kill(server_process.pid, signal.SIGKILL)
            except:
                pass

def main():
    """主函数"""
    print("===== 添加同步API路由 =====")
    
    # 修改主应用
    success = modify_main_app()
    
    if success:
        # 测试同步API路由
        test_sync_routes()
    else:
        print("由于修改失败，跳过测试")

if __name__ == "__main__":
    main() 
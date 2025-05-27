#!/usr/bin/env python
"""
测试学习内容同步API路由
"""

import os
import sys
import json
import time
import subprocess
import threading
import signal
import requests

# API基础URL
API_BASE_URL = "http://localhost:8000"

def test_learning_sync_endpoint(endpoint="/api/learning_sync", item_id=None):
    """测试学习内容同步API端点"""
    url = f"{API_BASE_URL}{endpoint}"
    if item_id:
        url = f"{url}/{item_id}"
    
    print(f"\n测试 GET {url}")
    
    try:
        response = requests.get(url)
        status_code = response.status_code
        print(f"状态码: {status_code}")
        
        try:
            response_json = response.json()
            print(f"响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"解析响应失败: {e}")
            print(f"原始响应: {response.text}")
        
        if status_code == 200:
            print("✅ 测试成功")
            return True
        else:
            print(f"❌ 测试失败: 状态码 {status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def read_process_output(process, prefix):
    """读取并打印进程的输出"""
    for line in process.stdout:
        print(f"{prefix}: {line.strip()}")

def read_process_error(process, prefix):
    """读取并打印进程的错误输出"""
    for line in process.stderr:
        print(f"{prefix} ERROR: {line.strip()}")

def main():
    """主函数"""
    print("===== 测试学习内容同步API路由 =====")
    
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
        
        # 测试列表端点
        success_list = test_learning_sync_endpoint()
        
        # 如果列表测试成功，尝试获取第一个项目的ID并测试详情端点
        if success_list:
            try:
                response = requests.get(f"{API_BASE_URL}/api/learning_sync")
                if response.status_code == 200:
                    data = response.json()
                    if data["items"] and len(data["items"]) > 0:
                        item_id = data["items"][0]["id"]
                        test_learning_sync_endpoint(item_id=item_id)
            except Exception as e:
                print(f"获取项目ID失败: {e}")
    
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

if __name__ == "__main__":
    main() 
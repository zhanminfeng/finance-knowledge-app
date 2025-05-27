#!/usr/bin/env python
import asyncio
import json
import sys
import subprocess
import time
import threading
import requests
import os
import signal
from concurrent.futures import ThreadPoolExecutor

# API基础URL
API_BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """测试API端点并打印详细信息"""
    url = f"{API_BASE_URL}{endpoint}"
    print(f"\n测试 {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"不支持的HTTP方法: {method}")
            return False
        
        status_code = response.status_code
        print(f"状态码: {status_code}")
        
        try:
            response_json = response.json()
            print(f"响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            
            # 如果是错误响应，检查详细信息
            if status_code >= 400 and "detail" in response_json:
                print(f"错误详情: {response_json['detail']}")
        except Exception as e:
            print(f"解析响应失败 ({e}): {response.text}")
        
        if status_code != expected_status:
            print(f"警告: 状态码 {status_code} 与预期的 {expected_status} 不符")
            return False
        
        return True
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_all_original_endpoints():
    """测试所有原始API端点"""
    print("\n===== 测试原始API端点 =====")
    successes = 0
    failures = 0
    
    # 测试API状态
    if test_api_endpoint("/api/status"):
        successes += 1
    else:
        failures += 1
    
    # 测试学习内容API
    if test_api_endpoint("/api/learning"):
        successes += 1
    else:
        failures += 1
    
    # 测试新闻API
    if test_api_endpoint("/api/news"):
        successes += 1
    else:
        failures += 1
    
    # 测试问题API
    if test_api_endpoint("/api/questions"):
        successes += 1
    else:
        failures += 1
    
    # 测试搜索API
    search_data = {"query": "基金", "categories": []}
    if test_api_endpoint("/api/search", method="POST", data=search_data):
        successes += 1
    else:
        failures += 1
    
    # 测试聊天API
    chat_data = {"message": "什么是股票?"}
    if test_api_endpoint("/api/chat", method="POST", data=chat_data):
        successes += 1
    else:
        failures += 1
    
    # 打印测试摘要
    print(f"\n===== 原始API测试摘要 =====")
    print(f"成功: {successes}")
    print(f"失败: {failures}")
    print(f"总计: {successes + failures}")
    
    return failures == 0

def test_debug_endpoint():
    """测试调试端点"""
    print("\n===== 测试调试端点 =====")
    
    # 测试学习内容API调试端点
    test_api_endpoint("/api/learning/debug")

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
        time.sleep(3)
        
        # 测试API端点
        test_debug_endpoint()
        test_all_original_endpoints()
        
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

if __name__ == "__main__":
    main() 
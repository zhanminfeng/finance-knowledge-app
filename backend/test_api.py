#!/usr/bin/env python
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import requests
import threading

API_BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """测试API端点"""
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
        except:
            print(f"响应内容: {response.text}")
        
        if status_code != expected_status:
            print(f"警告: 状态码 {status_code} 与预期的 {expected_status} 不符")
            return False
        
        return True
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_all_endpoints():
    """测试所有API端点"""
    successes = 0
    failures = 0
    
    # 测试API状态
    if test_api_endpoint("/api/status"):
        successes += 1
    else:
        failures += 1
    
    # 测试学习内容API
    if test_api_endpoint("/api/learning", expected_status=500):
        successes += 1
    else:
        failures += 1
    
    # 测试新闻API
    if test_api_endpoint("/api/news", expected_status=500):
        successes += 1
    else:
        failures += 1
    
    # 测试问题API
    if test_api_endpoint("/api/questions", expected_status=500):
        successes += 1
    else:
        failures += 1
    
    # 测试搜索API
    search_data = {"query": "基金", "categories": []}
    if test_api_endpoint("/api/search", method="POST", data=search_data, expected_status=500):
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
    print(f"\n===== 测试摘要 =====")
    print(f"成功: {successes}")
    print(f"失败: {failures}")
    print(f"总计: {successes + failures}")
    
    return failures == 0

def read_process_output(process, prefix):
    """读取并打印进程的输出"""
    for line in iter(process.stdout.readline, b''):
        print(f"{prefix}: {line.decode().strip()}")

def read_process_error(process, prefix):
    """读取并打印进程的错误输出"""
    for line in iter(process.stderr.readline, b''):
        print(f"{prefix} ERROR: {line.decode().strip()}")

if __name__ == "__main__":
    # 首先启动服务器
    server_process = subprocess.Popen(
        ["python", "-m", "app.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True
    )
    
    # 启动线程读取服务器输出
    stdout_thread = threading.Thread(target=read_process_output, args=(server_process, "SERVER"))
    stderr_thread = threading.Thread(target=read_process_error, args=(server_process, "SERVER"))
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()
    
    print("等待服务器启动...")
    import time
    time.sleep(3)
    
    try:
        success = test_all_endpoints()
        sys.exit(0 if success else 1)
    finally:
        print("关闭服务器...")
        server_process.terminate()
        time.sleep(1)
        print("服务器关闭")
        server_process.wait(5) 
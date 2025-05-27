#!/usr/bin/env python
"""
测试完全同步版API
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
API_BASE_URL = "http://localhost:8001"

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
            # 只打印简化版响应，避免输出过多内容
            if "items" in response_json and len(response_json["items"]) > 2:
                items_count = len(response_json["items"])
                response_json["items"] = response_json["items"][:2]
                response_json["items"].append({"note": f"还有 {items_count - 2} 项未显示..."})
            
            print(f"响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"解析响应失败 ({e}): {response.text}")
        
        if status_code != expected_status:
            print(f"❌ 测试失败: 状态码 {status_code} 与预期的 {expected_status} 不符")
            return False
        
        print("✅ 测试成功")
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_all_endpoints():
    """测试所有API端点"""
    print("\n===== 测试所有API端点 =====")
    
    results = {}
    
    # 测试API状态
    results["/api/status"] = test_api_endpoint("/api/status")
    
    # 测试学习内容API
    results["/api/learning"] = test_api_endpoint("/api/learning")
    # 获取一个学习内容ID用于测试详情
    try:
        response = requests.get(f"{API_BASE_URL}/api/learning")
        if response.status_code == 200:
            data = response.json()
            if data["items"] and len(data["items"]) > 0:
                item_id = data["items"][0]["id"]
                results[f"/api/learning/{item_id}"] = test_api_endpoint(f"/api/learning/{item_id}")
    except:
        pass
    
    # 测试新闻API
    results["/api/news"] = test_api_endpoint("/api/news")
    # 获取一个新闻ID用于测试详情
    try:
        response = requests.get(f"{API_BASE_URL}/api/news")
        if response.status_code == 200:
            data = response.json()
            if data["items"] and len(data["items"]) > 0:
                item_id = data["items"][0]["id"]
                results[f"/api/news/{item_id}"] = test_api_endpoint(f"/api/news/{item_id}")
    except:
        pass
    
    # 测试问题API
    results["/api/questions"] = test_api_endpoint("/api/questions")
    # 获取一个问题ID用于测试详情
    try:
        response = requests.get(f"{API_BASE_URL}/api/questions")
        if response.status_code == 200:
            data = response.json()
            if data["items"] and len(data["items"]) > 0:
                item_id = data["items"][0]["id"]
                results[f"/api/questions/{item_id}"] = test_api_endpoint(f"/api/questions/{item_id}")
    except:
        pass
    
    # 测试搜索API
    search_data = {"query": "基金", "categories": []}
    results["/api/search"] = test_api_endpoint("/api/search", method="POST", data=search_data)
    
    # 测试聊天API
    chat_data = {"message": "什么是股票?"}
    results["/api/chat"] = test_api_endpoint("/api/chat", method="POST", data=chat_data)
    
    # 打印测试摘要
    print("\n===== 测试摘要 =====")
    success_count = sum(1 for result in results.values() if result)
    failure_count = sum(1 for result in results.values() if not result)
    
    for endpoint, result in results.items():
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{endpoint}: {status}")
    
    print(f"\n成功: {success_count}")
    print(f"失败: {failure_count}")
    print(f"总计: {success_count + failure_count}")
    
    return failure_count == 0

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
    print("启动完全同步版API服务器...")
    server_process = subprocess.Popen(
        ["python", "sync_api_all.py"],
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
        
        # 测试端点
        success = test_all_endpoints()
        
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
        
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 
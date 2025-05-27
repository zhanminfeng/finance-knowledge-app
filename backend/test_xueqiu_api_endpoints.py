import requests
import json
import sys
import os
from pathlib import Path

# 服务器URL
API_URL = "http://localhost:8888"

def test_status():
    """测试API状态"""
    print("\n测试API状态...")
    response = requests.get(f"{API_URL}/api/status")
    if response.status_code == 200:
        print(f"✅ 状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return True
    else:
        print(f"❌ 状态码: {response.status_code}")
        return False

def test_xueqiu_categories():
    """测试获取雪球分类"""
    print("\n测试获取雪球分类...")
    response = requests.get(f"{API_URL}/api/news/xueqiu/categories")
    if response.status_code == 200:
        print(f"✅ 状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return True
    else:
        print(f"❌ 状态码: {response.status_code}")
        print(f"错误: {response.text}")
        return False

def test_fetch_xueqiu_news():
    """测试获取雪球新闻"""
    print("\n测试获取雪球新闻...")
    categories = ["全部", "股市", "美股"]
    
    success = True
    for category in categories:
        print(f"\n测试获取[{category}]分类新闻...")
        response = requests.post(f"{API_URL}/api/news/xueqiu/fetch?category={category}")
        if response.status_code == 200:
            print(f"✅ 状态码: {response.status_code}")
            data = response.json()
            print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 状态码: {response.status_code}")
            print(f"错误: {response.text}")
            success = False
    
    return success

def test_start_stop_task():
    """测试启动和停止任务"""
    print("\n测试启动雪球新闻定期获取任务...")
    response = requests.post(f"{API_URL}/api/news/xueqiu/start")
    if response.status_code == 202:
        print(f"✅ 状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        start_success = True
    else:
        print(f"❌ 状态码: {response.status_code}")
        print(f"错误: {response.text}")
        start_success = False
    
    print("\n测试停止雪球新闻定期获取任务...")
    response = requests.post(f"{API_URL}/api/news/xueqiu/stop")
    if response.status_code == 202:
        print(f"✅ 状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        stop_success = True
    else:
        print(f"❌ 状态码: {response.status_code}")
        print(f"错误: {response.text}")
        stop_success = False
    
    return start_success and stop_success

def test_get_news():
    """测试获取新闻列表"""
    print("\n测试获取新闻列表...")
    response = requests.get(f"{API_URL}/api/news")
    if response.status_code == 200:
        print(f"✅ 状态码: {response.status_code}")
        data = response.json()
        print(f"获取到 {data.get('total', 0)} 条新闻")
        
        # 如果有新闻，打印第一条
        if data.get('total', 0) > 0 and len(data.get('items', [])) > 0:
            first_news = data['items'][0]
            print(f"第一条新闻: {first_news.get('title')}")
            print(f"来源: {first_news.get('source')}")
            print(f"是否来自雪球: {first_news.get('is_xueqiu', False)}")
        
        return True
    else:
        print(f"❌ 状态码: {response.status_code}")
        print(f"错误: {response.text}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("======= 开始测试雪球API端点 =======")
    
    # 测试API状态
    if not test_status():
        print("❌ API状态测试失败，中止测试")
        return
    
    # 测试雪球分类
    test_xueqiu_categories()
    
    # 测试获取雪球新闻
    test_fetch_xueqiu_news()
    
    # 测试启动和停止任务
    test_start_stop_task()
    
    # 测试获取新闻列表
    # 注意：这个测试可能需要之前的测试成功才能看到结果
    test_get_news()
    
    print("\n======= 测试完成 =======")

if __name__ == "__main__":
    run_all_tests() 
#!/bin/bash

echo "===== 测试API端点 ====="

BASE_URL="http://localhost:8000/api"

# 测试API状态
echo "\n----- 测试API状态 -----"
curl -s "$BASE_URL/status" | python -m json.tool

# 测试学习内容API
echo "\n----- 测试学习内容API -----"
curl -s "$BASE_URL/learning" | python -m json.tool

# 测试新闻API
echo "\n----- 测试新闻API -----"
curl -s "$BASE_URL/news" | python -m json.tool

# 测试问题API
echo "\n----- 测试问题API -----"
curl -s "$BASE_URL/questions" | python -m json.tool

# 测试搜索API
echo "\n----- 测试搜索API -----"
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"基金","categories":[]}' | python -m json.tool

# 测试聊天API
echo "\n----- 测试聊天API -----"
curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"什么是股票?"}' | python -m json.tool

echo "\n===== 测试完成 =====" 
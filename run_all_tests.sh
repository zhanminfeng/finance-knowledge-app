#!/bin/bash

# 财知道全项目测试脚本

echo "=== 开始运行财知道全项目测试 ==="

# 后端测试
echo -e "\n=== 运行后端测试 ==="
cd backend
python run_tests.py
BACKEND_RESULT=$?
cd ..

# 前端测试
echo -e "\n=== 运行前端测试 ==="
cd frontend
./run_tests.sh
FRONTEND_RESULT=$?
cd ..

# 检查结果
echo -e "\n=== 测试结果汇总 ==="
if [ $BACKEND_RESULT -eq 0 ] && [ $FRONTEND_RESULT -eq 0 ]; then
  echo "✅ 所有测试通过!"
  exit 0
else
  echo "❌ 测试失败!"
  if [ $BACKEND_RESULT -ne 0 ]; then
    echo "   后端测试失败"
  fi
  if [ $FRONTEND_RESULT -ne 0 ]; then
    echo "   前端测试失败"
  fi
  exit 1
fi 
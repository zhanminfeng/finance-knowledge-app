#!/bin/bash

# 财知道前端测试脚本

echo "=== 开始运行财知道前端测试 ==="

# 安装依赖
echo "正在检查和安装依赖..."
npm install

# 运行测试
echo "正在运行测试..."
npm test

# 检查测试结果
if [ $? -eq 0 ]; then
  echo "=== 所有测试通过! ✅ ==="
else
  echo "=== 测试失败! ❌ ==="
  exit 1
fi

# 可选：运行测试覆盖率报告
# echo "正在生成测试覆盖率报告..."
# npm run test:coverage 
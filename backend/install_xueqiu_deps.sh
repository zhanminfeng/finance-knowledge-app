#!/bin/bash

# 安装雪球API所需依赖
echo "安装雪球API集成所需依赖..."
pip install aiohttp==3.9.0 requests==2.31.0

# 安装本地包
echo "安装本地包..."
pip install -e .

echo "依赖安装完成!" 
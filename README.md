# Finance Knowledge App

一个基于 React Native 和 Python 的财经知识学习应用。

## 功能特点

- 📚 财经知识学习
- 📰 实时财经新闻
- 💬 智能问答系统
- 🤖 AI 助手支持

## 技术栈

### 前端
- React Native
- Expo
- TypeScript
- React Navigation

### 后端
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

## 开发环境设置

### 前端
```bash
cd frontend
npm install
npm start
```

### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 系统要求

- Python 3.11
- Node.js (LTS 版本)
- npm
- Expo CLI

## 目录结构

```
.
├── backend/           # FastAPI 后端
│   ├── app/          # 应用代码
│   ├── venv/         # Python 虚拟环境
│   └── requirements.txt
├── frontend/         # React Native 前端
│   ├── src/         # 源代码
│   ├── assets/      # 静态资源
│   └── package.json
└── deploy.sh        # 部署脚本
```

## 快速开始

1. 克隆仓库：
```bash
git clone <repository-url>
cd <project-directory>
```

2. 运行部署脚本：
```bash
./deploy.sh
```

或者后台运行：
```bash
./deploy.sh --background
```

## 手动安装步骤

### 后端设置

1. 创建并激活虚拟环境：
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
```

2. 安装依赖：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. 启动服务：
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端设置

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 启动开发服务器：
```bash
npm start
```

## 调试信息

### 常见问题

1. **Python 版本问题**
   - 确保使用 Python 3.11
   - 检查 Python 路径：`which python3.11`
   - 如果使用 Homebrew：`brew install python@3.11`

2. **Node.js 问题**
   - 检查 Node.js 版本：`node --version`
   - 检查 npm 版本：`npm --version`
   - 如果未安装，使用 nvm 安装：
     ```bash
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
     nvm install --lts
     nvm use --lts
     ```

3. **依赖安装问题**
   - 后端：检查 `requirements.txt` 是否存在
   - 前端：删除 `node_modules` 并重新安装
   - 运行 `npm audit fix` 修复安全漏洞

4. **服务启动问题**
   - 检查端口占用：`lsof -i :8000` 或 `lsof -i :8081`
   - 检查日志文件：`tail -f deploy.log`
   - 确保防火墙未阻止端口访问

### 日志查看

- 部署日志：`tail -f deploy.log`
- 后端日志：`tail -f backend/backend.log`
- 前端日志：`tail -f frontend/frontend.log`

### 服务管理

1. **启动服务**
   - 前台运行：`./deploy.sh`
   - 后台运行：`./deploy.sh --background`

2. **停止服务**
   - 前台运行：按 `Ctrl+C`
   - 后台运行：`pkill -f "uvicorn|npm start|expo"`

3. **检查服务状态**
   - 后端：访问 `http://localhost:8000/docs`
   - 前端：访问 `http://localhost:8081`

### 开发工具

1. **API 文档**
   - Swagger UI：`http://localhost:8000/docs`
   - ReDoc：`http://localhost:8000/redoc`

2. **移动端调试**
   - 安装 Expo Go 应用
   - iOS：App Store
   - Android：Google Play Store

### 本地网络测试

1. **确保设备在同一网络**
   - 手机和电脑必须连接到同一个 WiFi 网络
   - 检查电脑的防火墙设置，确保允许 8081 端口访问

2. **获取电脑的局域网 IP**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows
   ipconfig
   ```

3. **在手机上访问**
   - 打开 Expo Go 应用
   - 点击 "Enter URL manually"
   - 输入电脑的局域网 IP 地址和端口，例如：`http://192.168.1.xxx:8081`

4. **常见问题解决**
   - 如果无法连接，检查：
     - 防火墙设置
     - 网络连接
     - 端口是否被占用
   - 使用 `lsof -i :8081` 检查端口占用
   - 确保手机和电脑在同一网段

5. **开发模式选项**
   - 本地网络模式：`npm start -- --lan`
   - 仅本地模式：`npm start -- --localhost`
   - 隧道模式：`npm start -- --tunnel`（需要 ngrok）

## 项目概述

"财知道"是一款专为财经小白设计的移动端应用，通过简洁易懂的内容帮助用户理解基础财经知识，获取实时财经新闻并解答常见财经问题，降低财经学习门槛。

## 技术架构

本项目采用前后端分离架构：

### 前端技术栈

- **开发框架**：React Native
- **UI组件库**：React Native Paper
- **状态管理**：React Context API
- **导航系统**：React Navigation
- **网络请求**：Axios

### 后端技术栈

- **API框架**：Python FastAPI
- **数据库**：SQLite (开发环境)
- **ORM**：SQLAlchemy
- **异步支持**：基于asyncio的异步API

## 项目结构

```
财知道/
├── frontend/              # 前端React Native应用
│   ├── src/               # 源代码
│   ├── __tests__/         # 测试文件
│   └── README.md          # 前端文档
├── backend/               # 后端FastAPI服务
│   ├── app/               # API应用
│   ├── tests/             # 测试文件
│   └── README.md          # 后端文档
└── README.md              # 项目总体文档(本文件)
```

## 测试

本项目包含前后端的自动化测试套件:

### 后端测试

```bash
cd backend
python run_tests.py
```

### 前端测试

```bash
cd frontend
npm test
```

## 前后端集成测试 (2024-03-21)

### API 集成测试结果

1. API 状态检查
   - 端点: `/api/status`
   - 状态: ✅ 成功
   - 响应: 返回正确的状态信息

2. 学习内容 API
   - 端点: `/api/learning`
   - 状态: ✅ 成功
   - 响应: 返回学习内容数据

3. 新闻 API
   - 端点: `/api/news`
   - 状态: ✅ 成功
   - 响应: 返回多条测试新闻数据
   - 数据格式: 包含标题、摘要、来源、发布日期、分类等信息

4. 问题 API
   - 端点: `/api/questions`
   - 状态: ✅ 成功
   - 响应: 返回空数组（符合预期，尚未添加问题数据）

### 测试环境
- 前端: React Native
- 后端: FastAPI (运行在 http://localhost:8000)
- 测试工具: Node.js + node-fetch

### 下一步计划
1. 添加问题数据到测试环境
2. 实现更多API端点的测试
3. 添加错误处理测试用例
4. 实现端到端测试 

./deploy.sh -- 前台运行
./deploy.sh --background 后台运行
tail -f deploy.log 查看日志
pkill -f "uvicorn|npm start|expo" 停止服务

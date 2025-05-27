# 财知道后端API

财知道是一个面向财经小白的移动端应用，旨在通过简洁易懂的内容帮助用户理解基础财经知识，获取实时财经新闻并解答常见财经问题。本仓库包含了财知道的后端API实现。

## 功能特点

- **基础知识学习**：提供分级别的财经知识，包括基金、ETF、开户等基础知识
- **财经新闻**：实时财经新闻展示，每篇新闻配有AI解读
- **问题解答**：常见财经问题解答和智能AI聊天功能
- **全局搜索**：跨模块搜索功能，帮助用户快速找到所需内容

## 技术栈

- **后端框架**：Python FastAPI
- **数据库**：SQLite (开发环境) / 可扩展至PostgreSQL等生产数据库
- **异步支持**：基于asyncio的异步API实现
- **数据模型**：SQLAlchemy ORM
- **API文档**：自动生成的Swagger/OpenAPI文档
- **测试工具**：pytest和pytest-asyncio

## API概览

### 学习内容 API

- `GET /api/learning` - 获取学习内容列表
- `GET /api/learning/{id}` - 获取特定学习内容详情
- `POST /api/learning` - 创建新的学习内容
- `PUT /api/learning/{id}` - 更新现有学习内容
- `DELETE /api/learning/{id}` - 删除学习内容
- `GET /api/learning/search/{keyword}` - 搜索学习内容

### 新闻 API

- `GET /api/news` - 获取新闻列表
- `GET /api/news/{id}` - 获取新闻详情
- `GET /api/news/search/{keyword}` - 搜索新闻

### 问答 API

- `GET /api/questions` - 获取问题列表
- `GET /api/questions/{id}` - 获取问题详情
- `GET /api/questions/search/{keyword}` - 搜索问题
- `GET /api/questions/related/{id}` - 获取相关问题

### 搜索 API

- `POST /api/search` - 全局搜索（跨学习内容、新闻和问题）

### 聊天 API

- `POST /api/chat` - AI聊天功能

## 安装与运行

### 前提条件

- Python 3.8+
- pip (Python包管理工具)

### 安装步骤

1. 克隆仓库

```bash
git clone <仓库地址>
cd 财知道/backend
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 初始化数据库 (可选，首次运行时会自动创建)

```bash
python migrate.py
```

4. 运行服务器

```bash
uvicorn app.main:app --reload
```

服务器将在 http://localhost:8000 启动，API文档可在 http://localhost:8000/docs 访问。

## 测试

运行测试:

```bash
python run_tests.py
```

如果测试中出现索引问题，可以运行修复脚本:

```bash
python fix_models.py
```

## 项目结构

```
backend/
├── app/                # 主应用目录
│   ├── api/            # API路由
│   ├── core/           # 核心配置
│   ├── models/         # 数据模型
│   │   ├── db/         # 数据库模型
│   ├── services/       # 业务逻辑服务
│   └── main.py         # 应用入口
├── data/               # 示例数据
├── docs/               # 文档目录
│   └── xueqiu_api.md   # 雪球API使用文档
├── tests/              # 测试目录
├── requirements.txt    # 依赖列表
├── migrate.py          # 数据库迁移脚本
├── run_tests.py        # 测试运行脚本
├── test_xueqiu_api.py  # 雪球API测试脚本
└── README.md           # 本文档
```

## 开发指南

### 添加新API端点

1. 在 `app/api/` 目录下创建或修改路由文件
2. 在 `app/models/db/` 目录下添加所需数据模型
3. 在 `app/services/` 目录下实现业务逻辑
4. 更新测试用例

### 外部API集成

项目已集成雪球财经新闻API，提供实时财经新闻获取功能：

1. 雪球API配置
   - 通过环境变量`XUEQIU_API_ENABLED`启用
   - 需要设置`XUEQIU_COOKIE`用于接口认证

2. 新闻获取方式
   - 自动定期获取：启动服务后自动运行
   - 手动触发获取：通过API端点手动获取最新新闻
   
3. 详细文档
   - 查看[雪球API集成文档](docs/xueqiu_api.md)了解详细信息

### 数据模型修改

如果修改了数据模型结构，请确保:

1. 更新相关 Pydantic 模型
2. 运行迁移脚本更新数据库结构
3. 更新相关测试用例

## 故障排除与调试指南

### 解决常见的500错误

后端可能遇到的500错误主要源于以下几个方面：

1. **SQLAlchemy异步ORM问题**
   - 症状：API返回500错误，日志显示SQLAlchemy相关异常
   - 解决方案：
     - 使用同步SQL实现替代异步ORM
     - 检查模型定义中是否添加了`__table_args__ = {'extend_existing': True}`
     - 验证连接池配置是否合理

2. **模块导入错误**
   - 症状：`ModuleNotFoundError: No module named 'app'`
   - 解决方案：
     ```bash
     # 创建setup.py文件
     from setuptools import setup, find_packages
     setup(name="app", packages=find_packages())
     
     # 安装本地包
     pip install -e .
     ```

3. **Greenlet兼容性问题**
   - 症状：`ImportError: cannot import name '_green_dummymodule'`
   - 解决方案：
     ```bash
     pip install greenlet==2.0.2
     ```

### 调试工具与方法

1. **数据库连接测试脚本**

   ```python
   # db_test.py
   from app.db.database import engine
   import asyncio
   
   async def test_db_connection():
       try:
           conn = await engine.connect()
           print("数据库连接成功!")
           await conn.close()
       except Exception as e:
           print(f"数据库连接失败: {e}")
   
   if __name__ == "__main__":
       asyncio.run(test_db_connection())
   ```

2. **API端点调试脚本**

   ```python
   # api_test.py
   import requests
   import json
   
   def test_endpoint(endpoint, method="GET", data=None):
       url = f"http://localhost:8000{endpoint}"
       print(f"测试 {method} {url}")
       
       if method == "GET":
           response = requests.get(url)
       else:
           response = requests.post(url, json=data)
           
       print(f"状态码: {response.status_code}")
       try:
           print(json.dumps(response.json(), ensure_ascii=False, indent=2))
       except:
           print(response.text)
       print("-" * 50)
       
   if __name__ == "__main__":
       test_endpoint("/api/learning")
       test_endpoint("/api/news")
       test_endpoint("/api/questions")
       test_endpoint("/api/search", "POST", {"query": "基金"})
   ```

### 异步与同步API解决方案

为解决异步ORM相关的500错误，我们开发了两种解决方案：

1. **单端点同步实现**
   - 文件: `fix_learning_sync.py`
   - 功能: 提供学习内容API的同步SQL实现
   - 用法:
     ```python
     # 在app/main.py中添加路由
     from app.api import fix_learning_sync
     app.include_router(fix_learning_sync.router)
     ```

2. **完整同步API服务**
   - 文件: `sync_api_all.py`
   - 功能: 提供所有API端点的同步SQL实现
   - 用法:
     ```bash
     # 启动同步API服务器（默认端口8001）
     python sync_api_all.py
     ```

### 同步SQL实现示例

将异步ORM代码转换为同步SQL查询的示例：

```python
# 异步ORM版本
async def get_learning_items():
    async with async_session() as session:
        result = await session.execute(select(LearningModel))
        items = result.scalars().all()
        return [item.to_dict() for item in items]

# 同步SQL版本
def get_learning_items_sync():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM learning"))
        items = []
        for row in result:
            item_dict = dict(row)
            # 处理JSON字段
            if 'tags' in item_dict and item_dict['tags']:
                item_dict['tags'] = json.loads(item_dict['tags'])
            items.append(item_dict)
        return items
```

## 贡献

欢迎提交问题报告或功能建议!

## 许可证

[项目许可证] 
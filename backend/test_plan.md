# 财知道后端测试计划

本文档提供了财知道后端API的分步测试指南，确保所有功能按预期工作。

## 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 确保数据库正确配置
python fix_models.py
```

## 2. 自动化测试套件

运行完整的自动化测试套件：

```bash
python run_tests.py
```

## 3. 模块化功能测试

### 3.1 数据库连接测试

```bash
# 运行数据库连接测试
pytest tests/test_database.py -v
```

### 3.2 学习内容API测试

```bash
# 运行学习内容API测试
pytest tests/test_learning_api.py -v
```

检查要点：
- 是否能成功获取学习内容列表
- 是否能通过ID获取特定学习内容
- 分页功能是否正常
- 筛选功能是否正常

### 3.3 新闻API测试

```bash
# 运行新闻API测试
pytest tests/test_news_api.py -v
```

检查要点：
- 是否能成功获取新闻列表
- 是否能通过ID获取特定新闻详情
- 新闻分类筛选是否正常
- 分页功能是否正常

### 3.4 问答API测试

```bash
# 运行问答API测试
pytest tests/test_questions_api.py -v
```

检查要点：
- 是否能成功获取问题列表
- 是否能通过ID获取特定问题详情
- 相关问题推荐是否正常

### 3.5 搜索API测试

```bash
# 运行搜索API测试
pytest tests/test_search_api.py -v
```

检查要点：
- 跨模块搜索功能是否正常
- 按关键词搜索是否返回预期结果
- 按分类过滤搜索结果是否正常

### 3.6 聊天API测试

```bash
# 运行聊天API测试
pytest tests/test_chat_api.py -v
```

检查要点：
- 是否能成功向AI发送消息并获取回复
- 响应时间是否在可接受范围内

## 4. 手动API测试

启动开发服务器：

```bash
uvicorn app.main:app --reload
```

### 4.1 使用Swagger UI测试

访问 http://localhost:8000/docs 使用Swagger UI进行交互式API测试：

1. 展开各个API端点
2. 点击"Try it out"
3. 填写必要参数
4. 执行请求并验证响应

### 4.2 使用Postman或curl测试

准备包含以下测试的Postman集合或curl命令：

#### 学习内容测试
```bash
# 获取学习内容列表
curl -X GET "http://localhost:8000/api/learning?page=1&limit=10" -H "accept: application/json"

# 获取特定学习内容
curl -X GET "http://localhost:8000/api/learning/1" -H "accept: application/json"
```

#### 新闻测试
```bash
# 获取新闻列表
curl -X GET "http://localhost:8000/api/news?page=1&limit=10" -H "accept: application/json"

# 获取特定新闻
curl -X GET "http://localhost:8000/api/news/1" -H "accept: application/json"
```

#### 问题测试
```bash
# 获取问题列表
curl -X GET "http://localhost:8000/api/questions?page=1&limit=10" -H "accept: application/json"

# 获取特定问题
curl -X GET "http://localhost:8000/api/questions/1" -H "accept: application/json"
```

#### 搜索测试
```bash
# 搜索"基金"相关内容
curl -X POST "http://localhost:8000/api/search" -H "accept: application/json" -H "Content-Type: application/json" -d '{"query":"基金","categories":[]}'
```

#### 聊天测试
```bash
# 测试AI聊天
curl -X POST "http://localhost:8000/api/chat" -H "accept: application/json" -H "Content-Type: application/json" -d '{"message":"什么是股票?"}'
```

## 5. 性能测试

对关键API进行负载测试：

```bash
# 使用ApacheBench对关键API进行简单负载测试
ab -n 100 -c 10 http://localhost:8000/api/learning
ab -n 100 -c 10 http://localhost:8000/api/news
```

## 6. 测试后清理

```bash
# 清理测试数据（如果需要）
python clean_test_data.py
```

## 测试报告模板

| API | 状态 | 响应时间 | 问题描述 |
|-----|------|----------|----------|
| GET /api/learning | ✅/❌ | xxx ms | |
| GET /api/learning/{id} | ✅/❌ | xxx ms | |
| GET /api/news | ✅/❌ | xxx ms | |
| GET /api/news/{id} | ✅/❌ | xxx ms | |
| GET /api/questions | ✅/❌ | xxx ms | |
| GET /api/questions/{id} | ✅/❌ | xxx ms | |
| POST /api/search | ✅/❌ | xxx ms | |
| POST /api/chat | ✅/❌ | xxx ms | | 
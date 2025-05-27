# 财知道后端数据模块

本目录包含"财知道"应用的JSON格式数据文件，作为MVP阶段的数据存储方案。

## 数据文件说明

### 学习内容数据

**文件**: `learning_data.json`

**数据结构**:
```json
[
  {
    "id": "learn-001",                              // 唯一标识符
    "title": "什么是基金？基金入门指南",              // 标题
    "shortDescription": "了解基金的基本概念...",      // 简短描述
    "fullContent": "# 什么是基金？基金入门指南...",   // 完整内容(Markdown格式)
    "difficulty": "beginner",                       // 难度级别：beginner/intermediate/advanced
    "tags": ["基金", "理财入门", "投资基础"],         // 标签
    "nextSteps": ["learn-002", "learn-004"]         // 推荐后续学习(可选)
  },
  // 更多学习内容...
]
```

**主要字段**:
- `id`: 学习内容的唯一标识符，用于查询特定内容
- `title`: 学习内容的标题
- `shortDescription`: 简短描述，用于列表展示
- `fullContent`: 完整内容，使用Markdown格式
- `difficulty`: 难度级别，分为入门(beginner)、进阶(intermediate)和高级(advanced)
- `tags`: 标签数组，用于分类和搜索
- `nextSteps`: 推荐的后续学习ID数组(可选)

### 新闻数据

**文件**: `news_data.json`

**数据结构**:
```json
[
  {
    "id": "news-001",                                // 唯一标识符
    "title": "央行下调MLF利率至2.3%，释放利好信号",    // 新闻标题
    "summary": "中国人民银行今日宣布下调...",          // 新闻摘要
    "content": "# 央行下调MLF利率至2.3%...",          // 完整内容(Markdown格式)
    "aiExplanation": "这个新闻说的是央行降低了...",     // AI对新闻的通俗解释
    "date": "2023-08-10",                           // 发布日期
    "source": "经济日报",                             // 新闻来源
    "imageUrl": "https://example.com/news1.jpg",     // 配图URL
    "category": "宏观经济",                           // 新闻分类
    "tags": ["央行", "利率", "货币政策", "经济刺激"]    // 标签
  },
  // 更多新闻...
]
```

**主要字段**:
- `id`: 新闻的唯一标识符
- `title`: 新闻标题
- `summary`: 新闻摘要，用于列表展示
- `content`: 完整新闻内容，使用Markdown格式
- `aiExplanation`: 面向财经小白的AI解读
- `date`: 发布日期，格式为YYYY-MM-DD
- `source`: 新闻来源
- `imageUrl`: 新闻配图URL
- `category`: 新闻分类，用于筛选
- `tags`: 标签数组，用于分类和搜索

### 问答数据

**文件**: `questions_data.json`

**数据结构**:
```json
[
  {
    "id": "q-001",                                  // 唯一标识符
    "question": "什么是"年化收益率"？如何计算？",      // 问题
    "answerPreview": "年化收益率是将投资的收益率...",  // 回答预览
    "fullAnswer": "# 什么是"年化收益率"？如何计算？...", // 完整回答(Markdown格式)
    "category": "基础概念",                           // 问题分类
    "relatedQuestions": ["q-002", "q-007"],         // 相关问题ID(可选)
    "tags": ["收益率", "财务计算", "投资基础"]          // 标签
  },
  // 更多问题...
]
```

**主要字段**:
- `id`: 问题的唯一标识符
- `question`: 问题内容
- `answerPreview`: 简短回答预览，用于列表展示
- `fullAnswer`: 完整回答，使用Markdown格式
- `category`: 问题分类，用于筛选
- `relatedQuestions`: 相关问题ID数组(可选)
- `tags`: 标签数组，用于分类和搜索

## 数据维护指南

### 添加新数据

1. **保持ID唯一**:
   - 学习内容使用`learn-XXX`格式
   - 新闻使用`news-XXX`格式
   - 问题使用`q-XXX`格式
   - XXX为递增的数字序号

2. **确保数据完整性**:
   - 填写所有必需字段
   - 验证关联ID存在(如nextSteps和relatedQuestions)

3. **内容格式**:
   - 正文内容使用Markdown格式
   - 标题使用`#`开头
   - 副标题使用`##`或`###`
   - 列表项使用`-`或数字
   - 表格使用Markdown表格语法

### 数据迁移计划

未来将从JSON文件迁移到数据库存储，计划步骤：

1. 设计数据库模式，保持与当前JSON结构一致
2. 创建数据迁移脚本，将JSON数据导入数据库
3. 修改API端点，从数据库读取数据而非JSON文件
4. 添加数据验证和错误处理机制

## 示例数据

每个文件已包含若干示例数据，可作为添加新数据的参考。目前数据量：

- 学习内容: 6个项目
- 新闻: 5条新闻
- 问答: 6个问题

## 备注

当前数据仅用于开发和演示，实际生产环境应考虑：

1. 实施更安全的数据存储方案
2. 添加用户生成内容的管理机制
3. 实现数据备份和恢复策略
4. 设计内容审核流程 
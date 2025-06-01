# 财知道前端工具模块

本目录包含"财知道"应用的工具函数和数据文件，用于管理应用的静态数据和共享功能。

## 数据文件概述

### dummyData.ts

**功能**: 统一导出所有数据模型和数据源，方便在组件中引用。

**内容**:
```typescript
// 导出所有数据类型和数据源
export * from './learningData';
export * from './newsData';
export * from './questionsData';
```

**用途**:
- 允许组件通过单一导入获取所有所需数据
- 简化导入语句，提高代码可读性

### learningData.ts

**功能**: 定义学习内容的数据模型和提供示例数据。

**数据模型**:
```typescript
export interface LearningItem {
  id: string;
  title: string;
  shortDescription: string;
  fullContent: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
  nextSteps?: string[];
}
```

**字段说明**:
- `id`: 唯一标识符
- `title`: 学习项目标题
- `shortDescription`: 简短描述
- `fullContent`: 完整内容（Markdown格式）
- `difficulty`: 难度级别（入门/进阶/高级）
- `tags`: 标签数组
- `nextSteps`: 推荐后续学习项目ID（可选）

**数据数量**: 6个学习项目

### newsData.ts

**功能**: 定义新闻内容的数据模型和提供示例数据。

**数据模型**:
```typescript
export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  content: string;
  aiExplanation: string;
  date: string;
  source: string;
  imageUrl: string;
  category: string;
  tags: string[];
}
```

**字段说明**:
- `id`: 唯一标识符
- `title`: 新闻标题
- `summary`: 新闻摘要
- `content`: 完整内容（Markdown格式）
- `aiExplanation`: 面向小白的AI解释
- `date`: 发布日期
- `source`: 新闻来源
- `imageUrl`: 新闻图片URL
- `category`: 分类
- `tags`: 标签数组

**数据数量**: 5条新闻

### questionsData.ts

**功能**: 定义问答内容的数据模型和提供示例数据。

**数据模型**:
```typescript
export interface Question {
  id: string;
  question: string;
  answerPreview: string;
  fullAnswer: string;
  category: string;
  relatedQuestions?: string[];
  tags: string[];
}
```

**字段说明**:
- `id`: 唯一标识符
- `question`: 问题内容
- `answerPreview`: 答案预览
- `fullAnswer`: 完整答案（Markdown格式）
- `category`: 问题分类
- `relatedQuestions`: 相关问题ID数组（可选）
- `tags`: 标签数组

**数据数量**: 6个问题

## 使用方式

### 在组件中导入和使用数据

```jsx
// 导入所有数据类型和数据源
import { learningData, LearningItem } from '../utils/dummyData';

// 在组件中使用
const MyComponent = () => {
  // 获取前3条数据
  const topItems = learningData.slice(0, 3);
  
  return (
    <View>
      {topItems.map(item => (
        <Text key={item.id}>{item.title}</Text>
      ))}
    </View>
  );
};
```

### 数据过滤示例

```jsx
// 按难度过滤
const beginnerItems = learningData.filter(item => item.difficulty === 'beginner');

// 按关键词搜索
const searchResults = learningData.filter(item => 
  item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
  item.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
);
```

### 根据ID查找项目

```jsx
// 查找特定项目
const findItemById = (id) => {
  return learningData.find(item => item.id === id);
};

// 查找相关项目
const getRelatedItems = (relatedIds) => {
  return relatedIds
    .map(id => learningData.find(item => item.id === id))
    .filter(Boolean); // 过滤掉undefined结果
};
```

## 未来扩展

目前，数据直接存储在前端代码中作为开发阶段的解决方案。未来计划:

1. **API集成**: 
   - 替换静态数据为后端API调用
   - 添加数据获取、缓存和错误处理逻辑

2. **状态管理**:
   - 考虑添加Redux或Context API进行全局状态管理
   - 实现数据读取、更新和持久化

3. **工具函数**:
   - 添加日期格式化函数
   - 添加文本处理和搜索优化函数
   - 添加数据验证和转换函数

4. **本地存储**:
   - 实现用户偏好和历史记录的本地存储
   - 添加离线数据缓存功能

## 开发说明

扩展或修改数据文件时，请注意以下几点:

1. 保持数据结构的一致性
2. 确保所有必需字段都有有效值
3. 维护ID的唯一性
4. 验证关联ID的有效性（如nextSteps和relatedQuestions）
5. 确保Markdown格式内容的正确性 
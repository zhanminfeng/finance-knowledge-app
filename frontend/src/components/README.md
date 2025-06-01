# 财知道前端组件模块

本目录包含"财知道"应用的可复用组件，用于在不同页面中实现一致的功能和界面。

## 组件列表

### RecommendedLearning

显示推荐的学习内容卡片。

**文件**: `RecommendedLearning.tsx`

**功能**:
- 展示最多3个推荐学习内容
- 使用水平滚动列表布局
- 显示每个内容的难度标签、标题和简短描述
- 处理点击事件，导航到学习详情页

**Props**:
```typescript
interface RecommendedLearningProps {
  onPress: (item: LearningItem) => void;
}
```

**使用示例**:
```jsx
<RecommendedLearning 
  onPress={(item) => navigation.navigate('LearningDetail', { item })} 
/>
```

### LatestNews

显示最新财经新闻列表。

**文件**: `LatestNews.tsx`

**功能**:
- 展示最多3条最新新闻
- 每条新闻包含图片、标题、摘要、来源和日期
- 垂直列表布局
- 处理点击事件，导航到新闻详情页

**Props**:
```typescript
interface LatestNewsProps {
  onPress: (news: NewsItem) => void;
}
```

**使用示例**:
```jsx
<LatestNews 
  onPress={(news) => navigation.navigate('NewsDetail', { news })} 
/>
```

### InterestingQuestions

显示推荐的财经问题列表。

**文件**: `InterestingQuestions.tsx`

**功能**:
- 展示最多3个推荐问题
- 每个问题包含分类、问题内容和回答预览
- 垂直列表布局
- 处理点击事件，导航到问题详情页

**Props**:
```typescript
interface InterestingQuestionsProps {
  onPress: (question: Question) => void;
}
```

**使用示例**:
```jsx
<InterestingQuestions 
  onPress={(question) => navigation.navigate('QuestionDetail', { question })} 
/>
```

## 样式说明

所有组件采用一致的设计风格:

1. **卡片布局**:
   - 白色背景
   - 圆角边框
   - 轻微阴影效果

2. **难度标签**:
   - 入门(beginner): 浅绿色背景 (#e3fcef)
   - 进阶(intermediate): 浅黄色背景 (#fff8e1)
   - 高级(advanced): 浅红色背景 (#ffebee)

3. **文本层次**:
   - 标题: 16px, 粗体, #333
   - 描述/摘要: 12-14px, 常规, #666/#777
   - 次要信息(日期/来源): 12px, #999

4. **间距与对齐**:
   - 内边距(padding): 15px
   - 元素间距(margin): 5-10px
   - 左对齐文本

## 如何扩展

创建新组件时，请遵循以下准则:

1. **命名规范**:
   - 使用PascalCase命名组件文件和组件
   - 使用有意义的名称描述组件功能

2. **类型定义**:
   - 为所有props创建TypeScript接口
   - 进行适当的类型检查

3. **样式一致性**:
   - 遵循已有的样式指南
   - 使用StyleSheet创建样式
   - 保持与应用整体风格一致

4. **性能考虑**:
   - 适当使用React.memo()优化渲染
   - 避免不必要的重渲染
   - 长列表考虑使用列表虚拟化

## 开发状态

- [x] RecommendedLearning组件
- [x] LatestNews组件
- [x] InterestingQuestions组件
- [ ] 标签组件(计划)
- [ ] 搜索框组件(计划)
- [ ] 加载状态组件(计划) 
# 财知道前端应用

财知道是一个面向财经小白的移动端应用，旨在通过简洁易懂的内容帮助用户理解基础财经知识，获取实时财经新闻并解答常见财经问题。本仓库包含了财知道的前端React Native实现。

## 功能特点

- **首页推荐**: 智能推荐学习内容、最新财经新闻和感兴趣的问题
- **基础知识学习**: 分级别的财经知识，包括基金、ETF、开户等
- **财经新闻浏览**: 最新财经新闻展示，每篇新闻配有AI解读
- **财经问答**: 常见财经问题解答和AI聊天功能
- **全局搜索**: 跨模块搜索功能，快速找到所需内容
- **个性化推荐**: 根据用户浏览历史和兴趣推荐内容

## 技术栈

- **核心框架**: React Native 
- **状态管理**: React Context API / Redux
- **UI组件库**: React Native Paper
- **导航系统**: React Navigation
- **网络请求**: Axios
- **本地存储**: AsyncStorage
- **国际化**: i18next

## 屏幕与组件

### 主要屏幕

- **首页**: 显示推荐内容和最新内容
- **学习**: 按类别和难度展示财经学习内容
- **新闻**: 展示最新财经新闻
- **问答**: 提供常见问题解答和AI聊天功能
- **我的**: 个人设置和历史记录

### 核心组件

- **学习卡片**: 展示学习内容的卡片组件
- **新闻项**: 展示新闻摘要的项目组件
- **问答卡**: 问题和答案的卡片组件
- **AI聊天界面**: 与AI助手交互的聊天界面
- **搜索栏**: 全局搜索组件

## 安装与运行

### 前提条件

- Node.js 14+
- npm 或 yarn
- React Native CLI
- iOS或Android开发环境

### 安装步骤

1. 克隆仓库

```bash
git clone <仓库地址>
cd 财知道/frontend
```

2. 安装依赖

```bash
npm install
# 或
yarn install
```

3. 启动开发服务器

```bash
# 启动Metro打包器
npm start
# 或
yarn start
```

4. 运行应用

```bash
# iOS
npm run ios
# 或
yarn ios

# Android
npm run android
# 或
yarn android
```

## 项目结构

```
frontend/
├── src/
│   ├── assets/           # 静态资源(图片、字体等)
│   ├── components/       # 可复用组件
│   │   ├── common/       # 通用组件
│   │   ├── learning/     # 学习相关组件
│   │   ├── news/         # 新闻相关组件
│   │   └── questions/    # 问答相关组件
│   ├── navigation/       # 路由和导航配置
│   ├── screens/          # 应用屏幕
│   │   ├── home/         # 首页相关屏幕
│   │   ├── learning/     # 学习模块屏幕
│   │   ├── news/         # 新闻模块屏幕
│   │   ├── questions/    # 问答模块屏幕
│   │   └── profile/      # 个人信息模块屏幕
│   ├── services/         # API服务
│   ├── context/          # React Context状态管理
│   ├── hooks/            # 自定义Hooks
│   ├── utils/            # 工具函数
│   ├── theme/            # 主题和样式配置
│   └── App.js            # 应用入口
├── android/              # Android平台特定代码
├── ios/                  # iOS平台特定代码
├── __tests__/            # 测试文件
├── package.json          # 依赖和脚本配置
└── README.md             # 本文档
```

## 开发指南

### 添加新屏幕

1. 在 `src/screens/` 目录下创建新的屏幕组件
2. 在 `src/navigation/` 下添加路由配置
3. 添加必要的服务调用或状态管理

### 添加新组件

1. 在 `src/components/` 目录下创建新组件
2. 确保组件遵循项目的样式和主题规范
3. 为复杂组件添加适当的文档注释

### 状态管理

- 对于屏幕内的局部状态，使用React的useState和useEffect
- 对于跨组件的共享状态，使用React Context API
- 对于应用级别的状态，可以考虑使用Redux或MobX

## 样式指南

项目使用了主题化的样式系统，确保一致的视觉体验：

- 使用预定义的颜色变量而不是硬编码颜色值
- 遵循定义的间距和排版规范
- 优先使用Flexbox布局
- 确保组件在不同屏幕尺寸上的响应式表现

## 测试

运行测试:

```bash
npm test
# 或
yarn test
```

## 构建与发布

### iOS 构建

```bash
npm run build:ios
# 或
yarn build:ios
```

### Android 构建

```bash
npm run build:android
# 或
yarn build:android
```

## 贡献

欢迎提交问题报告或功能建议!

## 许可证

[项目许可证] 
# 财知道导航模块

本目录包含"财知道"应用的导航配置，使用React Navigation实现应用的页面导航和标签栏功能。

## 导航结构

应用使用嵌套的导航结构:

```
导航容器 (NavigationContainer)
└── 底部标签导航 (Tab Navigator)
    ├── 首页标签
    │   └── 首页堆栈导航 (Stack Navigator)
    │       ├── 首页
    │       ├── 学习详情页
    │       ├── 新闻详情页
    │       └── 问题详情页
    ├── 学习标签
    │   └── 学习堆栈导航 (Stack Navigator)
    │       ├── 学习列表页
    │       └── 学习详情页
    ├── 资讯标签
    │   └── 资讯堆栈导航 (Stack Navigator)
    │       ├── 新闻列表页
    │       └── 新闻详情页
    └── 问答标签
        └── 问答堆栈导航 (Stack Navigator)
            ├── 问题列表页
            ├── 问题详情页
            └── AI聊天页
```

## 实现文件

**文件**: `AppNavigator.tsx`

**主要组件**:

1. **堆栈导航器**:
   - HomeStack: 首页及其子页面
   - LearningStack: 学习模块及其子页面
   - NewsStack: 新闻模块及其子页面
   - QuestionsStack: 问答模块及其子页面

2. **底部标签导航器**:
   - 首页(Home)标签
   - 学习(Learning)标签
   - 资讯(News)标签
   - 问答(Questions)标签

## 导航配置

### 堆栈导航器

每个堆栈导航器定义了该功能模块内的页面路由:

```jsx
// 首页堆栈示例
const HomeStackNavigator = () => (
  <HomeStack.Navigator>
    <HomeStack.Screen 
      name="Home" 
      component={HomeScreen} 
      options={{ headerShown: false }}
    />
    <HomeStack.Screen 
      name="LearningDetail" 
      component={LearningDetailScreen} 
      options={{ title: '知识详情' }}
    />
    <HomeStack.Screen 
      name="NewsDetail" 
      component={NewsDetailScreen} 
      options={{ title: '新闻详情' }}
    />
    <HomeStack.Screen 
      name="QuestionDetail" 
      component={QuestionDetailScreen} 
      options={{ title: '问题详情' }}
    />
  </HomeStack.Navigator>
);
```

### 底部标签导航器

底部标签导航器整合了各个堆栈导航器:

```jsx
const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen 
          name="HomeTab" 
          component={HomeStackNavigator} 
          options={{
            tabBarLabel: '首页',
            headerShown: false,
            tabBarIcon: ({ focused }) => <TabIcon name="home" focused={focused} />,
          }}
        />
        {/* 其他标签页配置... */}
      </Tab.Navigator>
    </NavigationContainer>
  );
};
```

## 导航图标

使用自定义的`TabIcon`组件渲染标签页图标:

```jsx
const TabIcon = ({ name, focused }: { name: string; focused: boolean }) => (
  <View style={{ alignItems: 'center', justifyContent: 'center' }}>
    <Text style={{ 
      color: focused ? '#3498db' : '#999',
      fontSize: 24,
      marginBottom: 2,
    }}>
      {/* 简单的emoji作为图标，实际应用中应使用图标库 */}
      {name === 'home' ? '🏠' : 
       name === 'learning' ? '📚' : 
       name === 'news' ? '📰' : 
       name === 'questions' ? '❓' : '🔍'}
    </Text>
    <Text style={{ 
      color: focused ? '#3498db' : '#999',
      fontSize: 12,
    }}>
      {name === 'home' ? '首页' : 
       name === 'learning' ? '学习' : 
       name === 'news' ? '资讯' : 
       name === 'questions' ? '问答' : ''}
    </Text>
  </View>
);
```

## 导航样式

所有标签页使用一致的样式配置:

```jsx
<Tab.Navigator
  screenOptions={{
    tabBarStyle: {
      height: 60,
      paddingBottom: 5,
    },
    tabBarActiveTintColor: '#3498db',
    tabBarInactiveTintColor: '#999',
  }}
>
```

## 导航处理

### 页面间导航

使用`navigation.navigate`方法在页面间导航:

```jsx
// 导航到详情页示例
navigation.navigate('LearningDetail', { item })
```

### 参数传递

通过路由参数传递数据:

```jsx
// 发送参数
navigation.navigate('QuestionDetail', { question: item })

// 接收参数
const { question } = route.params;
```

### 嵌套导航

从一个堆栈导航到另一个堆栈:

```jsx
// 从问题详情页导航到AI聊天页
navigation.navigate('AiChat', { initialQuestion: `关于"${question.question}"，我想进一步了解...` })
```

## 未来扩展

计划添加的导航功能:

1. **深层链接**: 支持从应用外直接打开特定页面
2. **身份验证流**: 添加登录/注册导航流程
3. **抽屉导航**: 添加侧边抽屉导航，用于设置和用户相关功能
4. **自定义导航过渡**: 增强页面切换动画效果
5. **导航状态持久化**: 保存导航状态，便于应用重启后恢复 
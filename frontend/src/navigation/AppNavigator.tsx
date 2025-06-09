import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Text, View } from 'react-native';
import { Ionicons, MaterialCommunityIcons, FontAwesome } from '@expo/vector-icons';

// 导入屏幕
import HomeScreen from '../screens/HomeScreen';
import LearningScreen from '../screens/LearningScreen';
import LearningDetailScreen from '../screens/LearningDetailScreen';
import NewsScreen from '../screens/NewsScreen';
import NewsDetailScreen from '../screens/NewsDetailScreen';
import QuestionsScreen from '../screens/QuestionsScreen';
import QuestionDetailScreen from '../screens/QuestionDetailScreen';
import AiChatScreen from '../screens/AiChatScreen';

// 创建导航堆栈
const HomeStack = createStackNavigator();
const LearningStack = createStackNavigator();
const NewsStack = createStackNavigator();
const QuestionsStack = createStackNavigator();

// 堆栈导航器
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

const LearningStackNavigator = () => (
  <LearningStack.Navigator>
    <LearningStack.Screen 
      name="Learning" 
      component={LearningScreen} 
      options={{ headerShown: false }}
    />
    <LearningStack.Screen 
      name="LearningDetail" 
      component={LearningDetailScreen} 
      options={{ title: '知识详情' }}
    />
  </LearningStack.Navigator>
);

const NewsStackNavigator = () => (
  <NewsStack.Navigator>
    <NewsStack.Screen 
      name="News" 
      component={NewsScreen} 
      options={{ headerShown: false }}
    />
    <NewsStack.Screen 
      name="NewsDetail" 
      component={NewsDetailScreen} 
      options={{ title: '新闻详情' }}
    />
  </NewsStack.Navigator>
);

const QuestionsStackNavigator = () => (
  <QuestionsStack.Navigator>
    <QuestionsStack.Screen 
      name="Questions" 
      component={QuestionsScreen} 
      options={{ headerShown: false }}
    />
    <QuestionsStack.Screen 
      name="QuestionDetail" 
      component={QuestionDetailScreen} 
      options={{ title: '问题详情' }}
    />
    <QuestionsStack.Screen 
      name="AiChat" 
      component={AiChatScreen} 
      options={{ title: 'AI助手' }}
    />
  </QuestionsStack.Navigator>
);

// Tab 图标组件
const TabIcon = ({ name, focused }: { name: string; focused: boolean }) => {
  let icon;
  if (name === 'home') {
    icon = <Ionicons name="home" size={24} color={focused ? '#3498db' : '#999'} />;
  } else if (name === 'learning') {
    icon = <MaterialCommunityIcons name="book-open-variant" size={24} color={focused ? '#3498db' : '#999'} />;
  } else if (name === 'news') {
    icon = <Ionicons name="newspaper" size={24} color={focused ? '#3498db' : '#999'} />;
  } else if (name === 'questions') {
    icon = <FontAwesome name="question-circle" size={24} color={focused ? '#3498db' : '#999'} />;
  } else {
    icon = <Ionicons name="search" size={24} color={focused ? '#3498db' : '#999'} />;
  }
  return (
    <View style={{ alignItems: 'center', justifyContent: 'center' }}>
      {icon}
      {/* 移除这里的Text组件，因为tabBarLabel已经提供了文字 */}
    </View>
  );
};

// 创建底部标签导航器
const Tab = createBottomTabNavigator();

const AppNavigator = () => {
  return (
    <NavigationContainer>
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
        <Tab.Screen 
          name="HomeTab" 
          component={HomeStackNavigator} 
          options={{
            tabBarLabel: '首页',
            headerShown: false,
            tabBarIcon: ({ focused }) => <TabIcon name="home" focused={focused} />,
          }}
        />
        <Tab.Screen 
          name="LearningTab" 
          component={LearningStackNavigator} 
          options={{
            tabBarLabel: '学习',
            headerShown: false,
            tabBarIcon: ({ focused }) => <TabIcon name="learning" focused={focused} />,
          }}
        />
        <Tab.Screen 
          name="NewsTab" 
          component={NewsStackNavigator} 
          options={{
            tabBarLabel: '资讯',
            headerShown: false,
            tabBarIcon: ({ focused }) => <TabIcon name="news" focused={focused} />,
          }}
        />
        <Tab.Screen 
          name="QuestionsTab" 
          component={QuestionsStackNavigator} 
          options={{
            tabBarLabel: '问答',
            headerShown: false,
            tabBarIcon: ({ focused }) => <TabIcon name="questions" focused={focused} />,
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
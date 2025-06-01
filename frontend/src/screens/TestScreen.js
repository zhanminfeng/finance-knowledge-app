import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Card, Button, Divider, List, Badge } from 'react-native-paper';
import * as apiTest from '../utils/apiTest';

/**
 * API测试界面
 * 用于测试前端与后端API的连接
 */
const TestScreen = () => {
  // 测试结果状态
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState({});
  const [expanded, setExpanded] = useState({});

  // 运行特定API测试
  const runTest = async (testName, testFunction) => {
    setLoading(prev => ({ ...prev, [testName]: true }));
    try {
      const result = await testFunction();
      setResults(prev => ({ ...prev, [testName]: result }));
    } catch (error) {
      setResults(prev => ({ 
        ...prev, 
        [testName]: { 
          success: false, 
          error, 
          message: '测试执行失败' 
        } 
      }));
    } finally {
      setLoading(prev => ({ ...prev, [testName]: false }));
    }
  };

  // 运行所有测试
  const runAllTests = async () => {
    setLoading(prev => ({ 
      ...prev, 
      all: true,
      apiStatus: true,
      learning: true,
      news: true,
      questions: true,
      search: true,
      chat: true
    }));
    
    try {
      const result = await apiTest.runAllApiTests();
      setResults(prev => ({ 
        ...prev, 
        all: result,
        apiStatus: result.results.apiStatus,
        learning: result.results.learning,
        news: result.results.news,
        questions: result.results.questions,
        search: result.results.search,
        chat: result.results.chat
      }));
    } catch (error) {
      setResults(prev => ({ 
        ...prev, 
        all: { 
          success: false, 
          error, 
          message: '测试执行失败' 
        } 
      }));
    } finally {
      setLoading(prev => ({ 
        ...prev, 
        all: false,
        apiStatus: false,
        learning: false,
        news: false,
        questions: false,
        search: false,
        chat: false
      }));
    }
  };

  // 切换展开/折叠测试详情
  const toggleExpanded = (key) => {
    setExpanded(prev => ({ ...prev, [key]: !prev[key] }));
  };

  // 渲染测试结果状态徽章
  const renderStatusBadge = (status) => {
    if (status === undefined) return null;
    
    return (
      <Badge 
        style={{ 
          backgroundColor: status ? '#4CAF50' : '#F44336',
          color: 'white',
          fontWeight: 'bold'
        }}
      >
        {status ? '成功' : '失败'}
      </Badge>
    );
  };

  // 渲染测试项
  const renderTestItem = (title, key, testFunction) => {
    const result = results[key];
    const isLoading = loading[key];
    const isExpanded = expanded[key];
    
    return (
      <List.Item
        title={title}
        right={() => (
          <View style={styles.itemRight}>
            {isLoading ? (
              <ActivityIndicator size="small" color="#6200ee" />
            ) : (
              renderStatusBadge(result?.success)
            )}
          </View>
        )}
        onPress={() => toggleExpanded(key)}
        left={props => <List.Icon {...props} icon="api" />}
        description={result?.message || '未测试'}
        expanded={isExpanded}
        onLongPress={() => runTest(key, testFunction)}
      />
    );
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Title title="财知道API测试" subtitle="测试前端与后端API连接" />
        <Card.Content>
          <Text style={styles.instructions}>
            点击测试项查看详情，长按单项执行测试
          </Text>
          
          <Button 
            mode="contained" 
            onPress={runAllTests} 
            loading={loading.all}
            style={styles.button}
          >
            运行所有测试
          </Button>
          
          <Divider style={styles.divider} />
          
          <List.Section>
            <List.Subheader>API状态测试</List.Subheader>
            {renderTestItem('API状态', 'apiStatus', apiTest.testApiStatus)}
            {expanded.apiStatus && results.apiStatus && (
              <Card style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.jsonText}>
                    {JSON.stringify(results.apiStatus.data, null, 2)}
                  </Text>
                </Card.Content>
              </Card>
            )}
            
            <List.Subheader>功能API测试</List.Subheader>
            {renderTestItem('学习内容API', 'learning', apiTest.testLearningApi)}
            {expanded.learning && results.learning && (
              <Card style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.jsonText}>
                    {JSON.stringify(results.learning.data, null, 2)}
                  </Text>
                </Card.Content>
              </Card>
            )}
            
            {renderTestItem('新闻API', 'news', apiTest.testNewsApi)}
            {expanded.news && results.news && (
              <Card style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.jsonText}>
                    {JSON.stringify(results.news.data, null, 2)}
                  </Text>
                </Card.Content>
              </Card>
            )}
            
            {renderTestItem('问答API', 'questions', apiTest.testQuestionsApi)}
            {expanded.questions && results.questions && (
              <Card style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.jsonText}>
                    {JSON.stringify(results.questions.data, null, 2)}
                  </Text>
                </Card.Content>
              </Card>
            )}
            
            {renderTestItem('搜索API', 'search', apiTest.testSearchApi)}
            {expanded.search && results.search && (
              <Card style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.jsonText}>
                    {JSON.stringify(results.search.data, null, 2)}
                  </Text>
                </Card.Content>
              </Card>
            )}
            
            {renderTestItem('聊天API', 'chat', apiTest.testChatApi)}
            {expanded.chat && results.chat && (
              <Card style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.jsonText}>
                    {JSON.stringify(results.chat.data, null, 2)}
                  </Text>
                </Card.Content>
              </Card>
            )}
          </List.Section>
        </Card.Content>
      </Card>
      
      <Card style={styles.card}>
        <Card.Title title="测试结果汇总" />
        <Card.Content>
          {results.all ? (
            <View style={styles.summaryContainer}>
              <Text style={styles.summaryText}>
                总体状态: {results.all.allSuccess ? '所有测试通过' : '部分测试失败'}
              </Text>
              <View style={styles.badgesContainer}>
                <View style={styles.badgeItem}>
                  <Text>API状态:</Text>
                  {renderStatusBadge(results.apiStatus?.success)}
                </View>
                <View style={styles.badgeItem}>
                  <Text>学习内容:</Text>
                  {renderStatusBadge(results.learning?.success)}
                </View>
                <View style={styles.badgeItem}>
                  <Text>新闻:</Text>
                  {renderStatusBadge(results.news?.success)}
                </View>
                <View style={styles.badgeItem}>
                  <Text>问答:</Text>
                  {renderStatusBadge(results.questions?.success)}
                </View>
                <View style={styles.badgeItem}>
                  <Text>搜索:</Text>
                  {renderStatusBadge(results.search?.success)}
                </View>
                <View style={styles.badgeItem}>
                  <Text>聊天:</Text>
                  {renderStatusBadge(results.chat?.success)}
                </View>
              </View>
            </View>
          ) : (
            <Text>尚未运行测试</Text>
          )}
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  button: {
    marginTop: 16,
  },
  divider: {
    marginVertical: 16,
  },
  instructions: {
    marginBottom: 8,
    fontStyle: 'italic',
  },
  itemRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  resultCard: {
    marginHorizontal: 16,
    marginBottom: 16,
    backgroundColor: '#f9f9f9',
  },
  jsonText: {
    fontFamily: 'monospace',
    fontSize: 12,
  },
  summaryContainer: {
    marginTop: 8,
  },
  summaryText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  badgesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  badgeItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
    marginBottom: 8,
  },
});

export default TestScreen; 
import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, SafeAreaView, ActivityIndicator } from 'react-native';
import RecommendedLearning from '../components/RecommendedLearning';
import LatestNews from '../components/LatestNews';
import InterestingQuestions from '../components/InterestingQuestions';
import api from '../utils/api';

const HomeScreen = ({ navigation }: any) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        // 这里可以添加实际的数据加载逻辑
        await Promise.all([
          api.learning.getAll(),
          api.news.getAll(),
          api.questions.getAll(),
        ]);
      } catch (err) {
        console.error('加载数据失败:', err);
        setError('加载数据失败，请重试');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator testID="loading-indicator" size="large" color="#3498db" />
        </View>
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity 
            style={styles.retryButton}
            onPress={() => {
              setLoading(true);
              setError(null);
              // 重新加载数据
              loadData();
            }}
          >
            <Text style={styles.retryButtonText}>重试</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView testID="home-content">
        <View style={styles.header}>
          <Text style={styles.headerTitle}>财知道</Text>
          <Text style={styles.headerSubtitle}>让财经知识更简单</Text>
        </View>
        
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>今日推荐学习</Text>
          <RecommendedLearning onPress={(item) => 
            navigation.navigate('LearningDetail', { item })
          } />
          <TouchableOpacity 
            style={styles.moreButton}
            onPress={() => navigation.navigate('Learning')}
          >
            <Text style={styles.moreButtonText}>查看更多</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>最新财经新闻</Text>
          <LatestNews onPress={(news) => 
            navigation.navigate('NewsDetail', { news })
          } />
          <TouchableOpacity 
            style={styles.moreButton}
            onPress={() => navigation.navigate('News')}
          >
            <Text style={styles.moreButtonText}>查看更多</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>你可能感兴趣的问题</Text>
          <InterestingQuestions onPress={(question) => 
            navigation.navigate('QuestionDetail', { question })
          } />
          <TouchableOpacity 
            style={styles.moreButton}
            onPress={() => navigation.navigate('Questions')}
          >
            <Text style={styles.moreButtonText}>查看更多</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9f9f9',
  },
  header: {
    padding: 20,
    backgroundColor: '#3498db',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 5,
  },
  section: {
    padding: 15,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  moreButton: {
    alignSelf: 'flex-end',
    paddingVertical: 5,
    paddingHorizontal: 10,
  },
  moreButtonText: {
    color: '#3498db',
    fontWeight: '500',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    color: '#e74c3c',
    marginBottom: 10,
    textAlign: 'center',
  },
  retryButton: {
    backgroundColor: '#3498db',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 5,
  },
  retryButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
});

export default HomeScreen; 
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, Image, ActivityIndicator } from 'react-native';
import api from '../utils/api';
import { NewsItem } from '../utils/types';

interface LatestNewsProps {
  onPress: (news: NewsItem) => void;
}

const LatestNews = ({ onPress }: LatestNewsProps) => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const response = await api.news.getAll();
        // 添加数据转换，确保所有必要的字段都存在
        const processedNews = response.items.slice(0, 3).map(item => ({
          ...item,
          tags: item.tags || [],
          content: item.content || '',
          aiExplanation: item.aiExplanation || '',
          category: item.category || '未分类'
        }));
        setNews(processedNews);
        setError(null);
      } catch (err) {
        console.error('获取新闻失败:', err);
        setError('无法加载新闻数据');
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  const renderItem = ({ item }: { item: NewsItem }) => (
    <TouchableOpacity 
      style={styles.newsItem}
      onPress={() => onPress(item)}
    >
      <View style={styles.newsContent}>
        <Text style={styles.newsTitle} numberOfLines={2}>{item.title}</Text>
        <Text style={styles.newsSummary} numberOfLines={2}>{item.summary}</Text>
        <View style={styles.newsFooter}>
          <Text style={styles.newsSource}>{item.source}</Text>
          <Text style={styles.newsDate}>{item.date}</Text>
        </View>
      </View>
      <View style={styles.newsImageContainer}>
        <Image 
          source={{ uri: item.imageUrl }} 
          style={styles.newsImage}
          resizeMode="cover"
        />
      </View>
    </TouchableOpacity>
  );

  return (
    <FlatList
      data={news}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      scrollEnabled={false}
      contentContainerStyle={styles.listContainer}
    />
  );
};

const styles = StyleSheet.create({
  listContainer: {
    paddingVertical: 5,
  },
  newsItem: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  newsContent: {
    flex: 1,
    marginRight: 10,
  },
  newsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#333',
  },
  newsSummary: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
    lineHeight: 20,
  },
  newsFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  newsSource: {
    fontSize: 12,
    color: '#999',
  },
  newsDate: {
    fontSize: 12,
    color: '#999',
  },
  newsImageContainer: {
    width: 90,
    height: 90,
    borderRadius: 8,
    overflow: 'hidden',
  },
  newsImage: {
    width: '100%',
    height: '100%',
  },
  loadingContainer: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  errorContainer: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  errorText: {
    color: 'red',
    fontSize: 14,
  }
});

export default LatestNews;
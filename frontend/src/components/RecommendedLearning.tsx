import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, ActivityIndicator } from 'react-native';
import api from '../utils/api';

interface LearningItem {
  id: string;
  title: string;
  shortDescription: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

interface RecommendedLearningProps {
  onPress: (item: LearningItem) => void;
}

const RecommendedLearning = ({ onPress }: RecommendedLearningProps) => {
  // 状态管理
  const [recommendedItems, setRecommendedItems] = useState<LearningItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 加载数据
  useEffect(() => {
    const fetchLearningData = async () => {
      try {
        setLoading(true);
        const response = await api.learning.getAll();
        // 获取全部内容并只使用前3个
        setRecommendedItems(response.items.slice(0, 3));
        setError(null);
      } catch (err) {
        console.error('获取学习内容失败:', err);
        setError('加载数据失败，请重试');
        // 在实际环境中可能需要降级到静态数据
      } finally {
        setLoading(false);
      }
    };

    fetchLearningData();
  }, []);

  // 加载中状态
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator testID="loading-indicator" size="large" color="#3498db" />
      </View>
    );
  }

  // 错误状态
  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity 
          style={styles.retryButton}
          onPress={() => {
            setLoading(true);
            setError(null);
            // 重新加载数据
            api.learning.getAll()
              .then(response => {
                setRecommendedItems(response.items.slice(0, 3));
                setLoading(false);
              })
              .catch(err => {
                console.error('重试获取学习内容失败:', err);
                setError('加载数据失败，请重试');
                setLoading(false);
              });
          }}
        >
          <Text style={styles.retryButtonText}>重试</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const renderItem = ({ item }: { item: LearningItem }) => (
    <TouchableOpacity 
      style={styles.itemContainer}
      onPress={() => onPress(item)}
      testID="learning-item"
    >
      <View style={[styles.difficultyBadge, 
        item.difficulty === 'beginner' ? styles.beginnerBadge : 
        item.difficulty === 'intermediate' ? styles.intermediateBadge : styles.advancedBadge
      ]}>
        <Text style={styles.difficultyText}>
          {item.difficulty === 'beginner' ? '入门' : 
           item.difficulty === 'intermediate' ? '进阶' : '高级'}
        </Text>
      </View>
      <Text style={styles.itemTitle}>{item.title}</Text>
      <Text style={styles.itemDescription} numberOfLines={2}>
        {item.shortDescription}
      </Text>
    </TouchableOpacity>
  );

  return (
    <FlatList
      data={recommendedItems}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.listContainer}
    />
  );
};

const styles = StyleSheet.create({
  listContainer: {
    paddingVertical: 10,
  },
  itemContainer: {
    width: 160,
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginRight: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  difficultyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  beginnerBadge: {
    backgroundColor: '#e3fcef',
  },
  intermediateBadge: {
    backgroundColor: '#fff8e1',
  },
  advancedBadge: {
    backgroundColor: '#ffebee',
  },
  difficultyText: {
    fontSize: 10,
    fontWeight: 'bold',
  },
  itemTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#333',
  },
  itemDescription: {
    fontSize: 12,
    color: '#777',
    lineHeight: 18,
  },
  loadingContainer: {
    height: 150,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorContainer: {
    height: 150,
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

export default RecommendedLearning; 
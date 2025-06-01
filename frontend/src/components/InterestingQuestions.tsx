import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, ActivityIndicator } from 'react-native';
import api from '../utils/api';

interface Question {
  id: string;
  question: string;
  previewAnswer: string;
  category: string;
}

interface InterestingQuestionsProps {
  onPress: (question: Question) => void;
}

const InterestingQuestions = ({ onPress }: InterestingQuestionsProps) => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoading(true);
        const response = await api.questions.getAll();
        // 只获取前3个问题
        setQuestions(response.items.slice(0, 3));
        setError(null);
      } catch (err) {
        console.error('获取问题失败:', err);
        setError('无法加载问题数据');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
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

  const renderItem = ({ item }: { item: Question }) => (
    <TouchableOpacity 
      style={styles.questionItem}
      onPress={() => onPress(item)}
    >
      <Text style={styles.category}>{item.category}</Text>
      <Text style={styles.question}>{item.question}</Text>
      <Text style={styles.answerPreview} numberOfLines={2}>
        {item.previewAnswer}
      </Text>
      <View style={styles.readMoreContainer}>
        <Text style={styles.readMore}>查看完整回答</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <FlatList
      data={questions}
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
  questionItem: {
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
  category: {
    fontSize: 12,
    color: '#3498db',
    marginBottom: 8,
    fontWeight: '500',
  },
  question: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
  },
  answerPreview: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  readMoreContainer: {
    marginTop: 10,
    alignSelf: 'flex-end',
  },
  readMore: {
    color: '#3498db',
    fontSize: 14,
    fontWeight: '500',
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

export default InterestingQuestions; 
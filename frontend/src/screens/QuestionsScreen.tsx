import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TextInput, 
  FlatList, 
  TouchableOpacity, 
  SafeAreaView
} from 'react-native';
import { questionsData, Question } from '../utils/dummyData';

const QuestionsScreen = ({ navigation }: any) => {
  const [searchQuery, setSearchQuery] = useState('');
  
  // 过滤并搜索问题
  const filteredQuestions = questionsData.filter(item => {
    return (
      searchQuery === '' || 
      item.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  });

  const renderQuestionItem = ({ item }: { item: Question }) => (
    <TouchableOpacity 
      style={styles.questionItem}
      onPress={() => navigation.navigate('QuestionDetail', { question: item })}
    >
      <Text style={styles.category}>{item.category}</Text>
      <Text style={styles.question}>{item.question}</Text>
      <Text style={styles.answerPreview} numberOfLines={2}>
        {item.answerPreview}
      </Text>
      <View style={styles.tagsContainer}>
        {item.tags.slice(0, 3).map((tag, index) => (
          <View key={index} style={styles.tag}>
            <Text style={styles.tagText}>{tag}</Text>
          </View>
        ))}
      </View>
      <TouchableOpacity 
        style={styles.readMoreButton}
        onPress={() => navigation.navigate('QuestionDetail', { question: item })}
      >
        <Text style={styles.readMoreText}>查看完整解答</Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>常见问题</Text>
        <View style={styles.searchContainer}>
          <TextInput 
            style={styles.searchInput}
            placeholder="搜索财经问题、关键词..."
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      </View>

      <FlatList
        data={filteredQuestions}
        renderItem={renderQuestionItem}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.listContainer}
      />
      
      <TouchableOpacity style={styles.aiChatButton} onPress={() => navigation.navigate('AiChat')}>
        <Text style={styles.aiChatButtonText}>向AI提问</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9f9f9',
  },
  header: {
    padding: 15,
    backgroundColor: '#3498db',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 15,
  },
  searchContainer: {
    backgroundColor: 'white',
    borderRadius: 5,
    paddingHorizontal: 10,
  },
  searchInput: {
    height: 40,
  },
  listContainer: {
    padding: 15,
    paddingBottom: 80, // 为底部按钮留空间
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
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  answerPreview: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 15,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 15,
  },
  tag: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 8,
    marginBottom: 8,
  },
  tagText: {
    fontSize: 12,
    color: '#666',
  },
  readMoreButton: {
    alignSelf: 'flex-end',
  },
  readMoreText: {
    color: '#3498db',
    fontWeight: '500',
  },
  aiChatButton: {
    position: 'absolute',
    bottom: 20,
    alignSelf: 'center',
    backgroundColor: '#3498db',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 5,
  },
  aiChatButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default QuestionsScreen; 
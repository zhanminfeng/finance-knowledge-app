import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TouchableOpacity, 
  SafeAreaView 
} from 'react-native';
import { Question, questionsData } from '../utils/dummyData';

const QuestionDetailScreen = ({ route, navigation }: any) => {
  const { question } = route.params as { question: Question };
  
  // 获取相关问题
  const relatedQuestions = question.relatedQuestions 
    ? question.relatedQuestions
        .map(id => questionsData.find(q => q.id === id))
        .filter(Boolean)
    : [];

  // 将 Markdown 格式的内容简单转换为可显示的组件
  // 注意：实际应用中应使用专门的 Markdown 渲染库，如 react-native-markdown-display
  const renderContent = () => {
    // 这里只是简单处理，实际应用中建议使用专业的 Markdown 渲染库
    return (
      <Text style={styles.content}>
        {question.fullAnswer}
      </Text>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <Text style={styles.category}>{question.category}</Text>
          <Text style={styles.title}>{question.question}</Text>
          <View style={styles.tagsContainer}>
            {question.tags.map((tag, index) => (
              <View key={index} style={styles.tag}>
                <Text style={styles.tagText}>{tag}</Text>
              </View>
            ))}
          </View>
        </View>
        
        <View style={styles.contentContainer}>
          {renderContent()}
        </View>
        
        {relatedQuestions.length > 0 && (
          <View style={styles.relatedQuestionsContainer}>
            <Text style={styles.relatedQuestionsTitle}>相关问题</Text>
            {relatedQuestions.map((relatedQuestion: any) => (
              <TouchableOpacity 
                key={relatedQuestion.id}
                style={styles.relatedQuestionItem}
                onPress={() => navigation.push('QuestionDetail', { question: relatedQuestion })}
              >
                <Text style={styles.relatedQuestionText}>{relatedQuestion.question}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
        
        <View style={styles.feedbackContainer}>
          <Text style={styles.feedbackTitle}>这个解答有帮助吗？</Text>
          <View style={styles.feedbackButtons}>
            <TouchableOpacity style={styles.feedbackButton}>
              <Text style={styles.feedbackButtonText}>👍 有帮助</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.feedbackButton}>
              <Text style={styles.feedbackButtonText}>👎 没帮助</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
      
      <TouchableOpacity 
        style={styles.askMoreButton}
        onPress={() => navigation.navigate('AiChat', { initialQuestion: `关于"${question.question}"，我想进一步了解...` })}
      >
        <Text style={styles.askMoreButtonText}>向AI提问相关问题</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
  },
  header: {
    padding: 20,
    backgroundColor: '#f9f9f9',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  category: {
    fontSize: 14,
    color: '#3498db',
    marginBottom: 10,
    fontWeight: '500',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    lineHeight: 30,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 15,
    marginRight: 8,
    marginBottom: 8,
  },
  tagText: {
    fontSize: 12,
    color: '#666',
  },
  contentContainer: {
    padding: 20,
  },
  content: {
    fontSize: 16,
    lineHeight: 24,
    color: '#333',
  },
  relatedQuestionsContainer: {
    padding: 20,
    backgroundColor: '#f9f9f9',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  relatedQuestionsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  relatedQuestionItem: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  relatedQuestionText: {
    fontSize: 14,
    color: '#3498db',
    fontWeight: '500',
  },
  feedbackContainer: {
    padding: 20,
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  feedbackTitle: {
    fontSize: 16,
    marginBottom: 15,
    color: '#666',
  },
  feedbackButtons: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  feedbackButton: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    marginHorizontal: 10,
  },
  feedbackButtonText: {
    color: '#555',
    fontWeight: '500',
  },
  askMoreButton: {
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
  askMoreButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default QuestionDetailScreen; 
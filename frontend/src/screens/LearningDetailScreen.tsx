import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TouchableOpacity, 
  SafeAreaView 
} from 'react-native';
import { LearningItem, learningData } from '../utils/dummyData';

const LearningDetailScreen = ({ route, navigation }: any) => {
  const { item } = route.params;
  
  // 将 Markdown 格式的内容简单转换为可显示的组件
  // 注意：实际应用中应使用专门的 Markdown 渲染库，如 react-native-markdown-display
  const renderContent = () => {
    // 这里只是简单处理，实际应用中建议使用专业的 Markdown 渲染库
    return (
      <Text style={styles.content}>
        {item.fullContent}
      </Text>
    );
  };
  
  // 查找相关的下一步学习内容
  const nextStepsItems = item.nextSteps 
    ? item.nextSteps.map(id => learningData.find(item => item.id === id)).filter(Boolean)
    : [];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <View style={[styles.difficultyBadge, 
            item.difficulty === 'beginner' ? styles.beginnerBadge : 
            item.difficulty === 'intermediate' ? styles.intermediateBadge : styles.advancedBadge
          ]}>
            <Text style={styles.difficultyText}>
              {item.difficulty === 'beginner' ? '入门' : 
              item.difficulty === 'intermediate' ? '进阶' : '高级'}
            </Text>
          </View>
          <Text style={styles.title}>{item.title}</Text>
          <View style={styles.tagsContainer}>
            {item.tags.map((tag, index) => (
              <View key={index} style={styles.tag}>
                <Text style={styles.tagText}>{tag}</Text>
              </View>
            ))}
          </View>
        </View>
        
        <View style={styles.contentContainer}>
          {renderContent()}
        </View>
        
        {nextStepsItems.length > 0 && (
          <View style={styles.nextStepsContainer}>
            <Text style={styles.nextStepsTitle}>推荐继续学习</Text>
            {nextStepsItems.map((nextItem: any) => (
              <TouchableOpacity 
                key={nextItem.id}
                style={styles.nextStepItem}
                onPress={() => navigation.push('LearningDetail', { item: nextItem })}
              >
                <Text style={styles.nextStepItemTitle}>{nextItem.title}</Text>
                <Text style={styles.nextStepItemDescription} numberOfLines={2}>
                  {nextItem.shortDescription}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </ScrollView>
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
  difficultyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginBottom: 10,
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
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
    marginRight: 8,
    marginBottom: 8,
  },
  tagText: {
    fontSize: 10,
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
  nextStepsContainer: {
    padding: 20,
    backgroundColor: '#f9f9f9',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  nextStepsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  nextStepItem: {
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
  nextStepItemTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#333',
  },
  nextStepItemDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
});

export default LearningDetailScreen; 
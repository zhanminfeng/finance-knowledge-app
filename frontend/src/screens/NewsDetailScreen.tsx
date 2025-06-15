import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  Image, 
  TouchableOpacity, 
  SafeAreaView 
} from 'react-native';
import { NewsItem } from '../utils/types';

const NewsDetailScreen = ({ route }: any) => {
  const { news } = route.params as { news: NewsItem };
  
  // 将 Markdown 格式的内容简单转换为可显示的组件
  // 注意：实际应用中应使用专门的 Markdown 渲染库，如 react-native-markdown-display
  const renderContent = () => {
    // 这里只是简单处理，实际应用中建议使用专业的 Markdown 渲染库
    return (
      <Text style={styles.content}>
        {news.content}
      </Text>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <Image 
          source={{ uri: news.imageUrl }} 
          style={styles.headerImage}
          resizeMode="cover"
        />

        <View style={styles.contentContainer}>
          <View style={styles.metaInfo}>
            <Text style={styles.source}>{news.source}</Text>
            <Text style={styles.date}>{news.date}</Text>
          </View>
          
          <Text style={styles.title}>{news.title}</Text>
          <Text style={styles.summary}>{news.summary}</Text>
          
          {news.tags && news.tags.length > 0 && (
            <View style={styles.tagsContainer}>
              {news.tags.map((tag, index) => (
                <View key={index} style={styles.tag}>
                  <Text style={styles.tagText}>{tag}</Text>
                </View>
              ))}
            </View>
          )}

          <View style={styles.divider} />
          
          {news.content && renderContent()}
          
          {news.aiExplanation && (
            <View style={styles.aiExplanationContainer}>
              <Text style={styles.aiExplanationTitle}>小白解读</Text>
              <Text style={styles.aiExplanation}>{news.aiExplanation}</Text>
            </View>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
  },
  headerImage: {
    width: '100%',
    height: 250,
  },
  contentContainer: {
    padding: 20,
  },
  metaInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  source: {
    fontSize: 14,
    color: '#3498db',
    fontWeight: '500',
  },
  date: {
    fontSize: 14,
    color: '#999',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    lineHeight: 32,
  },
  summary: {
    fontSize: 16,
    fontWeight: '500',
    color: '#555',
    marginBottom: 15,
    lineHeight: 24,
    fontStyle: 'italic',
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 15,
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
  divider: {
    height: 1,
    backgroundColor: '#eee',
    marginVertical: 20,
  },
  content: {
    fontSize: 16,
    lineHeight: 24,
    color: '#333',
  },
  aiExplanationContainer: {
    marginTop: 30,
    padding: 15,
    backgroundColor: '#f0f7fc',
    borderRadius: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#3498db',
  },
  aiExplanationTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#3498db',
    marginBottom: 10,
  },
  aiExplanation: {
    fontSize: 15,
    lineHeight: 22,
    color: '#444',
  },
});

export default NewsDetailScreen;
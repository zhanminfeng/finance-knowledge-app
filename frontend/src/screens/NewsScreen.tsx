import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  TouchableOpacity, 
  SafeAreaView,
  ScrollView,
  Image
} from 'react-native';
import { newsData, NewsItem } from '../utils/dummyData';

const NewsScreen = ({ navigation }: any) => {
  const [activeCategory, setActiveCategory] = useState('all');
  
  // 获取所有新闻分类
  const categories = ['all', ...Array.from(new Set(newsData.map(news => news.category)))];
  
  // 根据分类过滤新闻
  const filteredNews = activeCategory === 'all' 
    ? newsData 
    : newsData.filter(news => news.category === activeCategory);

  const renderNewsItem = ({ item }: { item: NewsItem }) => (
    <TouchableOpacity 
      style={styles.newsItem}
      onPress={() => navigation.navigate('NewsDetail', { news: item })}
    >
      <View style={styles.newsImageContainer}>
        <Image 
          source={{ uri: item.imageUrl }} 
          style={styles.newsImage}
          resizeMode="cover"
        />
        <View style={styles.categoryBadge}>
          <Text style={styles.categoryText}>{item.category}</Text>
        </View>
      </View>
      <View style={styles.newsContent}>
        <Text style={styles.newsTitle}>{item.title}</Text>
        <Text style={styles.newsSummary} numberOfLines={2}>{item.summary}</Text>
        <View style={styles.newsFooter}>
          <Text style={styles.newsSource}>{item.source}</Text>
          <Text style={styles.newsDate}>{item.date}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>财经新闻</Text>
      </View>

      <View style={styles.categoriesContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {categories.map((category, index) => (
            <TouchableOpacity 
              key={index}
              style={[styles.categoryTab, activeCategory === category && styles.activeCategoryTab]} 
              onPress={() => setActiveCategory(category)}
            >
              <Text 
                style={[styles.categoryTabText, activeCategory === category && styles.activeCategoryTabText]}
              >
                {category === 'all' ? '全部' : category}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      <FlatList
        data={filteredNews}
        renderItem={renderNewsItem}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.listContainer}
      />
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
  },
  categoriesContainer: {
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    backgroundColor: 'white',
  },
  categoryTab: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginHorizontal: 5,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
  },
  activeCategoryTab: {
    backgroundColor: '#3498db',
  },
  categoryTabText: {
    color: '#555',
    fontWeight: '500',
  },
  activeCategoryTabText: {
    color: 'white',
  },
  listContainer: {
    padding: 15,
  },
  newsItem: {
    backgroundColor: 'white',
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
    overflow: 'hidden',
  },
  newsImageContainer: {
    height: 180,
    width: '100%',
    position: 'relative',
  },
  newsImage: {
    width: '100%',
    height: '100%',
  },
  categoryBadge: {
    position: 'absolute',
    top: 10,
    left: 10,
    backgroundColor: 'rgba(52, 152, 219, 0.8)',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 15,
  },
  categoryText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
  },
  newsContent: {
    padding: 15,
  },
  newsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
  },
  newsSummary: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 10,
  },
  newsFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  newsSource: {
    fontSize: 12,
    color: '#3498db',
  },
  newsDate: {
    fontSize: 12,
    color: '#999',
  },
});

export default NewsScreen; 
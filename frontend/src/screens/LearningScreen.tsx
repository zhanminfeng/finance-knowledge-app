import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TextInput, 
  FlatList, 
  TouchableOpacity, 
  SafeAreaView,
  ScrollView
} from 'react-native';
import { learningData, LearningItem } from '../utils/dummyData';

const LearningScreen = ({ navigation }: any) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'beginner', 'intermediate', 'advanced'
  
  // 过滤和搜索功能
  const filteredData = learningData.filter(item => {
    const matchesDifficulty = activeTab === 'all' || item.difficulty === activeTab;
    const matchesSearch = 
      searchQuery === '' || 
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.shortDescription.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    
    return matchesDifficulty && matchesSearch;
  });

  const renderItem = ({ item }: { item: LearningItem }) => (
    <TouchableOpacity 
      style={styles.learningItem}
      onPress={() => navigation.navigate('LearningDetail', { item })}
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
      <View style={styles.tagsContainer}>
        {item.tags.slice(0, 2).map((tag, index) => (
          <View key={index} style={styles.tag}>
            <Text style={styles.tagText}>{tag}</Text>
          </View>
        ))}
        {item.tags.length > 2 && (
          <View style={styles.tag}>
            <Text style={styles.tagText}>+{item.tags.length - 2}</Text>
          </View>
        )}
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>财经知识学习</Text>
        <View style={styles.searchContainer}>
          <TextInput 
            style={styles.searchInput}
            placeholder="搜索知识点、关键词..."
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      </View>

      <View style={styles.tabsContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <TouchableOpacity 
            style={[styles.tab, activeTab === 'all' && styles.activeTab]} 
            onPress={() => setActiveTab('all')}
          >
            <Text style={[styles.tabText, activeTab === 'all' && styles.activeTabText]}>全部</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.tab, activeTab === 'beginner' && styles.activeTab]} 
            onPress={() => setActiveTab('beginner')}
          >
            <Text style={[styles.tabText, activeTab === 'beginner' && styles.activeTabText]}>入门</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.tab, activeTab === 'intermediate' && styles.activeTab]} 
            onPress={() => setActiveTab('intermediate')}
          >
            <Text style={[styles.tabText, activeTab === 'intermediate' && styles.activeTabText]}>进阶</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.tab, activeTab === 'advanced' && styles.activeTab]} 
            onPress={() => setActiveTab('advanced')}
          >
            <Text style={[styles.tabText, activeTab === 'advanced' && styles.activeTabText]}>高级</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      <FlatList
        data={filteredData}
        renderItem={renderItem}
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
  tabsContainer: {
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    backgroundColor: 'white',
  },
  tab: {
    paddingHorizontal: 20,
    paddingVertical: 8,
    marginHorizontal: 5,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
  },
  activeTab: {
    backgroundColor: '#3498db',
  },
  tabText: {
    color: '#555',
    fontWeight: '500',
  },
  activeTabText: {
    color: 'white',
  },
  listContainer: {
    padding: 15,
  },
  learningItem: {
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
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
    lineHeight: 20,
  },
  tagsContainer: {
    flexDirection: 'row',
  },
  tag: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
    marginRight: 5,
  },
  tagText: {
    fontSize: 10,
    color: '#666',
  },
});

export default LearningScreen; 
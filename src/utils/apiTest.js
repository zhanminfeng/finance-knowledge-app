/**
 * API测试工具
 * 用于测试前端与后端API的连接
 */

import axios from 'axios';

// API基础URL，可根据环境配置不同的地址
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * 测试API状态
 * @returns {Promise<Object>} API状态信息
 */
export const testApiStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/status`);
    console.log('API状态测试成功:', response.data);
    return {
      success: true,
      data: response.data,
      message: '后端API连接正常'
    };
  } catch (error) {
    console.error('API状态测试失败:', error);
    return {
      success: false,
      error: error,
      message: '无法连接到后端API'
    };
  }
};

/**
 * 测试学习内容API
 * @returns {Promise<Object>} 测试结果
 */
export const testLearningApi = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/learning`);
    console.log('学习内容API测试成功:', response.data);
    return {
      success: true,
      data: response.data,
      message: '学习内容API连接正常'
    };
  } catch (error) {
    console.error('学习内容API测试失败:', error);
    return {
      success: false,
      error: error,
      message: '无法连接到学习内容API'
    };
  }
};

/**
 * 测试新闻API
 * @returns {Promise<Object>} 测试结果
 */
export const testNewsApi = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/news`);
    console.log('新闻API测试成功:', response.data);
    return {
      success: true,
      data: response.data,
      message: '新闻API连接正常'
    };
  } catch (error) {
    console.error('新闻API测试失败:', error);
    return {
      success: false,
      error: error,
      message: '无法连接到新闻API'
    };
  }
};

/**
 * 测试问答API
 * @returns {Promise<Object>} 测试结果
 */
export const testQuestionsApi = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/questions`);
    console.log('问答API测试成功:', response.data);
    return {
      success: true,
      data: response.data,
      message: '问答API连接正常'
    };
  } catch (error) {
    console.error('问答API测试失败:', error);
    return {
      success: false,
      error: error,
      message: '无法连接到问答API'
    };
  }
};

/**
 * 测试搜索API
 * @returns {Promise<Object>} 测试结果
 */
export const testSearchApi = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/search`, {
      query: '基金',
      categories: []
    });
    console.log('搜索API测试成功:', response.data);
    return {
      success: true,
      data: response.data,
      message: '搜索API连接正常'
    };
  } catch (error) {
    console.error('搜索API测试失败:', error);
    return {
      success: false,
      error: error,
      message: '无法连接到搜索API'
    };
  }
};

/**
 * 测试聊天API
 * @returns {Promise<Object>} 测试结果
 */
export const testChatApi = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/chat`, {
      message: '什么是股票?'
    });
    console.log('聊天API测试成功:', response.data);
    return {
      success: true,
      data: response.data,
      message: '聊天API连接正常'
    };
  } catch (error) {
    console.error('聊天API测试失败:', error);
    return {
      success: false,
      error: error,
      message: '无法连接到聊天API'
    };
  }
};

/**
 * 运行所有API测试
 * @returns {Promise<Object>} 所有测试结果
 */
export const runAllApiTests = async () => {
  const results = {
    apiStatus: await testApiStatus(),
    learning: await testLearningApi(),
    news: await testNewsApi(),
    questions: await testQuestionsApi(),
    search: await testSearchApi(),
    chat: await testChatApi()
  };

  const allSuccess = Object.values(results).every(result => result.success);
  
  console.log('API测试结果汇总:', {
    allSuccess,
    results
  });
  
  return {
    allSuccess,
    results,
    message: allSuccess ? '所有API测试通过' : '部分API测试失败'
  };
};

export default {
  testApiStatus,
  testLearningApi,
  testNewsApi,
  testQuestionsApi,
  testSearchApi,
  testChatApi,
  runAllApiTests
}; 
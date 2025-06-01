// API服务封装模块
const API_BASE_URL = 'http://192.168.1.100:8000/api'; // 修改为你的实际服务器地址

// 基础请求函数
const request = async (endpoint: string, options: RequestInit = {}) => {
  const maxRetries = 3;
  let retries = 0;

  while (retries < maxRetries) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      retries++;
      if (retries === maxRetries) {
        console.error(`请求失败 (${retries}/${maxRetries}): ${error}`);
        throw new Error('网络请求失败，请检查网络连接后重试');
      }
      // 等待一段时间后重试
      await new Promise(resolve => setTimeout(resolve, 1000 * retries));
    }
  }
};

export const get = (endpoint: string) => request(endpoint);

export const post = (endpoint: string, data: any) => 
  request(endpoint, {
    method: 'POST',
    body: JSON.stringify(data)
  });

// 导出API服务
export const api = {
  // 学习内容API
  learning: {
    // 获取所有学习内容
    getAll: (difficulty?: string) => get(`/learning${difficulty ? `?difficulty=${difficulty}` : ''}`),
    // 获取特定学习内容
    getById: (id: string) => get(`/learning/${id}`),
    // 搜索学习内容
    search: (keyword: string) => get(`/learning/search/${keyword}`)
  },
  
  // 新闻API
  news: {
    // 获取所有新闻
    getAll: (category?: string) => get(`/news${category ? `?category=${category}` : ''}`),
    // 获取特定新闻
    getById: (id: string) => get(`/news/${id}`),
    // 搜索新闻
    search: (keyword: string) => get(`/news/search/${keyword}`)
  },
  
  // 问答API
  questions: {
    // 获取所有问题
    getAll: (category?: string) => get(`/questions${category ? `?category=${category}` : ''}`),
    // 获取特定问题
    getById: (id: string) => get(`/questions/${id}`),
    // 搜索问题
    search: (keyword: string) => get(`/questions/search/${keyword}`),
    // 获取相关问题
    getRelated: (id: string) => get(`/questions/related/${id}`)
  },
  
  // 搜索API
  search: {
    // 全局搜索
    query: (query: string, categories?: string[]) => post('/search', {
      query,
      categories: categories || ['all']
    })
  },
  
  // 聊天API
  chat: {
    // 发送消息
    send: (message: string, history?: Array<{role: string, content: string}>) => 
      post('/chat', { message, history })
  }
};

export default api; 
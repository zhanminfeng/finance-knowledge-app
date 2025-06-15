// 共享的数据类型定义
export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  content: string;
  aiExplanation: string;
  date: string;
  source: string;
  imageUrl: string;
  category: string;
  tags: string[];
}

// 其他数据类型定义...
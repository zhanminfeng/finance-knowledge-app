// 简单的前端API测试脚本
const API_BASE_URL = 'http://localhost:8001/api';

// 模拟fetch请求
async function get(endpoint) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log(`发起GET请求: ${url}`);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API错误: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`请求成功: ${endpoint}`);
    console.log(JSON.stringify(data, null, 2));
    return data;
  } catch (error) {
    console.error(`请求失败: ${error}`);
    throw error;
  }
}

async function post(endpoint, data) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log(`发起POST请求: ${url}`);
    console.log(`数据: ${JSON.stringify(data)}`);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`API错误: ${response.status}`);
    }
    
    const responseData = await response.json();
    console.log(`请求成功: ${endpoint}`);
    console.log(JSON.stringify(responseData, null, 2));
    return responseData;
  } catch (error) {
    console.error(`请求失败: ${error}`);
    throw error;
  }
}

// 测试所有API端点
async function testAllEndpoints() {
  console.log('===== 开始测试所有API端点 =====');
  
  try {
    // 测试根端点
    console.log('\n----- 测试根端点 -----');
    await get('');
    
    // 测试问题API
    console.log('\n----- 测试问题列表 -----');
    const questions = await get('/questions');
    
    if (questions.items && questions.items.length > 0) {
      const questionId = questions.items[0].id;
      console.log(`\n----- 测试问题详情 (ID: ${questionId}) -----`);
      await get(`/questions/${questionId}`);
    }
    
    // 测试新闻API
    console.log('\n----- 测试新闻列表 -----');
    const news = await get('/news');
    
    if (news.items && news.items.length > 0) {
      const newsId = news.items[0].id;
      console.log(`\n----- 测试新闻详情 (ID: ${newsId}) -----`);
      await get(`/news/${newsId}`);
    }
    
    // 测试学习内容API
    console.log('\n----- 测试学习内容列表 -----');
    await get('/learning');
    
    // 测试聊天API
    console.log('\n----- 测试聊天API -----');
    await post('/chat', { message: '请介绍一下什么是股票?' });
    
    console.log('\n===== 所有API测试完成 =====');
  } catch (error) {
    console.error('\n测试过程中发生错误:', error);
  }
}

async function testApiConnection() {
  try {
    // 测试 API 状态
    const statusResponse = await fetch('http://localhost:8000/api/status');
    const statusData = await statusResponse.json();
    console.log('API Status:', statusData);

    // 测试学习内容 API
    const learningResponse = await fetch('http://localhost:8000/api/learning');
    const learningData = await learningResponse.json();
    console.log('Learning Data:', learningData);

    // 测试新闻 API
    const newsResponse = await fetch('http://localhost:8000/api/news');
    const newsData = await newsResponse.json();
    console.log('News Data:', newsData);

    // 测试问题 API
    const questionsResponse = await fetch('http://localhost:8000/api/questions');
    const questionsData = await questionsResponse.json();
    console.log('Questions Data:', questionsData);

  } catch (error) {
    console.error('API Test Failed:', error);
  }
}

// 执行测试
testAllEndpoints();
testApiConnection(); 
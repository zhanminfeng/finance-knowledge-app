// 简单的前端API测试脚本 - 只测试问题API
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

// 测试问题API
async function testQuestionsAPI() {
  console.log('===== 开始测试问题API =====');
  
  try {
    console.log('\n----- 测试问题列表 -----');
    const questions = await get('/questions');
    
    if (questions.items && questions.items.length > 0) {
      const questionId = questions.items[0].id;
      console.log(`\n----- 测试问题详情 (ID: ${questionId}) -----`);
      await get(`/questions/${questionId}`);
    }
    
    console.log('\n===== 问题API测试完成 =====');
  } catch (error) {
    console.error('\n测试过程中发生错误:', error);
  }
}

// 执行测试
testQuestionsAPI(); 
// 简单的前端API测试脚本 - 使用fetch API
console.log('开始API测试...');

// 定义API基础URL
const API_BASE_URL = 'http://localhost:8001/api';

// 测试questions API
console.log('测试问题API...');
fetch(`${API_BASE_URL}/questions`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('问题API请求成功:');
    console.log(JSON.stringify(data, null, 2));
  })
  .catch(error => {
    console.error('问题API请求失败:', error);
  });

// 测试news API
console.log('测试新闻API...');
fetch(`${API_BASE_URL}/news`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('新闻API请求成功:');
    console.log(JSON.stringify(data, null, 2));
  })
  .catch(error => {
    console.error('新闻API请求失败:', error);
  });

// 测试learning API
console.log('测试学习内容API...');
fetch(`${API_BASE_URL}/learning`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('学习内容API请求成功:');
    console.log(JSON.stringify(data, null, 2));
  })
  .catch(error => {
    console.error('学习内容API请求失败:', error);
  });

console.log('API测试脚本执行完毕，请查看上方结果。'); 
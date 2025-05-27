# 雪球API集成使用说明

## 概述

财知道应用现已集成雪球财经新闻API，实现实时获取雪球平台上的热门财经新闻。本文档提供关于如何配置、使用和测试雪球API功能的详细说明。

## 配置说明

### 环境变量配置

雪球API功能通过以下环境变量进行控制：

1. **XUEQIU_API_ENABLED**: 是否启用雪球API (默认为False)
2. **XUEQIU_COOKIE**: 雪球网站的Cookie，用于API认证
3. **XUEQIU_USER_AGENT**: 浏览器User-Agent (可选，已有默认值)
4. **XUEQIU_FETCH_INTERVAL**: 定期获取新闻的间隔时间，单位为秒 (默认3600秒)
5. **XUEQIU_NEWS_LIMIT**: 每次获取的新闻数量 (默认20条)

### 配置示例

在启动应用前，可以通过以下方式设置环境变量：

```bash
# 启用雪球API
export XUEQIU_API_ENABLED=True

# 设置雪球Cookie (必须)
# 可通过浏览器登录雪球网站，然后从开发者工具中获取Cookie
export XUEQIU_COOKIE='your_cookie_string_here'

# 设置获取间隔 (可选)
export XUEQIU_FETCH_INTERVAL=1800  # 每30分钟获取一次

# 启动应用
uvicorn app.main:app --reload
```

## API端点说明

### 异步版API端点

1. **获取雪球新闻分类**
   - 端点: `GET /api/news/xueqiu/categories`
   - 返回: 可用的新闻分类列表
   - 示例: `["全部", "股市", "美股", "宏观", "外汇", "商品", "基金", "私募", "房产"]`

2. **手动获取最新雪球新闻**
   - 端点: `POST /api/news/xueqiu/fetch`
   - 参数: `category` (可选，默认为"全部")
   - 返回: 提示消息
   - 特点: 使用后台任务异步处理

3. **启动定期获取任务**
   - 端点: `POST /api/news/xueqiu/start`
   - 功能: 启动定期获取雪球新闻的后台任务
   - 返回: 提示消息

4. **停止定期获取任务**
   - 端点: `POST /api/news/xueqiu/stop`
   - 功能: 停止定期获取雪球新闻的后台任务
   - 返回: 提示消息

### 同步版API端点

1. **获取雪球新闻分类**
   - 端点: `GET /api/news/xueqiu/categories`
   - 返回: 可用的新闻分类列表

2. **手动获取最新雪球新闻**
   - 端点: `POST /api/news/xueqiu/fetch`
   - 参数: `category` (可选，默认为"全部")
   - 返回: 获取和保存结果
   - 特点: 同步处理，直接返回结果

## 使用示例

### 获取特定分类的新闻

```bash
# 使用curl获取美股分类新闻
curl -X POST "http://localhost:8000/api/news/xueqiu/fetch?category=美股"
```

### 前端调用示例

```javascript
// React示例
async function fetchXueqiuNews(category = '全部') {
  try {
    const response = await fetch(`/api/news/xueqiu/fetch?category=${category}`, {
      method: 'POST',
    });
    const data = await response.json();
    console.log(data.message);
    
    // 更新新闻列表
    fetchNewsAfterDelay();
  } catch (error) {
    console.error('获取雪球新闻失败:', error);
  }
}

// 延迟一段时间后获取新闻列表，以确保后台任务完成
function fetchNewsAfterDelay() {
  setTimeout(async () => {
    const response = await fetch('/api/news');
    const newsList = await response.json();
    // 更新UI
  }, 3000);
}
```

## 测试

项目包含用于测试雪球API集成的测试脚本：

```bash
# 运行雪球API测试
python test_xueqiu_api.py
```

测试脚本会执行以下测试：
1. 测试获取热门新闻
2. 测试获取不同分类新闻
3. 测试保存新闻到数据库

## 常见问题

### 1. 雪球API返回403或无法获取数据

可能原因：
- Cookie未设置或已过期
- 雪球API限制了请求频率

解决方案：
- 重新登录雪球网站获取新的Cookie
- 降低请求频率，增加`XUEQIU_FETCH_INTERVAL`的值

### 2. 无法启动定期获取任务

可能原因：
- 雪球API未启用
- 应用内存泄漏或异步任务问题

解决方案：
- 确认`XUEQIU_API_ENABLED`设置为True
- 重启应用并检查日志

## 数据结构

雪球新闻保存在数据库中的结构如下：

- **id**: 唯一标识符 (格式: "xueqiu-{原始ID}")
- **title**: 新闻标题
- **summary**: 新闻摘要
- **content**: 完整内容
- **source**: 来源 (固定为"雪球")
- **publish_date**: 发布日期
- **image_url**: 图片URL
- **url**: 原始新闻URL
- **categories**: 分类 (JSON字符串)
- **tags**: 标签 (JSON字符串)
- **ai_interpretation**: AI解读 (可选，初始为空) 
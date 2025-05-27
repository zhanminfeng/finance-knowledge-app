import asyncio
from app.services.sina_service import sina_service

async def test_fetch_news():
    print("开始测试新浪财经新闻抓取...")
    
    # 测试新闻内容抓取
    news_list = await sina_service.fetch_news_content()
    
    print(f"成功抓取到 {len(news_list)} 条新闻")
    
    # 打印所有新闻的详细信息
    print("\n所有新闻详情:")
    for i, news in enumerate(news_list, 1):
        print(f"{i}. 标题: {news['title']}")
        print(f"   链接: {news['url']}")
        print(f"   发布时间: {news['publish_time']}")
        print(f"   摘要: {news['summary']}")
        print(f"   来源: {news['source']}")
        print(f"   分类: {news['categories']}")
        print(f"   抓取时间: {news['created_at']}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(test_fetch_news()) 
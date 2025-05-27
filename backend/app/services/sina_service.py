import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import re
import asyncio
import uuid
from app.models.db.news import News as NewsModel  # 使用数据库模型
from app.db.session import async_session  # 导入异步session
import json
from sqlalchemy.ext.asyncio import AsyncSession

class SinaService:
    def __init__(self):
        self.base_url = "https://finance.sina.com.cn/"
        self.news_url = "https://finance.sina.com.cn/stock/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://finance.sina.com.cn/"
        }
        self.task = None

    async def fetch_news(self) -> List[Dict[str, Any]]:
        """
        列出新浪财经首页所有模块（栏目）的标题和链接
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=self.headers) as response:
                if response.status != 200:
                    return []
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                result = []
                # 抓取导航栏和主要模块链接
                for a in soup.find_all("a", href=True):
                    title = a.get_text(strip=True)
                    link = a["href"]
                    # 过滤掉非模块链接（如广告、活动等）
                    if title and link and link.startswith("http") and not any(x in link for x in ["zt_d", "subject", "tousu", "forerunner", "zhongce"]):
                        result.append({"title": title, "link": link})
                return result

    async def fetch_news_content(self) -> List[Dict[str, Any]]:
        """
        获取新浪财经新闻内容
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.news_url, headers=self.headers) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                print("\n--- 抓取到的HTML片段 ---\n", html[:10000], "\n--- END ---\n")
                soup = BeautifulSoup(html, "html.parser")
                news_list = []
                
                # 遍历所有a标签，筛选新闻链接
                for a in soup.find_all("a", href=True):
                    link = a["href"]
                    # 筛选href包含'/202'的链接（新闻链接通常包含日期路径）
                    if '/202' in link:
                        title = a.get_text(strip=True)
                        # 使用正则表达式提取中文标题
                        title = re.sub(r'[^\u4e00-\u9fa5]', '', title)
                        if title and link:
                            # 确保链接是完整的URL
                            if link.startswith("//"):
                                link = "https:" + link
                            elif not link.startswith("http"):
                                link = "https://finance.sina.com.cn" + link
                            
                            # 尝试获取发布时间和摘要（如果存在）
                            parent = a.parent
                            time_element = parent.find("span", class_="time") or parent.find("span", class_="date")
                            publish_time = time_element.get_text(strip=True) if time_element else datetime.now().isoformat()
                            
                            summary_element = parent.find("div", class_="summary") or parent.find("p")
                            summary = summary_element.get_text(strip=True) if summary_element else title
                            # 使用正则表达式提取中文摘要
                            if summary:
                                summary = re.sub(r'[^\u4e00-\u9fa5]', '', summary)
                            
                            # 获取新闻内容
                            try:
                                async with session.get(link, headers=self.headers) as content_response:
                                    if content_response.status == 200:
                                        content_html = await content_response.text()
                                        content_soup = BeautifulSoup(content_html, "html.parser")
                                        content_div = content_soup.find("div", class_="article-content") or content_soup.find("div", class_="article")
                                        content = content_div.get_text(strip=True) if content_div else summary
                                    else:
                                        content = summary
                            except Exception:
                                content = summary
                            
                            # 获取图片URL
                            try:
                                img_element = content_soup.find("img", class_="article-img") if content_soup else None
                                image_url = img_element["src"] if img_element and "src" in img_element.attrs else None
                            except Exception:
                                image_url = None
                            
                            news_list.append({
                                "id": str(uuid.uuid4()),
                                "title": title,
                                "summary": summary,
                                "content": content,
                                "source": "新浪财经",
                                "url": link,
                                "publish_date": datetime.fromisoformat(publish_time) if publish_time else datetime.now(),
                                "category": "财经",
                                "image_url": image_url,
                                "tags": json.dumps(["财经", "股票"]),
                                "created_at": datetime.now(),
                                "updated_at": datetime.now()
                            })
                
                return news_list

    async def schedule_news_fetch(self):
        """定时抓取新闻"""
        while True:
            try:
                news_list = await self.fetch_news_content()
                async with async_session() as session:
                    for news_data in news_list:
                        news_record = NewsModel(**news_data)
                        session.add(news_record)
                    await session.commit()
                await asyncio.sleep(86400)  # 每24小时执行一次
            except Exception as e:
                print(f"抓取新闻失败: {str(e)}")
                await asyncio.sleep(60)  # 发生错误时等待1分钟后重试

    def start_scheduled_task(self):
        if self.task is None:
            loop = asyncio.get_event_loop()
            self.task = loop.create_task(self.schedule_news_fetch())

# 启动定时任务
sina_service = SinaService()
sina_service.start_scheduled_task() 
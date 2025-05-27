import aiohttp
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from app.core.config import settings
from app.core.logging import logger

class XueqiuClient:
    """雪球财经新闻API客户端"""
    
    def __init__(self):
        """初始化雪球API客户端"""
        self.base_url = settings.XUEQIU_NEWS_URL
        self.headers = {
            "User-Agent": settings.XUEQIU_USER_AGENT,
            "Cookie": settings.XUEQIU_COOKIE,
            "Accept": "application/json, text/plain, */*"
        }
        self.is_enabled = settings.XUEQIU_API_ENABLED
        self.fetch_interval = settings.XUEQIU_FETCH_INTERVAL
        
    async def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        向雪球API发送请求
        
        Args:
            url: API URL
            params: 请求参数
            
        Returns:
            响应JSON数据或None
        """
        if not self.is_enabled:
            logger.warning("雪球API未启用，跳过请求")
            return None
            
        if not settings.XUEQIU_COOKIE:
            logger.error("雪球API Cookie未设置，无法请求")
            return None
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f"雪球API请求失败: 状态码 {response.status}")
                        return None
        except Exception as e:
            logger.error(f"雪球API请求发生异常: {str(e)}")
            return None
            
    async def get_hot_news(self, category: str = "全部", max_count: int = None) -> List[Dict]:
        """
        获取雪球热门新闻
        
        Args:
            category: 新闻分类，可选:"全部", "股市", "美股", "宏观", "外汇", "商品", "基金", "私募", "房产"
            max_count: 返回的最大新闻数量
            
        Returns:
            新闻列表
        """
        if not max_count:
            max_count = settings.XUEQIU_NEWS_LIMIT
            
        params = {
            "since_id": -1,
            "max_id": -1,
            "size": max_count
        }
        
        # 如果不是"全部"，添加分类过滤参数
        if category != "全部":
            category_mapping = {
                "股市": 102,
                "美股": 101,
                "宏观": 6,
                "外汇": 111,
                "商品": 113,
                "基金": 104,
                "私募": 105,
                "房产": 116
            }
            if category in category_mapping:
                params["category"] = category_mapping[category]
        
        result = await self._make_request(self.base_url, params)
        if not result or "list" not in result:
            return []
            
        # 格式化新闻数据
        news_list = []
        for item in result["list"]:
            try:
                # 获取主要内容
                title = item.get("title", "")
                if not title and "text" in item:
                    # 如果没有标题，使用正文前30个字作为标题
                    title = item["text"][:30] + "..." if len(item["text"]) > 30 else item["text"]
                
                # 生成唯一ID (使用雪球的ID)
                news_id = f"xueqiu-{item.get('id', '')}"
                
                # 发布日期处理
                created_at = item.get("created_at", 0)
                if created_at:
                    publish_date = datetime.fromtimestamp(created_at / 1000)  # 雪球时间戳是毫秒
                else:
                    publish_date = datetime.now()
                
                # 提取摘要 (去除HTML标签)
                text = item.get("text", "").replace("<[^>]+>", "")
                summary = text[:100] + "..." if len(text) > 100 else text
                
                # 构造新闻项
                news_item = {
                    "id": news_id,
                    "title": title,
                    "summary": summary,
                    "content": text,
                    "aiInterpretation": "",  # 初始为空，后续可通过AI生成
                    "date": publish_date.strftime("%Y-%m-%d"),
                    "source": "雪球",
                    "imageUrl": item.get("user", {}).get("profile_image_url", ""),
                    "category": category,
                    "tags": item.get("topics", []),
                    "url": f"https://xueqiu.com/{item.get('user_id', '')}/{item.get('id', '')}"
                }
                
                news_list.append(news_item)
            except Exception as e:
                logger.error(f"处理雪球新闻项时出错: {str(e)}")
                continue
                
        return news_list
    
    @classmethod
    def is_xueqiu_news_id(cls, news_id: str) -> bool:
        """检查ID是否为雪球新闻ID"""
        return news_id.startswith("xueqiu-")

# 创建单例
xueqiu_client = XueqiuClient() 
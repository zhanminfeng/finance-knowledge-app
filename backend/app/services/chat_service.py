from typing import Dict, Any
from fastapi import HTTPException
import json
import random

from app.models.chat import ChatRequest, ChatResponse
from app.core.logging import logger


class ChatService:
    """聊天服务，提供AI聊天功能"""
    
    def __init__(self):
        """初始化聊天服务"""
        # 预设一些财经问题的回答
        self.responses = {
            "股票": "股票是股份公司发行的所有权凭证，持有股票代表着对公司的部分所有权。投资股票可以通过股息收益和资本增值获利，但也面临市场风险。",
            "基金": "基金是一种集合投资工具，由专业基金经理管理，将多位投资者的资金集中起来投资于股票、债券等金融资产。基金类型包括股票型、债券型、混合型和货币市场基金等。",
            "债券": "债券是一种债务证券，发行者向投资者借款并承诺在指定日期偿还本金并支付利息。债券通常被视为比股票风险更低的投资工具。",
            "理财": "理财是对个人或家庭资产进行规划和管理，以实现财务目标的过程。良好的理财计划包括预算管理、储蓄投资、风险管理和退休规划等方面。",
            "保险": "保险是一种风险管理工具，通过支付保费来转移特定风险。常见的保险类型包括人寿保险、健康保险、财产保险和责任保险等。",
            "通货膨胀": "通货膨胀是指一般物价水平持续上涨，导致货币购买力下降的经济现象。适度的通胀对经济有益，但高通胀会侵蚀储蓄价值，影响经济稳定。",
            "利率": "利率是借款人为使用资金向贷款人支付的费用，通常以年百分比表示。中央银行通过调整基准利率来实施货币政策，影响经济活动和通胀水平。",
            "汇率": "汇率是一国货币兑换另一国货币的比率。汇率波动受多种因素影响，包括各国经济状况、利率差异、政治稳定性和市场预期等。",
            "投资组合": "投资组合是指个人或机构持有的各种投资资产的集合。通过资产配置和多元化投资，可以在控制风险的同时追求合理回报。",
            "财务报表": "财务报表是反映企业财务状况和经营成果的报告，主要包括资产负债表、利润表和现金流量表。投资者可以通过分析财务报表评估公司价值。"
        }
    
    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """生成AI回答"""
        try:
            message = request.message.strip()
            
            # 如果消息为空，返回错误
            if not message:
                raise HTTPException(status_code=400, detail="消息不能为空")
            
            # 根据消息内容生成回答
            response = self._generate_answer(message)
            
            return ChatResponse(response=response)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"生成AI回答失败: {e}")
            raise HTTPException(status_code=500, detail=f"生成回答失败: {str(e)}")
    
    def _generate_answer(self, message: str) -> str:
        """根据消息内容生成回答"""
        # 检查消息是否包含预设关键词
        for keyword, response in self.responses.items():
            if keyword in message:
                return response
        
        # 如果没有匹配的关键词，返回通用回答
        generic_responses = [
            "这是一个很好的财经问题。从财务角度来看，应该考虑风险与收益的平衡，做出合理的资产配置。",
            "作为财经小白，建议您先了解基础的财务知识，制定合理的理财计划，并根据自己的风险承受能力进行投资。",
            "这个问题涉及到金融市场的多个方面。一般来说，分散投资、长期持有、定期定额是较为稳健的投资策略。",
            "财务健康的关键在于量入为出，合理规划支出，并建立应急资金和长期投资计划。",
            "投资有风险，入市需谨慎。建议在做出任何投资决策前，充分了解相关产品特性和风险。"
        ]
        return random.choice(generic_responses)


# 创建服务实例
chat_service = ChatService() 
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_api_status(async_client: AsyncClient):
    """测试API状态检查端点"""
    response = await async_client.get("/api/status")
    
    # 验证响应状态码
    assert response.status_code == 200
    
    # 验证响应内容
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data
    assert "message" in data
    assert "财知道API服务运行正常" in data["message"] 
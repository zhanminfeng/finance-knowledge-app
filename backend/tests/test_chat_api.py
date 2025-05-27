import pytest
from httpx import AsyncClient

# Test chat API
@pytest.mark.asyncio
async def test_chat_api(async_client: AsyncClient):
    # Test chat with a simple question
    request_data = {"message": "什么是股票?"}
    response = await async_client.post("/api/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0

# Test chat API with empty message
@pytest.mark.asyncio
async def test_chat_api_empty_message(async_client: AsyncClient):
    request_data = {"message": ""}
    response = await async_client.post("/api/chat", json=request_data)
    
    # Expecting a 422 error for validation failure or a 400 for a bad request
    # The exact behavior depends on how the API validates input
    assert response.status_code in [400, 422]

# Test chat API with complex financial question
@pytest.mark.asyncio
async def test_chat_api_complex_question(async_client: AsyncClient):
    request_data = {"message": "请解释什么是股票市场的波动性以及如何应对?"}
    response = await async_client.post("/api/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 20  # Expecting a longer response for a complex question 
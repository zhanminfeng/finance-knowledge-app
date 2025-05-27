import pytest
from httpx import AsyncClient

# Test search API with keyword only
@pytest.mark.asyncio
async def test_search_with_keyword(async_client: AsyncClient):
    request_data = {"query": "投资", "categories": []}
    response = await async_client.post("/api/search", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "results" in data
    assert "total" in data
    assert isinstance(data["results"], list)
    assert isinstance(data["total"], int)
    
    # Check that each result has expected fields
    if data["results"]:
        for result in data["results"]:
            assert "id" in result
            assert "title" in result
            assert "snippet" in result
            assert "type" in result
            assert result["type"] in ["learning", "news", "question"]

# Test search API with filters
@pytest.mark.asyncio
async def test_search_with_filters(async_client: AsyncClient):
    # Test searching only in learning content
    request_data = {"query": "投资", "categories": ["learning"]}
    response = await async_client.post("/api/search", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "results" in data
    assert "total" in data
    
    # All results should be of type "learning"
    for result in data["results"]:
        assert result["type"] == "learning"
    
    # Test searching only in news
    request_data = {"query": "市场", "categories": ["news"]}
    response = await async_client.post("/api/search", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # All results should be of type "news"
    for result in data["results"]:
        assert result["type"] == "news"

# Test search API with empty keyword
@pytest.mark.asyncio
async def test_search_empty_keyword(async_client: AsyncClient):
    request_data = {"query": "", "categories": []}
    response = await async_client.post("/api/search", json=request_data)
    
    # Expecting a 422 error for validation failure or a 400 for a bad request
    # The exact behavior depends on how the API validates input
    assert response.status_code in [400, 422] 
import pytest
from httpx import AsyncClient

# Test get news items list
@pytest.mark.asyncio
async def test_get_news_items(async_client: AsyncClient):
    response = await async_client.get("/api/news")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "total" in data
    assert isinstance(data["total"], int)

# Test get news item detail
@pytest.mark.asyncio
async def test_get_news_item_detail(async_client: AsyncClient):
    # First get list to extract an ID
    list_response = await async_client.get("/api/news")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    
    if items:
        news_id = items[0]["id"]
        detail_response = await async_client.get(f"/api/news/{news_id}")
        assert detail_response.status_code == 200
        item = detail_response.json()
        assert "id" in item
        assert item["id"] == news_id
        assert "title" in item
        assert "content" in item
        assert "source" in item
        assert "publish_date" in item
    else:
        pytest.skip("No news items found to test detail view")

# Test news item detail with invalid ID
@pytest.mark.asyncio
async def test_get_news_item_detail_invalid_id(async_client: AsyncClient):
    invalid_id = "nonexistent_id"
    response = await async_client.get(f"/api/news/{invalid_id}")
    assert response.status_code == 404

# Test search news items
@pytest.mark.asyncio
async def test_search_news_items(async_client: AsyncClient):
    # Assuming there's a news item with "市场" or some keyword in the content
    search_term = "市场"
    response = await async_client.get(f"/api/news/search/{search_term}")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

# Test filtering news by category
@pytest.mark.asyncio
async def test_filter_news_by_category(async_client: AsyncClient):
    # Get all news first to see what categories exist
    all_news_response = await async_client.get("/api/news")
    assert all_news_response.status_code == 200
    all_news = all_news_response.json()["items"]
    
    if all_news:
        # Get the category from the first news item
        category = all_news[0].get("category")
        if category:
            # Filter by that category
            filtered_response = await async_client.get(f"/api/news?category={category}")
            assert filtered_response.status_code == 200
            filtered_data = filtered_response.json()
            assert "items" in filtered_data
            
            # All returned items should have the specified category
            for item in filtered_data["items"]:
                assert item["category"] == category
        else:
            pytest.skip("No category found in news items")
    else:
        pytest.skip("No news items found to test category filtering") 
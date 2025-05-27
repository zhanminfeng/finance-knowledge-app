import pytest
from httpx import AsyncClient

# Test get learning items list
@pytest.mark.asyncio
async def test_get_learning_items(async_client: AsyncClient):
    response = await async_client.get("/api/learning")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "total" in data
    assert isinstance(data["total"], int)

# Test get learning item detail
@pytest.mark.asyncio
async def test_get_learning_item_detail(async_client: AsyncClient):
    # First get list to extract an ID
    list_response = await async_client.get("/api/learning")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    
    if items:
        item_id = items[0]["id"]
        detail_response = await async_client.get(f"/api/learning/{item_id}")
        assert detail_response.status_code == 200
        item = detail_response.json()
        assert "id" in item
        assert item["id"] == item_id
        assert "title" in item
        assert "content" in item
    else:
        pytest.skip("No learning items found to test detail view")

# Test search learning items
@pytest.mark.asyncio
async def test_search_learning_items(async_client: AsyncClient):
    # Assuming there's a learning item with "股票" or some keyword in the content
    search_term = "股票"
    response = await async_client.get(f"/api/learning/search/{search_term}")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

# Test create learning item
@pytest.mark.asyncio
async def test_create_learning_item(async_client: AsyncClient):
    new_item = {
        "title": "测试学习内容",
        "shortDescription": "这是一个测试内容摘要",
        "content": "这是一个测试内容，用于测试创建功能",
        "difficulty": "入门",
        "tags": ["测试", "入门"],
        "relatedItems": []
    }
    
    response = await async_client.post("/api/learning", json=new_item)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_item["title"]
    assert data["content"] == new_item["content"]
    assert "id" in data

# Test update learning item
@pytest.mark.asyncio
async def test_update_learning_item(async_client: AsyncClient):
    # First create a new item to update
    new_item = {
        "title": "更新前的标题",
        "shortDescription": "这是更新前的内容摘要",
        "content": "这是更新前的内容",
        "difficulty": "入门",
        "tags": ["测试"],
        "relatedItems": []
    }
    
    create_response = await async_client.post("/api/learning", json=new_item)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Update the item
    updated_data = {
        "title": "更新后的标题",
        "shortDescription": "这是更新后的内容摘要",
        "content": "这是更新后的内容",
        "difficulty": "进阶",
        "tags": ["测试", "更新"],
        "relatedItems": []
    }
    
    update_response = await async_client.put(f"/api/learning/{item_id}", json=updated_data)
    assert update_response.status_code == 200
    updated_item = update_response.json()
    assert updated_item["title"] == updated_data["title"]
    assert updated_item["content"] == updated_data["content"]

# Test delete learning item
@pytest.mark.asyncio
async def test_delete_learning_item(async_client: AsyncClient):
    # First create a new item to delete
    new_item = {
        "title": "待删除的内容",
        "shortDescription": "这是待删除的内容摘要",
        "content": "这个内容将被删除",
        "difficulty": "入门",
        "tags": ["测试"],
        "relatedItems": []
    }
    
    create_response = await async_client.post("/api/learning", json=new_item)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Delete the item
    delete_response = await async_client.delete(f"/api/learning/{item_id}")
    assert delete_response.status_code == 204
    
    # Verify item is deleted
    get_response = await async_client.get(f"/api/learning/{item_id}")
    assert get_response.status_code == 404 
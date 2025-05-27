import pytest
from httpx import AsyncClient

# Test get questions list
@pytest.mark.asyncio
async def test_get_questions(async_client: AsyncClient):
    response = await async_client.get("/api/questions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "total" in data
    assert isinstance(data["total"], int)

# Test get question detail
@pytest.mark.asyncio
async def test_get_question_detail(async_client: AsyncClient):
    # First get list to extract an ID
    list_response = await async_client.get("/api/questions")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    
    if items:
        question_id = items[0]["id"]
        detail_response = await async_client.get(f"/api/questions/{question_id}")
        assert detail_response.status_code == 200
        item = detail_response.json()
        assert "id" in item
        assert item["id"] == question_id
        assert "title" in item
        assert "content" in item
        assert "answer" in item
    else:
        pytest.skip("No question items found to test detail view")

# Test question detail with invalid ID
@pytest.mark.asyncio
async def test_get_question_detail_invalid_id(async_client: AsyncClient):
    invalid_id = "nonexistent_id"
    response = await async_client.get(f"/api/questions/{invalid_id}")
    assert response.status_code == 404

# Test search questions
@pytest.mark.asyncio
async def test_search_questions(async_client: AsyncClient):
    # Assuming there's a question with "投资" or some keyword in the content
    search_term = "投资"
    response = await async_client.get(f"/api/questions/search/{search_term}")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

# Test filter questions by category
@pytest.mark.asyncio
async def test_filter_questions_by_category(async_client: AsyncClient):
    # Get all questions first to see what categories exist
    all_questions_response = await async_client.get("/api/questions")
    assert all_questions_response.status_code == 200
    all_questions = all_questions_response.json()["items"]
    
    if all_questions:
        # Get the category from the first question
        category = all_questions[0].get("category")
        if category:
            # Filter by that category
            filtered_response = await async_client.get(f"/api/questions?category={category}")
            assert filtered_response.status_code == 200
            filtered_data = filtered_response.json()
            assert "items" in filtered_data
            
            # All returned items should have the specified category
            for item in filtered_data["items"]:
                assert item["category"] == category
        else:
            pytest.skip("No category found in question items")
    else:
        pytest.skip("No question items found to test category filtering")

# Test related questions
@pytest.mark.asyncio
async def test_get_related_questions(async_client: AsyncClient):
    # First get list to extract an ID
    list_response = await async_client.get("/api/questions")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    
    if items:
        # Get the first question
        question_id = items[0]["id"]
        # Get the question detail to check if it has related questions
        detail_response = await async_client.get(f"/api/questions/{question_id}")
        assert detail_response.status_code == 200
        question = detail_response.json()
        
        # Test related questions endpoint
        related_response = await async_client.get(f"/api/questions/related/{question_id}")
        assert related_response.status_code == 200
        related_data = related_response.json()
        assert "items" in related_data
        assert "total" in related_data
        
        # If the question has related questions, verify the response
        if "relatedQuestions" in question and question["relatedQuestions"]:
            expected_count = min(len(question["relatedQuestions"]), 5)  # Default limit is 5
            assert related_data["total"] <= expected_count
    else:
        pytest.skip("No question items found to test related questions") 
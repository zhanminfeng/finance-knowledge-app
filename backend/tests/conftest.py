import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_async_db
from sqlalchemy.pool import StaticPool

# Create a test-specific in-memory database
TEST_ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_async_engine = create_async_engine(
    TEST_ASYNC_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use static pool for in-memory database
)

TestAsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_async_engine, 
    class_=AsyncSession
)

# Override the get_async_db dependency
async def override_get_async_db():
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Override the dependency for tests
app.dependency_overrides[get_async_db] = override_get_async_db

# Setup test database
@pytest_asyncio.fixture(scope="function")
async def async_client():
    # Drop all tables first to avoid index conflicts
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Create test database tables
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Run tests
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    
    # Clean up database after tests
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
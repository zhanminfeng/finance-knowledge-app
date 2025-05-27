import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 自动加载.env文件
env_path = ROOT_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # 若不存在则创建一个模板
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('''# 数据库配置
DATABASE_TYPE=sqlite
SQLITE_DB=app.db

# 应用配置
DEBUG=True
API_PREFIX=/api

# CORS配置
CORS_ORIGINS=["*"]

# 雪球API配置
XUEQIU_API_ENABLED=False
''')
    load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """应用配置设置"""
    # 应用信息
    APP_NAME: str = "财知道API"
    API_PREFIX: str = "/api"
    VERSION: str = "0.1.0"
    
    # 环境设置
    DEBUG: bool = True
    
    # 数据目录
    DATA_DIR: Path = ROOT_DIR / "data"
    
    # 雪球API配置
    XUEQIU_API_ENABLED: bool = os.getenv("XUEQIU_API_ENABLED", "False") == "True"
    XUEQIU_COOKIE: str = os.getenv("XUEQIU_COOKIE", "")
    XUEQIU_USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    XUEQIU_NEWS_URL: str = "https://xueqiu.com/statuses/hot/listV2.json"
    XUEQIU_FETCH_INTERVAL: int = 3600  # 每小时获取一次
    XUEQIU_NEWS_LIMIT: int = 20  # 每次获取的新闻数量
    
    # AI聊天相关配置
    OPENAI_API_KEY: str = ""
    AI_MODEL: str = "gpt-3.5-turbo"
    
    # CORS设置
    CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库设置
    DATABASE_TYPE: str = "sqlite"  # 可选: sqlite, postgresql
    
    # PostgreSQL设置
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "financepedia"
    
    # SQLite设置
    SQLITE_DB: str = "app.db"
    
    # 数据库URL
    DATABASE_URL: str = ""
    ASYNC_DATABASE_URL: str = ""
    SQLALCHEMY_DATABASE_URI: str = ""
    
    @field_validator('DEBUG', mode='before')
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() == "true"
        return v
    
    @field_validator('DATABASE_URL', mode='before')
    def assemble_db_url(cls, v, values):
        if v:
            return v
        
        db_type = values.data.get("DATABASE_TYPE", "sqlite")
        
        if db_type == "postgresql":
            user = values.data.get('POSTGRES_USER')
            password = values.data.get('POSTGRES_PASSWORD')
            host = values.data.get('POSTGRES_HOST')
            port = values.data.get('POSTGRES_PORT')
            db = values.data.get('POSTGRES_DB')
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        else:
            # SQLite
            db_path = ROOT_DIR / values.data.get('SQLITE_DB', 'app.db')
            # 确保数据库目录存在
            db_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{db_path}"
    
    @field_validator('ASYNC_DATABASE_URL', mode='before')
    def assemble_async_db_url(cls, v, values):
        if v:
            return v
        
        db_type = values.data.get("DATABASE_TYPE", "sqlite")
        
        if db_type == "postgresql":
            user = values.data.get('POSTGRES_USER')
            password = values.data.get('POSTGRES_PASSWORD')
            host = values.data.get('POSTGRES_HOST')
            port = values.data.get('POSTGRES_PORT')
            db = values.data.get('POSTGRES_DB')
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        else:
            # SQLite
            db_path = ROOT_DIR / values.data.get('SQLITE_DB', 'app.db')
            # 确保数据库目录存在
            db_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite+aiosqlite:///{db_path}"
    
    @field_validator('SQLALCHEMY_DATABASE_URI', mode='before')
    def assemble_sqlalchemy_db_url(cls, v, values):
        if v:
            return v
        
        db_type = values.data.get("DATABASE_TYPE", "sqlite")
        
        if db_type == "postgresql":
            user = values.data.get('POSTGRES_USER')
            password = values.data.get('POSTGRES_PASSWORD')
            host = values.data.get('POSTGRES_HOST')
            port = values.data.get('POSTGRES_PORT')
            db = values.data.get('POSTGRES_DB')
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        else:
            # SQLite
            db_path = ROOT_DIR / values.data.get('SQLITE_DB', 'app.db')
            # 确保数据库目录存在
            db_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite+aiosqlite:///{db_path}"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

# 创建设置单例
settings = Settings() 
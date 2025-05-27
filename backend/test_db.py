import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_db_connection():
    """测试数据库连接"""
    try:
        # 创建引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 尝试连接
        with engine.connect() as connection:
            print(f"成功连接到数据库: {settings.DATABASE_URL}")
            
            # 测试查询
            result = connection.execute(text("SELECT sqlite_version()"))
            version = result.scalar()
            print(f"SQLite版本: {version}")
            
            # 检查表是否存在
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            print(f"数据库中的表: {', '.join(tables)}")
            
            # 检查学习内容表数据
            if 'learning' in tables:
                result = connection.execute(text("SELECT COUNT(*) FROM learning"))
                count = result.scalar()
                print(f"learning表中有 {count} 条记录")
                
                if count > 0:
                    result = connection.execute(text("SELECT id, title, difficulty FROM learning LIMIT 3"))
                    rows = result.fetchall()
                    print("\n学习内容示例:")
                    for row in rows:
                        print(f"  ID: {row[0]}, 标题: {row[1]}, 难度: {row[2]}")
                
                # 测试JSON字段
                try:
                    result = connection.execute(text("SELECT id, title, tags FROM learning LIMIT 1"))
                    row = result.fetchone()
                    if row:
                        print(f"\nJSON字段示例:")
                        print(f"  ID: {row[0]}, 标题: {row[1]}, 标签(原始): {row[2]}")
                except Exception as e:
                    print(f"检查JSON字段时出错: {e}")
            
            # 检查新闻表数据
            if 'news' in tables:
                result = connection.execute(text("SELECT COUNT(*) FROM news"))
                count = result.scalar()
                print(f"\nnews表中有 {count} 条记录")
            
            # 检查问题表数据
            if 'questions' in tables:
                result = connection.execute(text("SELECT COUNT(*) FROM questions"))
                count = result.scalar()
                print(f"questions表中有 {count} 条记录")
                
    except Exception as e:
        print(f"数据库测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1) 
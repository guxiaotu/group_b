from sqlmodel import text

from app.config.database import engine


def test_connection():

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print("✅ 数据库连接成功！")
            print(f"PostgreSQL 版本: {version[0]}")
    except Exception as e:
        print("❌ 数据库连接失败！")
        print(f"错误: {e}")
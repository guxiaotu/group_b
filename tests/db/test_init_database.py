from sqlalchemy import text

from app.config.database import engine, create_tables, drop_tables
from app.service.x_service import save_data


def test_connection():

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print("✅ 数据库连接成功！")
            print(f"PostgreSQL 版本: {version[0]}")
    except Exception as e:
        raise e


def test_create_table():
    create_tables()


def test_drop_table():
    drop_tables()


def test_sava_data():
    save_data()

import pytest
from sqlalchemy import text

from app.config.database import engine, create_tables, drop_tables
from app.service.x_service import save_data


@pytest.mark.asyncio
async def test_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            assert version is not None
            print("✅ 数据库连接成功！")
            print(f"PostgreSQL 版本: {version[0]}")
    except Exception as e:
        raise e


@pytest.mark.asyncio
async def test_create_table():
    await create_tables()


@pytest.mark.asyncio
async def test_sava_data():
    await save_data()


@pytest.mark.asyncio
async def test_drop_table():
    await drop_tables()

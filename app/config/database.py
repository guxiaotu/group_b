import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel

# 加载 .env
load_dotenv()

# 只读取 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# mysql 异步协议：mysql+aiomysql://
engine = create_async_engine(
    url=str(DATABASE_URL),
    echo=True,  # 调试用
    pool_pre_ping=True,  # 防止断连
)

# SessionLocal：会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()


# FastAPI依赖项，使用SessionLocal
# 异步依赖项
async def get_session():
    async with AsyncSessionLocal() as db:
        yield db


async def create_tables():
    async with engine.begin() as conn:
        # run_sync 用来在异步连接上执行同步的metadata操作
        await conn.run_sync(lambda _: SQLModel.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: SQLModel.metadata.drop_all)


def test_x():
    import asyncio
    # 创建表
    asyncio.run(create_tables())
    # 删除表
    # asyncio.run(drop_tables())

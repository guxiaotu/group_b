import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# 加载 .env
load_dotenv()

# 只读取 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# mysql 异步协议：mysql+aiomysql://
# postgresql 异步协议：postgresql+asyncpg:
engine = create_async_engine(
    url=str(DATABASE_URL),
    echo=True,  # 调试打印SQL语句
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接词大池满后最多再创建20个连接池
    pool_pre_ping=True,  # 防止断连
)

# SessionLocal：会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # commit后不会自动过期（可以继续使用对象，比如访问对象属性）
    class_=AsyncSession,  # 指定为SQLModel封装后的AsyncSession，而不是原生SQLAlchemy
)


# FastAPI依赖项，使用SessionLocal
# 异步依赖项
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables():
    async with engine.begin() as conn:
        # run_sync 用来在异步连接上执行同步的metadata操作
        await conn.run_sync(
            lambda sync_conn: SQLModel.metadata.create_all(bind=sync_conn)
        )


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: SQLModel.metadata.drop_all(bind=sync_conn)
        )

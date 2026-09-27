import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session

# 加载 .env
load_dotenv()

# 只读取 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    url=str(DATABASE_URL),
    echo=True,  # 打印SQL语句
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接词大池满后最多再创建20个连接池
    pool_pre_ping=True,  # 防止断连
)

# 会话工厂：SessionLocal，每次调用产生新Session
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,  # commit后不会自动过期（可以继续使用对象，比如访问对象属性）
    class_=Session,  # 指定为SQLModel的Session，而不是原生SQLAlchemy
)


def get_session():
    with SessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def create_tables():
    SQLModel.metadata.create_all(engine)


def drop_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.drop_all(engine)

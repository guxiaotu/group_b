import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# 加载 .env
load_dotenv()

# 只读取 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    url=str(DATABASE_URL),
    echo=True,  # 调试用
    pool_pre_ping=True,  # 防止断连
)


def create_tables():
    SQLModel.metadata.create_all(engine)


def drop_tables():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        return session


def test_x():
    create_tables()

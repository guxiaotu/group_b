from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql+psycopg://Django123456:Django123456@localhost:5432/test"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # 调试用
    pool_pre_ping=True,  # 防止断连
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]





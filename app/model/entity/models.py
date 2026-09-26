import datetime

from sqlalchemy import Column, Date, Float, Integer
from sqlmodel import Field, SQLModel

class X(SQLModel, table=True):
    id: int = Field(sa_column=Column('id', Integer, primary_key=True, autoincrement=True))
    month: datetime.date = Field(sa_column=Column('month', Date, nullable=False))
    count: int = Field(sa_column=Column('count', Integer, nullable=False))
    ratios: float = Field(sa_column=Column('ratios', Float, nullable=False))
    sample_count: int = Field(sa_column=Column('sample_count', Integer, nullable=False))

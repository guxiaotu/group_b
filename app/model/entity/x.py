from datetime import date

from sqlmodel import SQLModel, Field


class X(SQLModel, table=True):
    # 由数据库控制组建的创建
    id: int | None = Field(default=None, primary_key=True)
    month: date = Field()
    count: int
    ratios: float
    sample_count: int
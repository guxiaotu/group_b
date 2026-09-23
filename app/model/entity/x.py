from datetime import date, datetime

from pydantic import field_serializer
from sqlmodel import SQLModel, Field


class X(SQLModel, table=True):
    # 由数据库控制组建的创建
    id: int | None = Field(default=None, primary_key=True)
    month: date = Field()
    count: int
    ratios: float
    sample_count: int

    @field_serializer("month")
    def serialize_sample_count(self, v: datetime) -> str:
        """ 需要序列化字符串后才能传输给前端"""
        return v.strftime("%Y-%m")

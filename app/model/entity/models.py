import datetime

from sqlmodel import Field, SQLModel


class X(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    month: datetime.date
    count: int
    ratios: float
    sample_count: int

from typing import List

from pydantic import BaseModel


class X(BaseModel):
    months: List[str]
    counts: List[float]
    ratios: List[float]
    sample_count: List[float]

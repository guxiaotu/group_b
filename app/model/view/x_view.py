from datetime import date
from typing import List

from pydantic import BaseModel


class XView(BaseModel):
    """
    DTO for X
    """
    month: List[str]
    count: List[float]
    ratios: List[float]
    sample_count: List[float]

from typing import List

from pydantic import BaseModel


class XView(BaseModel):
    """
    VO for X
    """

    month: List[str]  # echarts渲染time类型会有问题，转化为字符串
    count: List[int]
    ratios: List[float]
    sample_count: List[float]

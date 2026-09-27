from pydantic import BaseModel


class XView(BaseModel):
    """
    VO for X
    """

    month: list[str]  # echarts渲染time类型会有问题，转化为字符串
    count: list[int]
    ratios: list[float]
    sample_count: list[float]

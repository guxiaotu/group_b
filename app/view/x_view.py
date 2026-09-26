from typing import List

from sqlmodel import select

from app.config.database import get_session
from app.model.entity import X
from app.model.view import XView


def find_entity() -> List[X]:
    with get_session() as s:
        return s.exec(select(X)).all()


def get_view() -> XView:
    x_list = find_entity()
    return XView(
        month=[
            x.month.strftime("%Y-%m") for x in x_list
        ],  # echarts渲染time类型会有问题，转化为字符串
        count=[x.count for x in x_list],
        ratios=[x.ratios for x in x_list],
        sample_count=[x.sample_count for x in x_list],
    )

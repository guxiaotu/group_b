from typing import Sequence

from sqlmodel import select, Session

from app.model.entity import X
from app.model.view import XView


def find_entity(s: Session) -> Sequence[X]:
    return s.exec(select(X)).all()


def get_view(s: Session) -> XView:
    x_list = find_entity(s)
    return XView(
        month=[
            x.month.strftime("%Y-%m") for x in x_list
        ],  # echarts渲染time类型会有问题，转化为字符串
        count=[x.count for x in x_list],
        ratios=[x.ratios for x in x_list],
        sample_count=[x.sample_count for x in x_list],
    )

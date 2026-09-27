from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.model.entity import X
from app.model.view import XView


async def find_entity(s: AsyncSession) -> Sequence[X]:
    return (await s.execute(select(X))).scalars().all()


async def get_view(s: AsyncSession) -> XView:
    x_list = await find_entity(s)
    return XView(
        month=[
            x.month.strftime("%Y-%m") for x in x_list
        ],  # echarts渲染time类型会有问题，转化为字符串
        count=[x.count for x in x_list],
        ratios=[x.ratios for x in x_list],
        sample_count=[x.sample_count for x in x_list],
    )

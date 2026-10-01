import logging
from typing import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.entity import X
from app.model.view import XView

logger = logging.getLogger(__name__)


async def find_entity(s: AsyncSession) -> Sequence[X]:
    return (await s.exec(select(X))).all()


async def get_view(s: AsyncSession) -> XView:
    x_list = await find_entity(s) or []

    if not x_list:
        logger.info("查询结果为空！")
        return XView(month=[], count=[], ratios=[], sample_count=[])

    months: list[str] = []
    counts: list[int] = []
    ratios: list[float] = []
    sample_counts: list[int] = []

    for x in x_list:
        months.append(x.month.strftime("%Y-%m") if x.month else "")
        counts.append(x.count)
        ratios.append(x.ratios)
        sample_counts.append(x.sample_count)

    return XView(
        month=months,
        count=counts,
        ratios=ratios,
        sample_count=sample_counts,
    )

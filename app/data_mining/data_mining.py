import asyncio
from pathlib import Path

import pandas as pd

from app.model.entity import X

DATA_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "csv"
    / "上架月份分布图_分析数据.csv"
)


async def read_data() -> list[X]:
    # 1. 读取 CSV（日期列自动解析）
    df = await asyncio.to_thread(pd.read_csv, DATA_DIR)

    # 转化标准日期格式
    df["月份"] = pd.to_datetime(
        df["月份"].astype(str) + "-01", format="%Y-%m-%d", errors="coerce"
    ).dt.date

    # 2. CSV → SQLModel 列表
    return [
        X(
            month=row["月份"],
            count=row["商品数量"],
            ratios=row["样本占比(%)"],
            sample_count=row["样本累计数量"],
        )
        for _, row in df.iterrows()
    ]

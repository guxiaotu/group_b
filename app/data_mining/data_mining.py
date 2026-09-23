from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd

from app.model.x import X

DATA_DIR = (
        Path(__file__).resolve().parent.parent.parent
        / "data"
        / "csv"
        / "上架月份分布图_分析数据.csv"
)


def get_data() -> List[X]:
    # 1. 读取 CSV（日期列自动解析）
    df = pd.read_csv(DATA_DIR)

    # 2. CSV → SQLModel 列表
    x_list: list[X] = []
    for _, row in df.iterrows():
        x_list.append(
            X(
                month=datetime.strptime(row["月份"], "%Y-%m").date(),
                count=int(row["商品数量"]),
                ratios=float(row["样本占比(%)"]),
                sample_count=int(row["样本累计数量"])
            )
        )

    return x_list

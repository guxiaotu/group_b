from pathlib import Path

import pandas as pd

DATA_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "csv"
    / "上架月份分布图_分析数据.csv"
)


def get_data():
    df = pd.read_csv(DATA_DIR)
    months = df["月份"].astype(str).tolist()
    counts = pd.to_numeric(df["商品数量"], errors="coerce").tolist()
    ratios = pd.to_numeric(df["样本占比(%)"], errors="coerce").tolist()
    sample_count = pd.to_numeric(df["样本累计数量"], errors="coerce").tolist()
    return months, counts, ratios, sample_count


get_data()

"""TRANSFORM: làm sạch dữ liệu (tương ứng cell 6, 9, 12, 18 trong notebook)."""
import logging

import pandas as pd

from . import config

log = logging.getLogger(__name__)

REQUIRED_COLS = {"InvoiceNo", "StockCode", "Description", "Quantity",
                 "InvoiceDate", "UnitPrice", "CustomerID", "Country"}
OUTPUT_COLS = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
               "UnitPrice", "CustomerID", "Country", "TotalSpend"]


def validate(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"File thiếu cột: {sorted(missing)}")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    validate(df)
    df = df.copy()
    for c in ["InvoiceNo", "StockCode", "Description", "Country"]:
        df[c] = df[c].astype(str).str.strip()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    if config.DROP_DUPLICATES:
        df = df.drop_duplicates()
    df["CustomerID"] = df["CustomerID"].astype("Int64")
    df["TotalSpend"] = df["Quantity"] * df["UnitPrice"]

    n0 = len(df)
    bad_date = df["InvoiceDate"].isna().sum()
    df = df.dropna(subset=["CustomerID", "InvoiceDate"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
    log.info("Transform: %s dòng -> %s dòng sạch (ngày lỗi: %s)", n0, len(df), bad_date)
    return df[OUTPUT_COLS].reset_index(drop=True)

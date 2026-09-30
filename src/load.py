"""LOAD: nạp vào MySQL theo kiểu upsert theo InvoiceNo (chạy lại không bị trùng)."""
import logging

import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.types import DateTime, String, Text

from . import config
from .transform import OUTPUT_COLS

log = logging.getLogger(__name__)

DTYPES = {  # kiểu rõ ràng để tạo được index trong MySQL
    "InvoiceNo": String(20), "StockCode": String(20), "Description": Text(),
    "InvoiceDate": DateTime(), "CustomerID": String(20), "Country": String(60),
}


def load(df: pd.DataFrame, engine) -> None:
    tbl, stage = config.TABLE_RETAIL, f"{config.TABLE_RETAIL}_stage"
    df.to_sql(stage, engine, if_exists="replace", index=False, chunksize=5000, dtype=DTYPES)

    cols = ", ".join(OUTPUT_COLS)
    with engine.begin() as conn:
        if not inspect(engine).has_table(tbl):
            conn.execute(text(f"RENAME TABLE {stage} TO {tbl}"))
            conn.execute(text(
                f"ALTER TABLE {tbl} ADD INDEX idx_invoice (InvoiceNo), "
                "ADD INDEX idx_customer (CustomerID), ADD INDEX idx_date (InvoiceDate)"))
            log.info("Tạo bảng %s mới với %s dòng", tbl, len(df))
        else:
            deleted = conn.execute(text(
                f"DELETE r FROM {tbl} r JOIN (SELECT DISTINCT InvoiceNo FROM {stage}) s "
                "ON r.InvoiceNo = s.InvoiceNo")).rowcount
            conn.execute(text(f"INSERT INTO {tbl} ({cols}) SELECT {cols} FROM {stage}"))
            conn.execute(text(f"DROP TABLE {stage}"))
            log.info("Upsert: xoá %s dòng cũ, chèn %s dòng", deleted, len(df))

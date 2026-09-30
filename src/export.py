"""EXPORT: ghi kết quả ra CSV (Power BI) và bảng MySQL."""
import logging

import pandas as pd

from . import config

log = logging.getLogger(__name__)


def to_csv(df_cohort: pd.DataFrame, rfm: pd.DataFrame, seg: pd.DataFrame) -> None:
    df_cohort.to_csv(config.PROCESSED_DIR / "Cohort_Retention_Data.csv", index=False)
    rfm.to_csv(config.PROCESSED_DIR / "RFM_Customers.csv", index=False)
    seg.reset_index().to_csv(config.PROCESSED_DIR / "RFM_Segments.csv", index=False)


def to_mysql(engine, df_cohort: pd.DataFrame, rfm: pd.DataFrame, seg: pd.DataFrame) -> None:
    df_cohort.to_sql("cohort_retention", engine, if_exists="replace", index=False)
    rfm.to_sql("rfm_customers", engine, if_exists="replace", index=False, chunksize=5000)
    seg.reset_index().to_sql("rfm_segments", engine, if_exists="replace", index=False)
    log.info("Đã ghi cohort_retention, rfm_customers, rfm_segments vào MySQL")

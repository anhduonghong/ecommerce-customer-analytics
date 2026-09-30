"""Cohort retention: truy vấn + biểu đồ heatmap."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import text

from . import config

COHORT_SQL = text("""
WITH cohort_base AS (
    SELECT CustomerID,
           DATE_FORMAT(InvoiceDate, '%Y-%m-01') AS InvoiceMonth,
           DATE_FORMAT(MIN(InvoiceDate) OVER(PARTITION BY CustomerID), '%Y-%m-01') AS CohortMonth
    FROM retail WHERE CustomerID IS NOT NULL AND Quantity > 0
),
cohort_counts AS (
    SELECT CohortMonth,
           PERIOD_DIFF(DATE_FORMAT(InvoiceMonth, '%Y%m'), DATE_FORMAT(CohortMonth, '%Y%m')) AS CohortIndex,
           COUNT(DISTINCT CustomerID) AS ActiveCustomers
    FROM cohort_base GROUP BY CohortMonth, CohortIndex
)
SELECT CohortMonth, CohortIndex, ActiveCustomers,
       FIRST_VALUE(ActiveCustomers) OVER(PARTITION BY CohortMonth ORDER BY CohortIndex ASC) AS InitialCustomers,
       ROUND(ActiveCustomers * 1.0 / FIRST_VALUE(ActiveCustomers) OVER(
             PARTITION BY CohortMonth ORDER BY CohortIndex ASC), 4) AS RetentionRate
FROM cohort_counts ORDER BY CohortMonth, CohortIndex;
""")


def compute(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(COHORT_SQL, con=conn)


def plot(df_cohort: pd.DataFrame) -> None:
    d = df_cohort.copy()
    d["CohortDate"] = pd.to_datetime(d["CohortMonth"])
    d = d.sort_values(["CohortDate", "CohortIndex"])
    labels = d["CohortDate"].dt.strftime("%b-%Y").unique()
    d["CohortDisplay"] = pd.Categorical(d["CohortDate"].dt.strftime("%b-%Y"), categories=labels, ordered=True)
    d["RetentionPct"] = d["RetentionRate"] * 100
    m = d.pivot(index="CohortDisplay", columns="CohortIndex", values="RetentionPct")

    plt.figure(figsize=(16, 9))
    sns.heatmap(m, annot=True, fmt=".1f", cmap="Blues", vmin=0, vmax=50,
                cbar_kws={"label": "Retention Rate (%)"})
    plt.title("Monthly Customer Retention Cohort Analysis (%)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Cohort Index (Months Since First Purchase)")
    plt.ylabel("Cohort Month (Acquisition Month)")
    plt.tight_layout()
    plt.savefig(config.IMAGES_DIR / "cohort_heatmap.png", dpi=150)
    plt.close()

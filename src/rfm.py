"""RFM: truy vấn, chấm điểm, phân segment + biểu đồ treemap."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import squarify
from sqlalchemy import text

from . import config

RFM_SQL = text("""
WITH snapshot AS (SELECT DATE_ADD(MAX(InvoiceDate), INTERVAL 1 DAY) AS snapshot_date FROM retail)
SELECT t.CustomerID,
       DATEDIFF((SELECT snapshot_date FROM snapshot), MAX(t.InvoiceDate)) AS Recency,
       COUNT(DISTINCT t.InvoiceNo) AS Frequency,
       ROUND(SUM(t.Quantity * t.UnitPrice), 2) AS Monetary
FROM retail t WHERE t.CustomerID IS NOT NULL
GROUP BY t.CustomerID HAVING Monetary > 0;
""")

SEGMENT_MAP = {
    r'[1-2][1-2]': 'Hibernating', r'[1-2][3-4]': 'At-Risk', r'[1-2]5': 'Cannot Lose Them',
    r'3[1-2]': 'About to Sleep', r'33': 'Need Attention', r'[3-4][4-5]': 'Loyal Customers',
    r'41': 'Promising', r'51': 'New Customers', r'[4-5][2-3]': 'Potential Loyalists',
    r'5[4-5]': 'Champions',
}


def compute(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        rfm = pd.read_sql(RFM_SQL, con=conn)
    rfm["R_score"] = pd.qcut(rfm["Recency"], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_score"] = pd.qcut(rfm["Monetary"], q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_Score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)
    rfm["Segment"] = (rfm["R_score"].astype(str) + rfm["F_score"].astype(str)).replace(SEGMENT_MAP, regex=True)
    return rfm


def summarize(rfm: pd.DataFrame) -> pd.DataFrame:
    seg = rfm.groupby("Segment").agg(
        Recency_mean=("Recency", "mean"), Frequency_mean=("Frequency", "mean"),
        Monetary_mean=("Monetary", "mean"), Customer_Count=("CustomerID", "count"),
        Total_Revenue=("Monetary", "sum")).round(1)
    seg["Customer_Share_%"] = (seg["Customer_Count"] / len(rfm) * 100).round(1)
    seg["Revenue_Share_%"] = (seg["Total_Revenue"] / rfm["Monetary"].sum() * 100).round(1)
    return seg.sort_values("Total_Revenue", ascending=False)


def plot(seg: pd.DataFrame) -> None:
    labels = [f"{s}\n{c:,} cust ({sh}%)\nRev: {r}%" for s, c, sh, r in
              zip(seg.index, seg["Customer_Count"], seg["Customer_Share_%"], seg["Revenue_Share_%"])]
    plt.figure(figsize=(14, 8))
    squarify.plot(sizes=seg["Customer_Count"], label=labels,
                  color=sns.color_palette("Blues_r", len(seg)), alpha=0.85,
                  text_kwargs={"fontsize": 10, "weight": "bold"})
    plt.title("Customer Segments Treemap (Counts & Revenue Contribution)", fontsize=14, fontweight="bold", pad=15)
    plt.axis("off")
    plt.savefig(config.IMAGES_DIR / "rfm_treemap.png", dpi=150, bbox_inches="tight")
    plt.close()

# E-Commerce Customer Analytics & Retention Intelligence Platform

An end-to-end data analytics pipeline and business intelligence system leveraging the UCI Online Retail II dataset (over 200,000 sales records in uS). The project models customer lifecycle dynamics, retention curves, and monetary concentration using a Dimensional Star Schema, Cohort Retention Indexing ($M_0$--$M_5$), and Behavioral RFM Segmentation[cite: 1].

---

## 1. Executive Summary & Core Metrics

E-commerce businesses frequently encounter high customer acquisition costs (CAC) paired with steep early drop-offs[cite: 1]. This project audits and analyzes customer purchasing behavior across 2,724 validated accounts to identify retention drop-off patterns, uncover high-value segments, and prevent revenue leakage[cite: 1].

| Metric | Measured Value | Operational Significance |
| :--- | :--- | :--- |
| Validated Customer Accounts | 2,724 accounts | Base after removing cancellations, guest IDs, and abnormal unit prices[cite: 1]. |
| Average Customer Lifetime Value (CLV) | £1,255 | Benchmark revenue expectation across retained customer cohorts. |
| Month 1 Churn Cliff | 65% – 75% | Steep drop-off observed immediately between acquisition ($M_0$) and $M_1$[cite: 1]. |
| Pareto Revenue Concentration | Top 20%–25% generate >70% revenue | Disproportionate financial dependency on high-Monetary accounts[cite: 1]. |
| Retention Payoff Threshold | >60% retention rate | Achieved once an account reaches their third completed order ($M_2+$)[cite: 1]. |

---

## 2. System Architecture & End-to-End Pipeline

```text
[ Raw Transaction Logs (CSV: 200k+ records) ]
                       │
                       ▼
[ Python Ingestion & Preprocessing (Pandas, NumPy) ]
  - Filter cancellations (InvoiceNo 'C') & Quantity <= 0[cite: 1]
  - Exclude null guest accounts (CustomerID IS NULL)[cite: 1]
  - Deduplicate records & eliminate UnitPrice <= 0[cite: 1]
  - Derive line-item revenue: TotalSpend = Quantity * UnitPrice[cite: 1]
                       │
                       ▼
[ Relational Data Warehouse (PostgreSQL / MySQL Engine) ]
  - Star Schema implementation (Fact_Transactions, Dim_Customer, Dim_Product, Dim_Date)[cite: 1]
  - Integrity constraints & indexing on foreign keys
                       │
                       ▼
[ Analytical Transformation Engines (SQL CTEs & Window Functions) ]
  - Cohort identification: MIN(InvoiceDate) OVER (PARTITION BY CustomerID)[cite: 1]
  - Quantile scoring (NTILE / qcut) across Recency, Frequency, and Monetary dimensions[cite: 1]
                       │
                       ▼
[ Business Intelligence & Reporting (Microsoft Power BI) ]
  - Direct relational modeling (Star Schema, 1-to-many bidirectional relationships)[cite: 1]
  - Dynamic DAX measures for MoM revenue, CLV, and cohort retention decay[cite: 1]
  - Interactive multi-page dashboard with dynamic customer lookup slicers[cite: 1]
```

---

## 3. Data Processing & Methodology Details

### Data Sanitization Protocol
The pipeline applies deterministic filtering logic to guarantee data integrity[cite: 1]:
* **Cancellations and Reversals:** Filtered records where `InvoiceNo` starts with `'C'` or `Quantity <= 0`[cite: 1].
* **Guest Transactions:** Removed records where `CustomerID IS NULL` to prevent distortion in customer-level metrics[cite: 1].
* **Price Anomalies:** Purged system adjustment rows and negative values where `UnitPrice <= 0`[cite: 1].
* **Feature Engineering:** Calculated gross transaction value per line item as $\text{TotalSpend} = \text{Quantity} \times \text{UnitPrice}$[cite: 1].

### Cohort Retention Indexing ($M_0$--$M_5$)
* Mapped each customer's acquisition timestamp:
  $$\text{First\_Purchase\_Month} = \min(\text{InvoiceDate}) \quad \text{over } \text{CustomerID} \text{ partition}$$[cite: 1]
* Computed `Cohort_Index` as the zero-indexed month offset between current order date and initial purchase date[cite: 1].
* Evaluated aggregate retention percentage across monthly boundaries:
  $$\text{Retention Rate}_{n} = \frac{\text{Active Customers in Cohort at Month } n}{\text{Total Cohort Base at Month } 0} \times 100\%$$[cite: 1]

### RFM Quantile Segmentation
Analyzed using the operational cutoff date $T = \max(\text{InvoiceDate}) + 1\text{ day}$[cite: 1]:
* **Recency ($R$):** Elapsed days from an account's latest invoice date to reference point $T$[cite: 1].
* **Frequency ($F$):** Total count of unique completed transactions via `COUNT(DISTINCT InvoiceNo)`[cite: 1].
* **Monetary ($M$):** Cumulative account revenue generated via `SUM(TotalSpend)`[cite: 1].

Values were partitioned into quintiles (1–5) and classified into operational groups: Champions, Loyal Customers, Potential Loyalists, New Customers, At Risk, and Lost[cite: 1].

---

## 4. Key Business Findings & Strategic Recommendations

### Quantitative Insights
* **The Month 1 Churn Cliff:** 65%–75% of newly acquired accounts churn prior to their second month, indicating an onboarding friction point rather than product dissatisfaction[cite: 1].
* **Revenue Asymmetry:** The top 20% of customer accounts contribute over 70% of total platform turnover[cite: 1].
* **Dormant Enterprise Value:** High historical spend accounts (£1,255 avg. CLV) exhibited inactivity exceeding 90 days due to absent post-purchase engagement workflows[cite: 1].

### Actionable Next Steps
* **Automated Onboarding Sequence (Days 14–30):** Execute an automated 3-stage communication flow (Day 1: confirmation and usage guide; Day 7: cross-category recommendations; Day 14: targeted time-sensitive voucher) to bridge the $M_0$ to $M_1$ retention drop[cite: 1].
* **At-Risk Account Recovery:** Query accounts in the At-Risk bucket ($R > 90$ days, high $M$) on a scheduled basis for prioritized outreach and restricted-window reactivation discounts[cite: 1].
* **VIP Account Protection:** Replace public discount models for Champions with loyalty benefits, such as priority fulfillment, dedicated support, and preview product access[cite: 1].
* **Data Roadmap:** Migrate periodic pipeline execution to an automated orchestration framework (`dbt` + `Apache Airflow`) and integrate predictive churn algorithms (XGBoost) to detect churn indicators ahead of disengagement[cite: 1].

---

## 5. Repository Layout

```text
ecommerce-customer-analytics/
├── .env                             # Database configuration template
├── .gitignore                       # Git exclusion rules (virtual envs, secrets, cache)
├── README.md                        # Project technical documentation
├── requirements.txt                 # Pinned dependencies for reproducible execution
│
├── dashboard/
│   └── Ecommerce_Customer_Segmentation.pbix      # 3-page interactive Power BI report
│
├── data/
│   ├── raw/                         # Raw transaction logs (UCI repository)
│   └── processed/                   # Cleaned and modeled CSV/Parquet extracts
│
├── images/
│   ├── executive.png                # Executive Overview
│   ├── cohort.png                   # Cohort retention visualization
│   └── rfm.png                      # RFM score distribution chart
│   └── products.png                 # Products Sales Performnace
└── notebooks/
    └── customer_analysis.ipynb      # Complete pipeline: ETL, EDA, Cohort, and RFM
```

---

## 6. Environment Setup & Execution

### Prerequisites
* Python 3.9 or higher
* PostgreSQL (v13+) or MySQL (v8.0+)
* Microsoft Power BI Desktop

### Installation
Clone the repository and set up a local virtual environment:

```bash
git clone [https://github.com/anhduonghong/ecommerce-customer-analytics.git](https://github.com/anhduonghong/ecommerce-customer-analytics.git)
cd ecommerce-customer-analytics

python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

## 7. Database Configuration via Environment Variables

The analytics pipeline abstracts database credentials into environment variables using `python-dotenv` and `SQLAlchemy`.

### Configuration Steps
1. Duplicate `.env.example` to create a local `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Populate `.env` with database connection parameters:
   ```ini
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=database_name
   DB_USER=root
   DB_PASSWORD=your_password
   ```
   *For PostgreSQL environments, set `DB_PORT=5432`.*

### Connection Implementation
The database engine is initialized programmatically within `notebooks/customer_analysis.ipynb`:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print("Database connection successfully verified.")
```

---

## 8. Execution Instructions

1. **Pipeline Execution:** Run all cells in `notebooks/customer_analysis.ipynb` to ingest raw data, execute cleaning and transformations, generate analytical metrics, and populate the target database.
2. **Dashboard Initialization:** Open `dashboard/Ecommerce_Customer_Segmentation.pbix` in Power BI Desktop. Point data source credentials to your local database instance to update the visualizations across the three report pages:
   * Page 1: Executive KPI Overview
   * Page 2: Cohort Retention Matrix & Drop-off Funnel
   * Page 3: RFM Behavioral Distribution & Account Drilldown

---

## 9. License & Attribution

* **Dataset Source:** [UCI Machine Learning Repository - Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
* **Author:** Duong Hong Anh ([@anhduonghong](https://github.com/anhduonghong))
* **License:** Distributed under the MIT License.


# E-Commerce Customer Analytics & Retention Strategy

## Project Overview

In e-commerce, sustainable growth cannot rely solely on customer acquisition while losing buyers after their first purchase.

This project establishes an automated analytics pipeline and business intelligence system designed to unpack customer purchase journeys, locate structural lifecycle drop-offs, and turn raw transactional logs into targeted retention tactics for Marketing and Operations.

---

## Dataset Overview Online Retail II

### Business Context
The dataset is sourced from the UCI Machine Learning Repository, capturing actual transactions from a UK based online retailer specializing in gifts, novelty homeware, and decor. The store serves both individual retail consumers and small wholesale clients purchasing products in bulk.

### Data Scope and Granularity
This study focuses on a 6 month continuous operational window from January 4, 2011 to June 30, 2011[cite: 10]:

* Raw Extract: Comprises 203,422 operational transaction lines across 8 core fields including InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, and Country[cite: 10].
* Cleaned Base: After eliminating records with missing customer IDs, handling cancelled orders, and removing unit price corrections, the pipeline isolates 146,478 verified purchase records[cite: 10].
* Business Scale: The active dataset accounts for 2,724 unique customers, 7,402 completed orders, 3,119 active SKUs, generating 3,421,091.76 GBP in gross revenue at an Average Order Value of 462.18 GBP[cite: 10].

### Analytical Value
* Hybrid Customer Personas: The presence of both low frequency individual shoppers and high volume wholesale buyers provides clear behavioral variance, ideal for 5 tier quantile RFM segmentation[cite: 10, 14].
* Lifecycle Tracking: Continuous daily timestamps enable exact measurement of customer retention curves and identify organic repurchase rhythms across monthly acquisition cohorts[cite: 10, 11].
## Target Business Questions

This project answers four core questions essential for customer retention and revenue growth:

1. **Where is the primary customer churn cliff?**  
   Pinpointing the exact month when churn peaks so proactive interventions can take place before accounts go cold.

2. **What is the natural repurchase rhythm?**  
   Tracking repurchase cycles across monthly cohorts to align lifecycle messaging and incentives with organic buying patterns.

3. **Which customer segments generate the majority of revenue?**  
   Segmenting accounts by Recency, Frequency, and Monetary value to isolate high-value champions from slipping accounts.

4. **Which products drive repeat purchases and baseline revenue?**  
   Applying Pareto analysis to identify key revenue-generating items and improve cross-selling opportunities.

---

## Core Business Insights & Strategic Impact

Across 146,478 validated transactions and 2,724 distinct customer profiles, analysis revealed four central operational opportunities:

### 1. Month 1 Churn Cliff
* **Finding:** Retention drops steeply from 100% to between 16.3% and 35.4% at Month 1 (M1), showing that 65% to 75% of new buyers do not return within their first 30 days.
* **Action:** Deploy automated post-purchase onboarding workflows and second-purchase incentives during Days 14 to 30 to secure early repeat orders.

### 2. Repurchase Resurgence Window
* **Finding:** Retention rates rebound between Months 2 and 4, rising from 23% back up to 34%–45.7% (notably within the January and February cohorts). Customers follow a 60 to 120-day replenishment rhythm rather than monthly repeat orders.
* **Action:** Trigger automated replenishment alerts and targeted promotions around Days 40 to 50 to meet customers at their natural buying window.

### 3. Revenue Concentration (Pareto Principle)
* **Finding:** The Champions (13.4%) and Loyal Customers (20.4%) segments combine to represent 33.8% of the user base but produce nearly 70% of total revenue. Conversely, At-Risk and Hibernating accounts make up 38.9% of customers while contributing minimal cash flow.
* **Action:** Protect top accounts with dedicated VIP loyalty programs, while running targeted, low-cost win-back campaigns on At-Risk accounts rather than unsegmented discounting.

### 4. Product Pareto Performance
* **Finding:** Top 19.8% of active SKUs generate 80% of total store revenue, anchored by key home decor and display pieces.
* **Action:** Maintain strict safety stock levels for the top 20% SKU tier to eliminate stockout risk, and create bundles pairing fast-moving goods with higher-margin accessories.

---

## System Architecture

```text
Raw Daily CSVs (data/incoming)
               │
               ▼
   Python Validation & Cleaning (Pandas)
               │
               ▼
   MySQL Database Ingestion (SQLAlchemy / Batch Inserts)
               │
               ▼
   Automated Analytics Processing (Cohort SQL & RFM Logic)
               │
               ▼
   Aggregated Tables & Visual Assets (data/processed, images)
               │
               ▼
   Interactive Executive Dashboards (Power BI)
```

1. **Extraction & Transformation:** Cleans cancellation invoices, removes missing customer records, parses timestamps, and builds clean analytical tables.
2. **Database Ingestion:** Loads validated transactions into MySQL using batch operations (`chunksize=5000`) for memory efficiency.
3. **Analytics Engine:** Computes monthly retention matrices using SQL window functions (`FIRST_VALUE`, `PERIOD_DIFF`) and runs quantile-based RFM scoring (1 to 5).
4. **Task Orchestration:** Runs automated daily updates via Windows Task Scheduler and batch scripts using a zero-touch incoming/archive queue pattern.
5. **Business Intelligence:** Exports clean reporting tables directly into Power BI to deliver executive-level performance tracking.

---

## Tech Stack

* **Data Processing & Analytics:** Python (Pandas, NumPy, SQLAlchemy, PyMySQL, Matplotlib, Seaborn, Squarify)
* **Database:** MySQL Server
* **Automation:** Windows Task Scheduler, Batch Scripting
* **Visualization:** Power BI Desktop

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/anhduonghong/ecommerce-customer-analytics.git](https://github.com/anhduonghong/ecommerce-customer-analytics.git)
   cd ecommerce-customer-analytics
   ```

2. **Set up the virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

3. **Configure environment variables:**
Create a `.env` file in the project root directory based on the provided template:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=retail_db
```

4. **Run the pipeline manually:**
Execute the batch script to load records, compute analytical tables, and export processed outputs:

```cmd
run_pipeline.bat
```

5. **Automate daily runs via Windows Task Scheduler:**
To establish a fully automated recurring pipeline:
* Open Windows Task Scheduler and click **Create Basic Task**
* Set the trigger frequency to **Daily** at your preferred time (example 07:00 AM).
* Select **Start a program** as the action.
* In the **Program/script** field, browse to `run_pipeline.bat`.
* In the **Start in (optional)** field, provide the absolute path to your project root folder (critical for resolving relative file paths).
* Save the task to let the pipeline execute automatically without manual intervention.

6. **View Power BI reports:**
Open `dashboard/Ecommerce_Customer_Analytics.pbix` in Power BI Desktop and select **Refresh** to sync the dashboard with the latest processed data.

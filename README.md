# E-Commerce Customer Analytics & Retention Strategy

## Project Overview

In e-commerce, sustainable growth cannot rely solely on customer acquisition while losing buyers after their first purchase[cite: 10, 11].

This project establishes an automated analytics pipeline and business intelligence system designed to unpack customer purchase journeys, locate structural lifecycle drop-offs, and turn raw transactional logs into targeted retention tactics for Marketing and Operations[cite: 10, 11].

---

## Target Business Questions

This project answers four core questions essential for customer retention and revenue growth:

1. **Where is the primary customer drop-off cliff?**  
   Pinpointing the exact month when churn peaks so proactive interventions can take place before accounts go cold[cite: 11].

2. **What is the natural repurchase rhythm?**  
   Tracking repurchase cycles across monthly cohorts to align lifecycle messaging and incentives with organic buying patterns[cite: 10, 11].

3. **Which customer segments generate the majority of revenue?**  
   Segmenting accounts by Recency, Frequency, and Monetary value to isolate high-value champions from slipping accounts[cite: 10, 15, 16].

4. **Which products drive repeat purchases and baseline revenue?**  
   Applying Pareto analysis to identify key revenue-generating items and improve cross-selling opportunities[cite: 14].

---

## Core Business Insights & Strategic Impact

Across 146,478 validated transactions and 2,724 distinct customer profiles, analysis revealed four central operational opportunities[cite: 10, 11]:

### 1. Month 1 Churn Cliff
* **Finding:** Retention drops steeply from 100% to between 16.3% and 35.4% at Month 1 (M1), showing that 65% to 75% of new buyers do not return within their first 30 days[cite: 10, 11].
* **Action:** Deploy automated post-purchase onboarding workflows and second-purchase incentives during Days 14 to 30 to secure early repeat orders[cite: 10, 11].

### 2. Repurchase Resurgence Window
* **Finding:** Retention rates rebound between Months 2 and 4, rising from 23% back up to 34%–45.7% (notably within the January and February cohorts)[cite: 10, 11]. Customers follow a 60 to 120-day replenishment rhythm rather than monthly repeat orders[cite: 10].
* **Action:** Trigger automated replenishment alerts and targeted promotions around Days 40 to 50 to meet customers at their natural buying window[cite: 10].

### 3. Revenue Concentration (Pareto Principle)
* **Finding:** The Champions (13.4%) and Loyal Customers (20.4%) segments combine to represent 33.8% of the user base but produce nearly 70% of total revenue[cite: 10, 16]. Conversely, At-Risk and Hibernating accounts make up 38.9% of customers while contributing minimal cash flow[cite: 10, 16].
* **Action:** Protect top accounts with dedicated VIP loyalty programs, while running targeted, low-cost win-back campaigns on At-Risk accounts rather than unsegmented discounting[cite: 10].

### 4. Product Pareto Performance
* **Finding:** Top 19.8% of active SKUs generate 80% of total store revenue, anchored by key home decor and display pieces[cite: 14].
* **Action:** Maintain strict safety stock levels for the top 20% SKU tier to eliminate stockout risk, and create bundles pairing fast-moving goods with higher-margin accessories[cite: 14].

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

1. **Extraction & Transformation:** Cleans cancellation invoices, removes missing customer records, parses timestamps, and builds clean analytical tables[cite: 10].
2. **Database Ingestion:** Loads validated transactions into MySQL using batch operations (`chunksize=5000`) for memory efficiency[cite: 10].
3. **Analytics Engine:** Computes monthly retention matrices using SQL window functions (`FIRST_VALUE`, `PERIOD_DIFF`) and runs quantile-based RFM scoring (1 to 5)[cite: 10].
4. **Task Orchestration:** Runs automated daily updates via Windows Task Scheduler and batch scripts using a zero-touch incoming/archive queue pattern[cite: 1, 3, 5].
5. **Business Intelligence:** Exports clean reporting tables directly into Power BI to deliver executive-level performance tracking[cite: 3, 5, 13].

---

## Tech Stack

* **Data Processing & Analytics:** Python (Pandas, NumPy, SQLAlchemy, PyMySQL, Matplotlib, Seaborn, Squarify)[cite: 10]
* **Database:** MySQL Server[cite: 10]
* **Automation:** Windows Task Scheduler, Batch Scripting[cite: 1, 3]
* **Visualization:** Power BI Desktop[cite: 11, 13, 14, 15]

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
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root based on `.env.example`:
   ```text
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=retail_db
   ```

4. **Run the automated pipeline:**
   Execute the batch script to load records, calculate analytical tables, and export processed files[cite: 3]:
   ```cmd
   run_pipeline.bat
   ```

5. **View Power BI reports:**
   Open `dashboard/Ecommerce_Customer_Analytics.pbix` in Power BI Desktop and select **Refresh** to sync the latest data[cite: 2, 5].

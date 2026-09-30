"""DAG Airflow. Chạy Airflow qua Docker hoặc WSL2 (Airflow không chạy native trên Windows).
Mount thư mục project vào container tại /opt/airflow/project và thêm vào PYTHONPATH."""
import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow/project")  # sửa theo nơi bạn mount project

from airflow import DAG
try:
    from airflow.providers.standard.operators.python import PythonOperator  # Airflow 3
except ImportError:
    from airflow.operators.python import PythonOperator  # Airflow 2

from src.pipeline import run_analytics, run_etl

with DAG(
    dag_id="customer_report_daily",
    start_date=datetime(2026, 10, 1),
    schedule="0 7 * * *",  # 07:00 mỗi ngày
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["retail", "rfm", "cohort"],
) as dag:
    etl_task = PythonOperator(task_id="load_new_data", python_callable=run_etl)
    analytics_task = PythonOperator(task_id="build_cohort_rfm", python_callable=run_analytics)
    etl_task >> analytics_task

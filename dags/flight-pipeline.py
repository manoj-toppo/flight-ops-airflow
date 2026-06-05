import sys
from pathlib import Path
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

AIRFLOW_HOME = Path("/opt/airflow")

if str(AIRFLOW_HOME) not in sys.path:
    sys.path.insert(0, str(AIRFLOW_HOME))

from scripts.bronze_ingest import run_bronze_ingestion
from scripts.silver_transform import run_silver_transform
from scripts.gold_aggregate import run_gold_aggregate
from scripts.load_gold_to_snowflakes import load_gold_to_snowflakes


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="flights_ops_medallion_pipe",
    default_args=default_args,
    start_date=datetime(2025, 12, 1),  # use a past date for testing
    schedule_interval="*/30 * * * *",
    catchup=False,
    tags=["flights", "medallion"],
    description="Bronze + Silver pipeline for flights data",
) as dag:
    bronze_task = PythonOperator(
        task_id="bronze_ingestion",
        python_callable=run_bronze_ingestion,
    )

    silver_task = PythonOperator(
        task_id="silver_transform",
        python_callable=run_silver_transform,
    )
    
    gold_task = PythonOperator(
    task_id="gold_aggregate",
    python_callable=run_gold_aggregate,
)

    load_to_snowflakes = PythonOperator(
    task_id="load_gold_to_snowflake",
    python_callable=load_gold_to_snowflakes,
)

    bronze_task >> silver_task >> gold_task >> load_to_snowflakes


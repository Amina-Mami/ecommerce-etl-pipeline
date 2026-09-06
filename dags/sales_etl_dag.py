

from __future__ import annotations

import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow/src")

CSV_PATH = "/opt/airflow/src/data/erp_export.csv"


def run_etl_pipeline():
    import pandas as pd
    from extract import extract_from_source_db, extract_from_csv
    from transform import transform_orders_from_db, transform_orders_from_csv
    from load import load_fact_sales

    db_raw = extract_from_source_db()
    db_transformed = transform_orders_from_db(db_raw)

    csv_raw = extract_from_csv(CSV_PATH)
    csv_transformed = transform_orders_from_csv(csv_raw)

    combined = pd.concat([db_transformed, csv_transformed], ignore_index=True)
    load_fact_sales(combined)


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="sales_etl_pipeline",
    description="Pipeline ETL des ventes e-commerce (DB + CSV -> DWH)",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "sales", "portfolio"],
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_etl_pipeline",
        python_callable=run_etl_pipeline,
    )
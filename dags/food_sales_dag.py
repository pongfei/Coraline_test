from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def ingest():
    from pipeline import run
    run()

def build_cat_reg():
    import psycopg2
    import config

    sql_text = open('/opt/airflow/sql/create_cat_reg.sql').read()

    conn = psycopg2.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,

    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(sql_text)
    conn.close()

with DAG(
    dag_id = 'food_sales_dag',
    start_date = datetime(2024,1,1),
    schedule = '@daily',
    catchup = False
) as dag:

    ingest_task = PythonOperator(
    task_id="ingest",
    python_callable=ingest,
    )

    build_cat_reg_task = PythonOperator(
    task_id="build_cat_reg",
    python_callable=build_cat_reg,
    )

    ingest_task >> build_cat_reg_task

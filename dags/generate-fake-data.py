# dags/fake_data_job.py
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'generate_fake_pos_data',
    default_args=default_args,
    schedule_interval='*/10 * * * *',  # 每 10 分鐘
    catchup=False,
    tags=['pos', 'fake-data']
) as dag:

    generate_data = KubernetesPodOperator(
        task_id='generate_fake_data',
        name='generate-fake-data',
        namespace='airflow',
        image='generate-fake-data:0.0.1',
        image_pull_policy='IfNotPresent',
        is_delete_operator_pod=True,
        get_logs=True,
        env_vars={
            'PGHOST': 'postgres.prod.svc.cluster.local',
            'PGUSER': 'airflow_user',
            'PGPASSWORD': 'airflow_pass',
            'PGDATABASE': 'orders',
            'PGPORT': '5432'
        }
    )

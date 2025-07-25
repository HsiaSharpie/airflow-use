from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.kubernetes.secret import Secret


aws_access_key_id_secret = Secret(
    deploy_type="env",              # 以環境變數形式掛載
    deploy_target="AWS_ACCESS_KEY_ID",  # 這是 Pod 內看到的變數名
    secret="aws-creds",             # Kubernetes Secret 名稱
    key="AWS_ACCESS_KEY_ID",       # Secret 中的 key
)

aws_secret_access_key_secret = Secret(
    deploy_type="env",
    deploy_target="AWS_SECRET_ACCESS_KEY",
    secret="aws-creds",
    key="AWS_SECRET_ACCESS_KEY",
)


with DAG(
    dag_id="secrets_test",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    print_env = KubernetesPodOperator(
        task_id="print-env",
        name="print-env",
        namespace="airflow",
        image="test-env-image:0.0.3",
        secrets=[aws_access_key_id_secret, aws_secret_access_key_secret],
        get_logs=True,
        is_delete_operator_pod=True,
    )

    print_env
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.bash import BashOperator
from datetime import datetime



with DAG(
    dag_id="simple_k8s_pod_operator",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    hello_task = KubernetesPodOperator(
        task_id="hello_k8s_pod",
        name="hello-k8s-pod",
        namespace="default",
        image="alpine:3.18",
        cmds=["sh", "-c"],
        arguments=["echo Hello from K8s Pod"],
        get_logs=True,
        is_delete_operator_pod=True,
    )

    bash_task = BashOperator(
        task_id="local_bash_task",
        bash_command="echo This runs after the K8s pod"
    )

    hello_task >> bash_task
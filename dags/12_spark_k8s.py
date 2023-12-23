from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from datetime import datetime

# Define the DAG
with DAG('spark_submit_sample',
          description='A simple DAG', 
          schedule_interval='0 0 * * *', 
          start_date=datetime(2023, 7, 1), 
          catchup=False) as dag:

    submit = SparkKubernetesOperator(
        task_id='spark_pi_submit',
        namespace='spark-operator',
        application_file="sample.yaml",
        kubernetes_conn_id='eks-flab',
        do_xcom_push=True,
    )

    submit 
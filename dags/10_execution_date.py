from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

def print_execution_date(execution_date, ds, **kwargs):
    print(f"kwargs: {kwargs}")
    print(f"ds: {ds}")
    print(f"datetime: {execution_date}")


with DAG(
    dag_id="print_execution_date",
    start_date=days_ago(2),
    schedule="*/2 * * * *",
    default_args={"retries": 1},
    catchup=False
):
    print_execution_date_task = PythonOperator(
        task_id='print_execution_date_task',
        python_callable=print_execution_date,
        provide_context=True)

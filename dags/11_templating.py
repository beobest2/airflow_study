from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

def print_execution_date(execution_date, ds, **kwargs):
    print(f"kwargs: {kwargs}")
    print(f"ds: {ds}")
    print(f"datetime: {execution_date}")

def sum_numbers1(*args):
    total = 0
    for val in args:
        total += val
    return total

def sum_numbers2(**kwargs):
    dag_run = kwargs["dag_run"]
    print(dag_run.conf)
    args = dag_run.conf.get('numbers', [])
    total = 0
    for val in args:
        total += val
    return total

with DAG(
    dag_id="templating",
    start_date=days_ago(2),
    schedule="@daily",
    default_args={"retries": 1},
    catchup=False,
    render_template_as_native_obj=True, # Render templates using Jinja NativeEnvironment
):
    print_execution_date_task = PythonOperator(
        task_id='print_execution_date_task',
        python_callable=print_execution_date,
        provide_context=True)
    
    print_days = BashOperator(
        task_id="print_days",
        bash_command="echo Days since {{ ds_nodash }}"
    )

    sum_numbers_task = PythonOperator(
        task_id="sum_numbers1",
        python_callable=sum_numbers1,
        op_args="{{ dag_run.conf['numbers'] }}",
    )

    sum_numbers_task2 = PythonOperator(
        task_id="sum_numbers2",
        python_callable=sum_numbers2,
        provide_context=True,
    )

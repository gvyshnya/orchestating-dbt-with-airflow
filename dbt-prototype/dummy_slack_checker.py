from datetime import datetime, timedelta
from airflow import DAG
from cosmos import DbtTaskGroup, ProfileConfig, ExecutionConfig, ProjectConfig, RenderConfig, ExecutionMode
from cosmos.constants import TestBehavior
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy import DummyOperator
import os

from dependencies.callback_notifier import CallbackNotifier

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_retry_callback': CallbackNotifier().on_retry_callback,
    'on_failure_callback': CallbackNotifier().on_failure_callback,
    'on_success_callback': CallbackNotifier().on_success_callback,
}

# Define the DAG
with DAG(
    dag_id="slack_note_test",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    # Start Task
    start = EmptyOperator(task_id="start")
    
    dag_success_check = DummyOperator(
        task_id="dag_success_check",
        retries=0,
    )
    
    # End Task
    end = EmptyOperator(task_id="end")
    
    start >> dag_success_check >> end
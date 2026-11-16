import datetime
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG, configuration
from airflow_dbt.hooks.dbt_hook import DbtCliHook
from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator

default_args = {
  'dir': '/home/airflow/gcs/dags',
  'profiles_dir': '/home/airflow/gcs/data/profiles',
  'dbt_bin': '/usr/bin/dbt',
  'owner': 'airflow',
  'models': 'tag:raw__coreapp__fake',
  'depends_on_past': False,
  'start_date': days_ago(0),
  'email': ['fake@fake-vinaj-project.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=5)
}

with DAG(dag_id='dbt', default_args=default_args, schedule_interval='@daily') as dag:

  dbt_run = DbtRunOperator(
    task_id='dbt_run',
  )

  dbt_test = DbtTestOperator(
    task_id='dbt_test',
    retries=0,  # Failing tests would fail the task, and we don't want Airflow to try again
  )

  dbt_run >> dbt_test


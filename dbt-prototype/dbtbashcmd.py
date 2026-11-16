# inspired by https://medium.com/globant/automating-pipelines-with-dbt-and-airflow-using-cosmos-bb0b0ffc025c

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
# Define the DAG
with DAG(
    dag_id="dbt_transformations_bash",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    # Task 1: Start Task
    start = EmptyOperator(task_id="start")
    # Task 2: Copy dbt project and profiles.yml from the Airflow bucket
    copy_dbt_project = BashOperator(
        task_id="copy_dbt_project",
        bash_command="""
        mkdir -p /home/airflow/dbt_workspace &&
        gsutil cp -r gs://europe-west3-production-com-8b0dc778-bucket/dags/my_dbt_project /home/airflow/dbt_workspace &&
        gsutil cp gs://europe-west3-production-com-8b0dc778-bucket/dags/profiles/profiles.yml /home/airflow/dbt_workspace/profiles.yml
        """)
    # Task 4: Run all raw__coreapp__doctors dbt models sequentially
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        $(which dbt) run \
        --project-dir /home/airflow/dbt_workspace/my_dbt_project \
        --profiles-dir /home/airflow/dbt_workspace
        --select tag:raw__coreapp__doctors
        """
    )
    # Task 6: End Task
    end = EmptyOperator(task_id="end")
    # Set Task Execution Order
    start >> copy_dbt_project >> dbt_run >> end
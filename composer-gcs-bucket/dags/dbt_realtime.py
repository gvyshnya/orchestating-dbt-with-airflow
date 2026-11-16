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
    'owner': "airflow",
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_retry_callback': CallbackNotifier().on_retry_callback,
    'on_failure_callback': CallbackNotifier().on_failure_callback,
}

# fetch environment variables from Airflow variables
env_vars = {
    'DBT_ENV': os.getenv('DBT_ENV', 'production'), 
    'DBT_BIGQUERY_PROJECT': os.getenv('DBT_BIGQUERY_PROJECT', 'fake-vinaj-project'),
    'DBT_BIGQUERY_DATASET': os.getenv('DBT_BIGQUERY_DATASET', 'dbt'),
    'DBT_BIGQUERY_PREFIX_RAW': os.getenv('DBT_BIGQUERY_PREFIX_RAW', 'raw'),
    'DBT_BIGQUERY_PREFIX_DERIVED': os.getenv('DBT_BIGQUERY_PREFIX_DERIVED', 'derived'),
    'DBT_BIGQUERY_PREFIX_MARTS': os.getenv('DBT_BIGQUERY_PREFIX_MARTS', 'marts'),
    'DBT_BIGQUERY_PREFIX_UTIL': os.getenv('DBT_BIGQUERY_PREFIX_UTIL', 'util'),
    'DBT_BIGQUERY_LOCATION': os.getenv('DBT_BIGQUERY_LOCATION', 'europe-west3'),
    'DBT_THREADS': os.getenv('DBT_THREADS', '2'),
    'DBT_HASH_SALT': os.getenv('DBT_HASH_SALT', 'blah-blah-blah'),
        'DBT_BIGQUERY_PREFIX_TESTFAILS': os.getenv('DBT_BIGQUERY_PREFIX_TESTFAILS', 'testfailures'),
}

# Define the DAG
# Run every 15 min (6-23 interval, Mon-Fri)
with DAG(
    dag_id="dbt_cosmos_realtime",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    #schedule_interval='15,30,45 6-23 * * 1-5',
    schedule_interval=None,
    catchup=False,
) as dag:
    # Start Task
    start = EmptyOperator(task_id="start")
    # Define Profile Configuration (BigQuery connection details)
    profile_config = ProfileConfig(
        profile_name="bigquery_dwh",  # Matches the profile name in profiles.yml
        target_name=env_vars["DBT_ENV"],   # Matches the target in profiles.yml
        profiles_yml_filepath="/home/airflow/gcs/data/profiles/profiles.yml",  # Path to profiles.yml
    )
    # Define Execution Configuration (Path to dbt and options)
    execution_config = ExecutionConfig(
        dbt_executable_path="/usr/bin/dbt",  # Path to dbt binary
    )
    # Define Project Configuration
    project_config = ProjectConfig(
        dbt_project_path="/home/airflow/gcs/dags/dbt",  # Path to dbt project
        env_vars=env_vars, #environment variables
        
    )
    # Define render config for raw-related jobs
    raw_render_config = RenderConfig(
           select=[
            "tag:raw,tag:production,tag:schedule__realtime",
           ],
           test_behavior=TestBehavior.NONE,
    )
    # Define render config for derived-related jobs
    derived_render_config = RenderConfig(
           select=[
            "tag:derived,tag:schedule__realtime,tag:production",
           ],
           test_behavior=TestBehavior.NONE,
    )
    # Define render config for marts-related jobs
    marts_render_config = RenderConfig(
           select=[
            "tag:marts,tag:schedule__realtime,tag:production", #intersection
           ],
           exclude=["tag:archive", "tag:schedule__never"], # union
           test_behavior=TestBehavior.NONE,
    )
    
    # Create the DbtTaskGroups (raw, derived, marts)
    # with profile and execution configs
    dbt_tg_raw = DbtTaskGroup(
        group_id="dbt_raw_transformations",
        render_config=raw_render_config,
        project_config=project_config,  # Project configuration object
        profile_config=profile_config,  # Profile configuration object
        execution_config=execution_config,  # Execution configuration object
        operator_args={
            "full_refresh": False,
        },
    )
    dbt_tg_derived = DbtTaskGroup(
        group_id="dbt_derived_transformations",
        render_config=derived_render_config,
        project_config=project_config,  # Project configuration object
        profile_config=profile_config,  # Profile configuration object
        execution_config=execution_config,  # Execution configuration object
        operator_args={
            "full_refresh": False,
        },
    )
    dbt_tg_marts = DbtTaskGroup(
        group_id="dbt_marts_transformations",
        render_config=marts_render_config,
        project_config=project_config,  # Project configuration object
        profile_config=profile_config,  # Profile configuration object
        execution_config=execution_config,  # Execution configuration object
        operator_args={
            "full_refresh": False,
        },
    )
    
    dag_success_check = DummyOperator(
        task_id="dbt_realtime_success_check",
        retries=0,
        on_success_callback=CallbackNotifier().on_success_callback
    )
      
    # End Task
    end = EmptyOperator(task_id="end")
    
    # Set Task Order
    start >> dbt_tg_raw >> dbt_tg_derived >> dbt_tg_marts >> dag_success_check >> end
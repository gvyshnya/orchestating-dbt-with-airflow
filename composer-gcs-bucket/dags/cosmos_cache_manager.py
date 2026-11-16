from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

from cosmos.cache import delete_unused_dbt_ls_cache, delete_unused_dbt_ls_remote_cache_files

DAYS=1

with DAG(
    dag_id="cosmos_cleanup_dag_demo",
    schedule="5 5 * * 6",  # Runs every Saturday at 5.05 am
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=[],
):

    @task()
    def clear_db_ls_cache(session=None):
        """
        Delete the dbt ls cache that has not been used for the last five days.
        """
        delete_unused_dbt_ls_cache(max_age_last_usage=timedelta(days=DAYS))

    clear_db_ls_cache()

    @task()
    def clear_db_ls_remote_cache(session=None):
        """
        Delete the dbt ls remote cache files that have not been used for the last five days.
        """
        delete_unused_dbt_ls_remote_cache_files(max_age_last_usage=timedelta(days=DAYS))

    clear_db_ls_remote_cache()
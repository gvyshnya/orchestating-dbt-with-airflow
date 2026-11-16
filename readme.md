# Introduction

This repo contains the materials to demonstrate one of the possible approaches to schedule running the stand-alone set of dbt transformations with Apache Airflow.

The essence of this approach it to utilize Astronomer Cosmos lib to facilitate it. Such an approach works for both the stand-along Airflow instances and the managed instances inside Google Cloud Composer.

*Notes:* 

- The standard set of Airflow dbt operators from *airflow_dbt^ did not work in the managed Google Cloud Composer environment
- The final destination of the data marts was GCP BigQuery 

# Files and Folders

The following subfolders are within this repo
- `production` subfolder contains the code of DAGs that utilize Astronomer Cosmos lib to run the scheduled DBT jobs (increemental hourly updates, full reloads of data, special-purpose runs with dbt tests applied etc.)
- `dbt-prototype` contains the brief prototypes for other orchestration options beyond cosmos (unfortunately, they did not fly in the managed Airflow environment inside Google Cloud Composer)
- `composer-gcs-bucket` shows the structure of the data within the Google Storage Bucket used by the respective Google Cloud Composer environment (it contains both the DAG scripts for Airflow and a replica of the dbt transformation project)
from datetime import datetime
from pathlib import Path
import os
import shutil
from airflow.models import DAG
from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from airflow.operators.python import PythonOperator


def save_clean_log(context):
    """
    Finds the log file for the task and copies it to a 'flat' folder
    renamed as {task_id}.txt for easy reading.
    """
    # Get details from the context
    ti = context['task_instance']
    dag_id = ti.dag_id
    task_id = ti.task_id
    run_id = ti.run_id
    try_number = ti.try_number - 1 # Adjust for 0-indexing if needed

    # Construct the internal Airflow log path
    # Standard format: /opt/airflow/logs/dag_id/task_id/run_id/attempt.log
    source_log = f"/opt/airflow/logs/{dag_id}/{task_id}/{run_id}/{try_number}.log"
    
    # Define where you want the clean file (Ensure this folder is mounted in K8s!)
    target_dir = "/opt/airflow/logs/flat_dbt_logs"
    os.makedirs(target_dir, exist_ok=True)
    
    target_file = f"{target_dir}/{task_id}.txt"

    # Copy the file
    if os.path.exists(source_log):
        shutil.copy(source_log, target_file)
        print(f"Log saved to: {target_file}")
    else:
        print(f"Could not find source log: {source_log}")



# Path to your dbt project
DBT_PROJECT_PATH = Path("/opt/airflow/dbt")

# Snowflake Connection (Ideally set this in Airflow UI)
profile_config = ProfileConfig(
    profile_name="tasty_bytes",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_default", 
        profile_args={"database": "TASTY_BYTES_DBT_DB", "schema": "DEV"},
    )
)

# 2. Attach this callback to your DAG
tasty_bytes_dag = DbtDag(
    project_config=ProjectConfig(DBT_PROJECT_PATH),
    profile_config=profile_config,
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="tasty_bytes_dbt_transformation",
    
    on_success_callback=save_clean_log, 
    on_failure_callback=save_clean_log,
)


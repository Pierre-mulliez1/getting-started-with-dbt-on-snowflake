from datetime import datetime
from pathlib import Path
import sys
import os
import shutil
from airflow.models import DAG
# CHANGED: Import DbtTaskGroup instead of DbtDag
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from airflow.operators.python import PythonOperator

# Add path for custom operators
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
from operators.success_operator import SuccessLogOperator

def save_clean_log(context):
    """
    Finds the log file for the task and copies it to a 'flat' folder
    renamed as {task_id}.txt for easy reading.
    """
    ti = context['task_instance']
    dag_id = ti.dag_id
    task_id = ti.task_id
    run_id = ti.run_id
    try_number = ti.try_number - 1 

    # Construct the internal Airflow log path
    source_log = f"/opt/airflow/logs/{dag_id}/{task_id}/{run_id}/{try_number}.log"
    
    # Define where you want the clean file (Ensure this folder is mounted in K8s!)
    target_dir = "/opt/airflow/logs/flat_dbt_logs"
    os.makedirs(target_dir, exist_ok=True)
    
    target_file = f"{target_dir}/{task_id}.txt"

    if os.path.exists(source_log):
        shutil.copy(source_log, target_file)
        print(f"Log saved to: {target_file}")
    else:
        print(f"Could not find source log: {source_log}")

# Path to your dbt project
DBT_PROJECT_PATH = Path("/opt/airflow/dbt")

# Snowflake Connection
profile_config = ProfileConfig(
    profile_name="tasty_bytes",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_default", 
        profile_args={"database": "TASTY_BYTES_DBT_DB", "schema": "DEV"},
    )
)

# Define the DAG context explicitly so we can chain operators
with DAG(
    dag_id="tasty_bytes_dbt_transformation",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    on_success_callback=save_clean_log, 
    on_failure_callback=save_clean_log
) as dag:

    # 1. The dbt Task Group (Cosmos)
    # CHANGED: Used DbtTaskGroup to allow embedding inside a DAG
    dbt_transformation = DbtTaskGroup(
        group_id="dbt_transformation",   # Required: Unique ID for the group
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        render_config=RenderConfig(emit_datasets=False),
       
    )

    # 2. The Custom Operator Task
    send_success_signal = SuccessLogOperator(
        task_id="send_custom_success_log",
        custom_message="The Tasty Bytes ETL has finished processing incremental data."
    )

    # 3. Define the Dependency
    dbt_transformation >> send_success_signal
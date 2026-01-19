from datetime import datetime
from pathlib import Path
from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

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

tasty_bytes_dag = DbtDag(
    project_config=ProjectConfig(DBT_PROJECT_PATH),
    profile_config=profile_config,
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="tasty_bytes_dbt_transformation",
)
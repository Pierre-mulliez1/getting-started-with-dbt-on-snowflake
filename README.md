# Getting Started with dbt on Snowflake

## Overview

Use of free dbt sample project to locally launch a Airflow managed dataflow through DOCKER 
tasty_bytes_orchestration/
├── dags/
│   └── tasty_bytes_dag.py        # The Airflow DAG created
├── dbt/
│   ├── dbt_project.yml           # sample dbt config
│   ├── models/                   # sample SQL models
│   ├── seeds/
│   ├── snapshots/
│   ├── tests/
│   └── macros/
├── Dockerfile                    # The custom Airflow + dbt image created
└── docker-compose.yaml           # The orchestration file created

This repository contains an example dbt project to get you started with dbt on Snowflake.
# Tasty Bytes: Modern Data Platform on Kubernetes

A production-ready ELT pipeline orchestrating **dbt Core** transformations on **Snowflake** using **Apache Airflow**, fully containerized and deployed on **Kubernetes** (Docker Desktop).

##  Project Overview

This project implements a **Medallion Architecture** (Raw → Staging → Marts) for the [Snowflake Tasty Bytes dataset](https://github.com/dbt-labs/snowflake_frostbyte_tasty_bytes). It demonstrates how to move beyond simple Docker Compose setups into a scalable Kubernetes environment with automated monitoring and data quality checks.

### Key Features
* **Orchestration:** Airflow 2.7+ running on Kubernetes.
* **Transformation:** dbt Core integrated via `astronomer-cosmos` for task-granular lineage.
* **Infrastructure as Code:** Kubernetes manifests (`k8s-platform.yaml`) for immutable deployments.
* **Data Quality:** Custom generic tests (Regex validation) and automated failure alerts.
* **Observability:** Custom Python callbacks that extract flat log files from K8s pods to the local host for easy debugging.

---

##  Architecture

1.  **Airflow Scheduler/Webserver:** Runs as a Kubernetes Deployment.
2.  **Metadata Database:** Postgres running as a K8s Service.
3.  **Executor:** LocalExecutor (running dbt commands inside the pod).
4.  **Data Warehouse:** Snowflake (External).
5.  **Logs:** Volume-mounted "Bridge" syncing logs from K8s to Windows/Local.

---

##  Prerequisites

* **Docker Desktop** (with Kubernetes enabled).
* **Snowflake Account** (Standard or Trial).
* **Python 3.10+** (for local dev).
* **kubectl** (CLI tool for Kubernetes).

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/tasty_bytes_orchestration.git](https://github.com/YOUR_USERNAME/tasty_bytes_orchestration.git)
cd tasty_bytes_orchestration

### 2. Configuration of K8s  
# k8s-platform.yaml
stringData:
  # Format: snowflake://<user>:<password>@<org>-<account>/<db>/<schema>?warehouse=<wh>&role=<role>&account=<org>-<account>
  AIRFLOW_CONN_SNOWFLAKE_DEFAULT: "snowflake://admin:Pass123@MYORG-MYACCOUNT/TASTY_BYTES/DEV?warehouse=COMPUTE_WH&role=SYSADMIN&account=MYORG-MYACCOUNT"

volumes:
  - name: local-logs
    hostPath:
      # Replace 'YOUR_USER' and path accordingly
      path: /run/desktop/mnt/host/c/Users/YOUR_USER/tasty_bytes_orchestration/airflow_logs
      type: DirectoryOrCreate
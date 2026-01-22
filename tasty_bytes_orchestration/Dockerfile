# Base Image
FROM apache/airflow:2.7.2-python3.10

USER root
RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow
# Install dependencies
RUN pip install --no-cache-dir \
    dbt-snowflake \
    astronomer-cosmos \
    apache-airflow-providers-snowflake

# K8S CHANGE: Copy project files into the image
COPY --chown=airflow:root ./dags /opt/airflow/dags
COPY --chown=airflow:root ./dbt /opt/airflow/dbt
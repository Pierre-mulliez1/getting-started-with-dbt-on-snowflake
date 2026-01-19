FROM apache/airflow:2.7.2-python3.10

USER root
RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow
# Install dbt and cosmos
RUN pip install --no-cache-dir \
    dbt-snowflake \
    astronomer-cosmos \
    apache-airflow-providers-snowflake
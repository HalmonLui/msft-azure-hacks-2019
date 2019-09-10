# Pipelines

This directory contains all methods used for the data pipeline and data aggregation component of this project which utilises Python and MongoDB.

The code in this directory also makes use of Azure services such as Text Analytics, Web Search, and Image Search.

Dataflows were created with cron jobs running daily using the Apache Airflow platform. (Copies of the scripts are located in here as Airflow requres the DAGs to be in a root directory in the system).

## Dependencies
In order to run any of the scripts in this folder, please run the following line on your terminal (pip or pip3)

```bash
pip3 install -r requirements.txt
```

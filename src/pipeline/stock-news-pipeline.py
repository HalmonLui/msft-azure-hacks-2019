import datetime
import json

from airflow import DAG
from airflow import models
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.hooks.mongo_hook import MongoHook


DEFAULT_ARGS = {
    'start_date': datetime.datetime.today(),
    'email_on_retry': False,
    'email_on_failure': False,
    'retries': 3,
    'retry_delay': datetime.timedelta(minutes=30),

}

dag = DAG('Stock-News-Pipeline', default_args=DEFAULT_ARGS,
           schedule_interval=" 0 0 20 ? * * *",
           )


t1 = BashOperator(task_id='Stock-News-Agg', dag=dag, bash_command="python3 /Users/sonamghosh/Desktop/msft_azure_hackathon_2019/exploratory_analysis/msft-azure-hacks-2019/src/pipeline/create_tables.py")

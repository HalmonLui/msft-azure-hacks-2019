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
    'retry_delay': datetime.timedelta(minutes=60),

}

dag = DAG('Stock-Price-Pipeline', default_args=DEFAULT_ARGS,
           schedule_interval="0 0 21 ? * MON,TUE,WED,THU,FRI *",
           )


t1 = BashOperator(task_id='test', dag=dag, bash_command="python3 /Users/sonamghosh/Desktop/msft_azure_hackathon_2019/exploratory_analysis/msft-azure-hacks-2019/src/pipeline/utils.py")





"""
def airflow_grab_stock_data(ticker, start, end, **context):
    date_interval = '1d'
    start = convert_ds_to_unix(start)
    end = convert_ds_to_unix(end)
    res = requests.get(
        "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start}&period2={end}&interval={date_interval}".format(**locals()))
    data_json = res.json()['chart']['result'][0]
    dt = pd.Series(map(lambda x: arrow.get(x).datetime.replace(
        tzinfo=None), data_json['timestamp']), name='date')
    df = pd.DataFrame(data_json['indicators']['quote'][0], index=dt)
    df.index = df.index.normalize()
    df = df[['close']]
    # Use date as its own column instead of index
    df = df.reset_index()
    df['Ticker'] = data_json["meta"]["symbol"]
    # Add column that calculates % change between adj close and open for that day
    percentage_change = []
    for i, num in df['close'].iteritems():
        open = data_json["indicators"]["quote"][0]["open"][i]
        change = (num - open) / open * 100
        percentage_change.append(change)
    df['change'] = percentage_change

    context['ti'].xcom_push(key='data', value=df)



def load_to_db(dbname, table, **contxt):
    load_dotenv()
    data = context['ti'].xcom_pull(task_ids=['grab-data'], key='data')

    client = pymongo.MongoClient(os.getenv("MONGO_NORM_USER"))
    db = client[dbname][table]
    data = df.to_dict(orient='records')
    db.insert_many(data)


DEFAULT_ARGS = {
    'start_date': datetime.datetime(2019, 9, 9),
    'email_on_retry': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=5),

}

dag = DAG('StockTest', default_args=DEFAULT_ARGS,
           schedule_interval=datetime.timedelta(days=1),
           )


task1 = BashOperator(
    task_id="echo1",
    bash_command="echo Start scraping reddit.",
    dag=dag,
)

task2 = PythonOperator(
    task_id="grab-data",
    params={'ticker': 'AAPL', 'start': '2019-09-03', 'end': '2019-09-03'},
    python_callable=airflow_grab_stock_data,
    provide_context=True,
    dag=dag,
)

task3 = PythonOperator(
    task_id="load-db",
    params={'df': context['ti'].xcom_pull(task_ids=['grab-data'], key='data'),
            'dbname': 'test', 'table': 'aapl'},
    python_callable=load_to_db,
    provide_context=True,
    dag=dag,
)

task1 >> task2 >> task3
"""

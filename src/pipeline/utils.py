import pandas as pd
import numpy as np
import requests
import datetime
import arrow
import os

# Grab data from Yahoo Finance
def grab_data(ticker, date_range, date_interval):
    # @TODO: consider a ticker column
    res = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={date_range}&interval={date_interval}'.format(**locals()))
    data = res.json()['chart']['result'][0]
    return data


def transform_data(data_json):
    dt = pd.Series(map(lambda x: arrow.get(x).datetime.replace(
        tzinfo=None), data_json['timestamp']), name='date')
    df = pd.DataFrame(data_json['indicators']['quote'][0], index=dt)
    df.index = df.index.normalize()
    df = df[['close']]

    return df


if __name__ == "__main__":
    a = grab_data('aapl', date_range='1y', date_interval='1d')
    b = transform_data(a)
    print(b.head(10))

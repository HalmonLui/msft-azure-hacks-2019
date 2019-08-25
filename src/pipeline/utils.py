import pandas as pd
import numpy as np
import requests
import datetime
import arrow


# Grab data from Yahoo Finance
def grab_data(ticker, date_range, date_interval):
    # @TODO: consider a ticker column
    res = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={date_range}&interval={date_interval}'.format(**locals()))
    #data = res.json()
    #body = data['chart']['result'][0]
    data = res.json()['chart']['result'][0]
    dt = pd.Series(map(lambda x: arrow.get(x).datetime.replace(tzinfo=None), data['timestamp']), name='date')
    df = pd.DataFrame(data['indicators']['quote'][0], index=dt)
    df.index = df.index.normalize()
    #df = df.reset_index()

    df = df[['close']]
    print(df.head(10))


if __name__ == "__main__":
    grab_data('aapl', date_range='1y', date_interval='1d')

import pandas as pd
import numpy as np
import requests
import datetime
import arrow
import os
from bs4 import BeautifulSoup
import re

# Grab data from Yahoo Finance

"""
TODO tasks:
consider renaming some stuff
condense some functionality in the ticker method

maybe add a ticker column to the dataframe in transform_data

probably only do one day of data for the pipeline and backfill all the other days
that way it doesnt do a full overwrite every single tim

"""


def grab_data(ticker, date_range, date_interval):
    # @TODO: consider a ticker column
    res = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={date_range}&interval={date_interval}'.format(**locals()))
    data = res.json()['chart']['result'][0]
    # Edge case for printing out single day value
    if date_range == '1d' and date_interval == '1d':
        data['indicators']['quote'][0] = {
            k: list(set(v)) for k, v in data['indicators']['quote'][0].items()}
        data['indicators']['adjclose'][0] = {
            k: list(set(v)) for k, v in data['indicators']['adjclose'][0].items()}
        data['timestamp'].pop(0)
        data['indicators']['quote'][0]['volume'].pop(0)
    return data


def transform_data(data_json):
    dt = pd.Series(map(lambda x: arrow.get(x).datetime.replace(
        tzinfo=None), data_json['timestamp']), name='date')
    df = pd.DataFrame(data_json['indicators']['quote'][0], index=dt)
    df.index = df.index.normalize()
    df = df[['close']]

    return df


def grab_nasdaq100_tickers():
    res = requests.get('https://en.wikipedia.org/wiki/NASDAQ-100').text
    soup = BeautifulSoup(res, 'lxml')
    ticker_table = soup.find('table', {'class': 'wikitable sortable'})

    links = ticker_table.findAll('a')
    company_names = []
    for link in links:
        company_names.append(link.get('title'))

    ticker_links = ticker_table.findAll('td')
    tickers = []
    for i in range(len(ticker_links)):
        if i % 2 == 1:
            ticker = re.sub(
                r"<.?table[^>]*>|<.?t[rd]>|<font[^>]+>|<.?b>", "", str(ticker_links[i]))
            tickers.append(re.sub("(\\r|)\\n$", "", ticker))

    df = pd.DataFrame()
    df['Company'] = company_names
    df['ticker'] = tickers

    return df


if __name__ == "__main__":
    a = grab_data(ticker='aapl', date_range='1d', date_interval='1d')
    import json
    print(json.dumps(a, indent=4))
    b = transform_data(a)
    print(b)

    # print(b.head(10))
    # grab_nasdaq100_tickers()

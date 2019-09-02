import pandas as pd
import numpy as np
import requests
import datetime
import arrow
import os
from bs4 import BeautifulSoup
import re
import feedparser
import time
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import json
import pymongo

# Grab data from Yahoo Finance

"""
TODO tasks:
consider renaming some stuff
condense some functionality in the ticker method

maybe add a ticker column to the dataframe in transform_data

probably only do one day of data for the pipeline and backfill all the other days
that way it doesnt do a full overwrite every single time


might do multi stock for news

put command line args

code in holidays for nasdaq 100 stocks (2019) and weekends
01/01
01/21
02/18
04/19
05/27
07/03
07/04
09/02
11/28, 11/29
12/24, 12/25

"""


def convert_ds_to_unix(ds):
    # Convert string to datestamp
    ds += " 12:00:00"  # Add market close date
    dt = datetime.datetime.strptime(ds, "%Y-%m-%d %H:%M:%S")
    # Check if valid date for our computation (weekends and holidays)
    holidays = ['2019-01-01', '2020-01-01', '2019-01-21', '2019-02-18', '2019-04-19', '2019-05-27',
                '2019-07-03', '2019-07-04', '2019-09-02', '2019-11-28', '2019-11-29', '2019-12-24', '2019-12-25']
    if dt.weekday() >= 5:
        raise ValueError("Can't check stock data for weekend")
    elif ds[0:10] in holidays:
        raise ValueError("Markets are closed on these holiday dates")
    # Where unix time starts from
    dstart = datetime.datetime(1970, 1, 1, tzinfo=dt.tzinfo)
    timedelta = dt - dstart
    ts = int(timedelta.total_seconds())

    return ts


def grab_stock_data(ticker, start=None, end=None, date_range=None, date_interval=None):
    # @TODO: consider a ticker column
    # Error Checkers
    if start and end and date_range:
        raise ValueError(
            "Cannot have date_range specific with start and end date")
    if start and end and not date_interval:
        date_interval = '1d'
        # Convert start and end to unixtime at 12 pm utc (4 pm est when markets close)
        start = convert_ds_to_unix(start)
        end = convert_ds_to_unix(end)
        res = requests.get(
            "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start}&period2={end}&interval={date_interval}".format(**locals()))
        data = res.json()['chart']['result'][0]
    else:
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
    df['Ticker'] = tickers

    return df


def grab_stock_news(ticker):
    # currently only getting news for ticker
    parsed = feedparser.parse(
        'https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US'.format(ticker))
    # Consider finding the correct rickers instead of single ticker (experimental so far)
    posts = []
    for e in parsed.entries:
        dt = datetime.datetime.fromtimestamp(time.mktime(e.published_parsed))
        posts.append((ticker.upper(), e.title, e.link, e.description, dt))

    df = pd.DataFrame(
        posts, columns=['ticker', 'title', 'link', 'description', 'date'])

    return df


def grab_images(query):
    load_dotenv()
    api_key = os.getenv("AZURE_API_KEY")
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
    EXCEPTIONS = set([IOError, FileNotFoundError, requests.exceptions.RequestException,
                      requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
                      requests.exceptions.Timeout])
    client = ImageSearchAPI(CognitiveServicesCredentials(api_key))
    image_results = client.images.search(
        query=query, imageType='Photo', license='Any')
    try:
        first_image_result = image_results.value[0]
        r = requests.get(first_image_result.content_url)
        ext = first_image_result.content_url[first_image_result.content_url.rfind(
            "."):]
        file_name = query.split("logo", 1)[0].rstrip() + ext
        p = os.path.join("./images/", file_name)
        # Write file to disk
        f = open(p, "wb")
        f.write(r.content)
        f.close()

    except Exception as e:
        if type(e) in EXCEPTIONS:
            print("No image results returned for:", query)


def load_to_db(df, dbname, table):
    load_dotenv()
    client = pymongo.MongoClient(os.getenv("MONGO_NORM_USER"))
    db = client[dbname][table]
    data = df.to_dict(orient='records')
    db.insert_many(data)


def grab_sentiment_analysis(txt):
    print('h')


if __name__ == "__main__":
    #a = grab_data(ticker='aapl', date_range='1d', date_interval='5d')
    #print(json.dumps(a, indent=4))
    #b = transform_data(a)
    # print(b)

    #grab_images("Fastenal logo")

    # print(b.head(10))
    # grab_nasdaq100_tickers()
    #c = grab_stock_news('aapl')
    # print(c.head(1))
    a = grab_stock_data(ticker='aapl', start='2019-08-26', end='2019-08-27')
    b = transform_data(a)
    print(b)

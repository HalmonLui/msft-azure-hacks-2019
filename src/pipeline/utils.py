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
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import json
import pymongo
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import time

# Grab data from Yahoo Finance

"""
TODO tasks:
consider renaming some stuff
condense some functionality in the ticker method


might do multi stock for news

put command line args

html entities showing up in news description
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
    df = df[['close', 'high', 'low', 'open']]
    # Use date as its own column instead of index
    df = df.reset_index()
    df['ticker'] = data_json["meta"]["symbol"]
    # Add column that calculates % change between adj close and open for that day
    percentage_change = []
    for i, num in df['close'].iteritems():
        open = data_json["indicators"]["quote"][0]["open"][i]
        change = (num - open) / open * 100
        percentage_change.append(change)
    df['change'] = percentage_change

    return df


def airflow_grab_stock_data(ticker, start, end):
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
    df['ticker'] = data_json["meta"]["symbol"]
    # Add column that calculates % change between adj close and open for that day
    percentage_change = []
    for i, num in df['close'].iteritems():
        open = data_json["indicators"]["quote"][0]["open"][i]
        change = (num - open) / open * 100
        percentage_change.append(change)
    df['change'] = percentage_change

    context['task_instance'].xcom_push(key='data', value=df)


def grab_nasdaq100_tickers():
    load_dotenv()
    base_url = "https://msft-azure-hacks-image.cognitiveservices.azure.com/bing/v7.0"
    api_key = os.getenv("AZURE_API_KEY_IMAGE")
    client = WebSearchAPI(CognitiveServicesCredentials(api_key), base_url=base_url)
    web_data = client.web.search(query="NASDAQ-100")
    for i in range(len(web_data.web_pages.value)):
        if 'wikipedia' in web_data.web_pages.value[i].url:
            query = web_data.web_pages.value[i].url
            break


    res = requests.get(query).text
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
    df['company'] = company_names
    df['ticker'] = tickers

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


def grab_images(query, file_name):
    load_dotenv()
    api_key = os.getenv("AZURE_API_KEY_IMAGE")
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
        #file_name = query.split("logo", 1)[0].rstrip() + ext
        file_name = file_name + ext
        p = os.path.join("./images2/", file_name)
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
    # test
    load_dotenv()
    api_key = os.getenv("AZURE_API_KEY_SENTI")
    sentiment_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment"
    # Headers
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = api_key
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    # Detect sentiment
    post_data = json.dumps({"documents":[{"id": "1", "language": "en", "text": txt}]}).encode('utf-8')
    request1 = urllib.request.Request(sentiment_url, post_data, headers)
    try:
        response = urllib.request.urlopen(request1)
        response_json = json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        if e.code == 429:
            time.sleep(30)
            response = urllib.request.urlopen(request1)
            response_json = json.loads(response.read().decode('utf-8'))
        #raise
    print(response_json)
    sentiment = response_json['documents'][0]['score']

    # Define categories for sentiment
    if sentiment < 0.35:
        sentiment = 'Negative'
    elif sentiment >= 0.35 and sentiment < 0.65:
        sentiment = 'Neutral'
    elif sentiment >= 0.65:
        sentiment = 'Positive'
    return sentiment


def main():
    info = grab_nasdaq100_tickers()
    tickers = info.ticker.tolist()
    today = datetime.datetime.today()
    date = datetime.datetime(today.year, today.month, today.day)
    date = datetime.datetime.strftime(date, "%Y-%m-%d")
    for ticker in tickers:
        data = grab_stock_data(ticker=ticker, start=date, end=date)
        prices_df = transform_data(data)
        load_to_db(prices_df, "test", ticker)




if __name__ == "__main__":
    #a = grab_data(ticker='aapl', date_range='1d', date_interval='5d')
    #print(json.dumps(a, indent=4))
    #b = transform_data(a)
    # print(b)
    #grab_images("Fastenal logo")

    # print(b.head(10))
    #a = grab_nasdaq100_tickers()
    #print(a)
    #c = grab_stock_news('aapl')
    # print(c.head(1))

    #a = grab_stock_data(ticker='amzn', start='2019-09-09', end='2019-09-09')
    #b = transform_data(a)
    #print(b)
    #grab_sentiment_analysis()
    #print('hello world')
    main()

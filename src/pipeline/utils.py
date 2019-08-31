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
import urllib

# Grab data from Yahoo Finance

"""
TODO tasks:
consider renaming some stuff
condense some functionality in the ticker method

maybe add a ticker column to the dataframe in transform_data

probably only do one day of data for the pipeline and backfill all the other days
that way it doesnt do a full overwrite every single time


might do multi stock for news

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
        data['indicators']['quote'][0]['low'].pop(0)

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
    image_results = client.images.search(query=query, imageType='Photo', license='Any')
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



if __name__ == "__main__":
    a = grab_data(ticker='aapl', date_range='1d', date_interval='1d')
    #print(json.dumps(a, indent=4))
    b = transform_data(a)
    print(b)

    grab_images("Fastenal logo")

    # print(b.head(10))
    # grab_nasdaq100_tickers()
    #c = grab_stock_news('aapl')
    # print(c)

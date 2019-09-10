from utils import *
import argparse
import base64


def gen_logo_table():
    tickers_df = grab_nasdaq100_tickers()
    for idx, row in tickers_df.iterrows():
        if row['ticker'] == 'GOOGL':
            grab_images("google logo", "GOOGL")
        elif row['ticker'] == 'FOXA':
            grab_images("foxa logo", "FOXA")
        elif row['ticker'] == 'LBTYA':
            grab_images("liberty global a logo", "LBTYA")
        else:
            grab_images(row['company'].rstrip('.') + ' logo', row['ticker'])


def grab_filenames():
    filenames = []
    for file in sorted(os.listdir("./images/"), key=lambda s: s.lower()):
        filenames.append(file)

    tmp = filenames[filenames.index('google.png')]
    idx_googl = filenames.remove(tmp)
    filenames.insert(filenames.index('Alphabet Inc.png'), tmp)
    tmp = filenames[filenames.index('foxa.png')]
    idx_foxa = filenames.remove(tmp)
    filenames.insert(filenames.index('Fox Corporation.png'), tmp)
    tmp = filenames[filenames.index('liberty global a.png')]
    idx_lbtya = filenames.remove(tmp)
    filenames.insert(filenames.index('Liberty Global.png'), tmp)

    # Remove .DS_Store
    filenames.pop(0)

    return filenames


def gen_companies_table():
    tickers_df = grab_nasdaq100_tickers()
    #tickers_df = tickers_df.sort_values(by=['Company'])
    tickers_df = tickers_df.iloc[tickers_df.company.str.lower().argsort()]
    """
    filenames = grab_filenames()

    #filenames = [os.path.splitext(i)[0] for i in filenames]

    encoded_images = []
    path = './images/'
    for file in filenames:
        with open(path + file, 'rb') as f:
            encoded_images.append(base64.b64encode(f.read()))
            #encoded_images.append(Binary(f.read()))

    df = tickers_df
    df['Image'] = encoded_images
    """

    return tickers_df


def gen_dummy_table():
    # this table is purely for website testing purposes
    # portfolio dummy = amzn, aapl, tsla
    tix = ['AAPL', 'AMZN', 'TSLA']
    # grab close price for some rando day
    stocks = []
    # Grab news for each stock
    news = []
    for tick in tix:
        d = grab_stock_data(tick, '2019-08-27', '2019-08-27')
        stocks.append(transform_data(d))
        news.append(grab_stock_news(tick))
    # grab appropriate data from db
    load_dotenv()
    client = pymongo.MongoClient(os.getenv("MONGO_NORM_USER"))
    db = client.test.companies
    # Filter for only the tickers in the dummy portfolio
    myquery = {"$or": [{"Ticker": i} for i in tix]}
    doc = db.find(myquery)
    df2 = pd.DataFrame(list(doc))
    #print(df2)

    # Add sentiment to news table
    news_df = pd.concat(news).reset_index(drop=True)

    sentiments = []
    for d in news_df.title:
        try:
            sentiments.append(grab_sentiment_analysis(d))
        except Exception as e:
            print(e, '\n', d)

    news_df['sentiment'] = sentiments
    #print(news_df)

     # Merge with Companies table so it has access to the logo
    result = df2[['Ticker', 'Image']].merge(news_df, on='Ticker', how='right')
    #print(result, '\n *******************')

    # Merge with Price Table
    stocks_df = pd.concat(stocks).reset_index(drop=True)
    #print(stocks_df, '\n ******************')

    result = result.merge(stocks_df[['Ticker', 'close', 'change']], on='Ticker', how='right')
    print(result)

    return result


def delete_collection(dbname, table):
    load_dotenv()
    client = pymongo.MongoClient(os.getenv("MONGO_NORM_USER"))
    db = client["dbname"]["table"]
    res = db.delete_many({})


def gen_news_table():
    load_dotenv()
    # Table with Full Company name and Ticker
    #client = pymongo.MongoClient(os.getenv("MONGO_NORM_USER"))
    #db = client.test.companies
    # Due to limited API calls
    tickers = ['AAPL', 'AMZN', 'GOOGL', 'FB', 'MSFT', 'TSLA', 'NFLX', 'ADBE', 'SBUX', 'INTC']


    today = datetime.datetime.today()
    date = datetime.datetime(today.year, today.month, 9)#today.day)
    date_str = datetime.datetime.strftime(date, "%Y-%m-%d")

    #companies = pd.DataFrame(list(db.find({})))
    #tickers = companies.ticker.tolist()

    prices = []
    for ticker in tickers:
        df = grab_stock_data(ticker, start=date_str, end=date_str)
        df = transform_data(df)
        #db2 = client.test.ticker
        #query = {'date': {"$lte": date}}
        #val = db2.find(query)
        #df = pd.DataFrame(list(val))
        prices.append(df)

    prices_df = pd.concat(prices).reset_index(drop=True)

    news = []
    for ticker in tickers:
        news.append(grab_stock_news(ticker))
    news_df = pd.concat(news).reset_index(drop=True)

    sentiments = []
    for d in news_df.title:
        try:
            sentiments.append(grab_sentiment_analysis((d)))
        except Exception as e:
            print(e, '\n', d)

    news_df['sentiment'] = sentiments

    result = news_df.merge(prices_df[['ticker', 'close', 'change']], on='ticker', how='right')

    print(result.head())
    print(result.shape)

    return result

if __name__ == "__main__":
    #gen_logo_table()
    #df = gen_companies_table()
    #print(df.head(10))
    #pd.set_option('display.max_colwidth', -1)
    #print(df.loc[df.Ticker == "ADI"].Image)
    #load_to_db(df, "test", "companies")
    #df = gen_dummy_table()
    #load_to_db(df, "test", "dummy")
    df = gen_news_table()
    load_to_db(df, "test", "news")

from utils import *
import argparse
import base64


def gen_logo_table():
    tickers_df = grab_nasdaq100_tickers()
    for idx, row in tickers_df.iterrows():
        if row['Ticker'] == 'GOOGL':
            grab_images("google logo")
        elif row['Ticker'] == 'FOXA':
            grab_images("foxa logo")
        elif row['Ticker'] == 'LBTYA':
            grab_images("liberty global a logo")
        else:
            grab_images(row['Company'].rstrip('.') + ' logo')


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
    tickers_df = tickers_df.sort_values(by=['Company'])
    filenames = grab_filenames()

    #filenames = [os.path.splitext(i)[0] for i in filenames]

    encoded_images = []
    path = './images/'
    for file in filenames:
        with open(path + file, 'rb') as f:
            encoded_images.append(base64.b64encode(f.read()))

    df = tickers_df
    df['Image'] = encoded_images

    return df


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

if __name__ == "__main__":
    # gen_logo_table()
    #df = gen_companies_table()
    #load_to_db(df, "test", "companies")
    df = gen_dummy_table()
    load_to_db(df, "test", "dummy")

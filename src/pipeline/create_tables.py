from utils import *
import argparse
import base64


def gen_logo_table():
    tickers_df = grab_nasdaq100_tickers()
    for idx, row in tickers_df.iterrows():
        print(row['Company'], row['Ticker'])
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


if __name__ == "__main__":
    # gen_logo_table()
    df = gen_companies_table()
    load_to_db(df, "test", "companies")

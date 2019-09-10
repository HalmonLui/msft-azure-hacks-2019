
import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import json
import datetime
import requests
import os
import arrow
import pymongo
from dotenv import load_dotenv
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
np.random.seed(777)


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

    return df


def gen_dataset(tickers, start, end):
    stocks = []
    for tick in tickers:
        d = grab_stock_data(tick, start, end)
        stocks.append(transform_data(d))
    stocks_df = pd.concat(stocks, ignore_index=True)
    stocks_df = stocks_df.set_index("date")

    data = stocks_df.drop(['change'], axis=1)
    data = data.pivot(columns="Ticker")
    data.columns = [col[1] for col in data.columns]

    return data


def plot_price(data):
    plt.figure(figsize=(14, 10))
    for c in data.columns.values:
        plt.plot(data.index, data[c], lw=3, alpha=0.8, label=c)
    plt.legend(loc='upper left', fontsize=12)
    plt.ylabel('price in $')
    plt.show()


def plot_daily_returns(data):
    # plot daily returns
    returns = data.pct_change()
    plt.figure(figsize=(14, 10))
    for c in returns.columns.values:
        plt.plot(returns.index, returns[c], lw=3, alpha=0.8, label=c)
    plt.legend(loc='upper right', fontsize=12)
    plt.ylabel('daily returns')
    plt.show()


def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    # Calculatew the returns and volatility and turn it into an
    # number of trading days in a year
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(
        cov_matrix, weights))) * np.sqrt(252)
    return std, returns


def random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate, num_tickers):
    # generate portfolios with random weights assigned to each stock
    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(num_tickers)
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(
            weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record


def plot_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, _ = random_portfolios(
        num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(
        max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(
        max_sharpe.x, index=data.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [
        round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(
        min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(
        min_vol.x, index=data.columns, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    print("-" * 80)
    print("Maximum Sharpe Ratio Portfolio Allocation \n")
    print("Annualized Return:", round(rp, 2))
    print("Annualized Volatility", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Minimum Volatility Portfolio Allocation \n")
    print("Annualized Return:", round(rp_min, 2))
    print("Annualized Volatility", round(sdp_min, 2))
    print("\n")
    print(min_vol_allocation)

    plt.figure(figsize=(10, 10))
    plt.scatter(results[0, :], results[1, :], c=results[2, :],
                cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()
    plt.scatter(sdp, rp, marker='*', color='r',
                s=500, label='Maximum Sharpe Ratio')
    plt.scatter(sdp_min, rp_min, marker='*', color='g',
                s=500, label='Minimum Volatility')

    target = np.linspace(rp_min, 0.32, 50)
    efficient_portfolios = efficent_frontier(mean_returns, cov_matrix, target)
    plt.plot([p['fun'] for p in efficient_portfolios], target,
             linestyle='-.', color='black', label='efficient frontier')

    plt.title('Simulated Portfolio Optimization based on Efficient Frontier')
    plt.xlabel('Annualized volatility')
    plt.ylabel('Annualized returns')
    plt.legend(labelspacing=0.8)
    plt.show()


def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_var, p_ret = portfolio_annualised_performance(
        weights, mean_returns, cov_matrix)
    return - (p_ret - risk_free_rate) / p_var


def max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))
    result = sp.optimize.minimize(neg_sharpe_ratio, num_assets * [
                                  1. / num_assets, ], args=args, method='SLSQP', bounds=bounds, constraints=constraints)

    return result


def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]


def min_variance(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))
    result = sp.optimize.minimize(portfolio_volatility, num_assets * [
                                  1. / num_assets, ], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def efficient_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = sp.optimize.minimize(portfolio_volatility, num_assets * [
                                  1. / num_assets, ], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(mean_returns, cov_matrix, ret))
    return efficients


def plot_ef_with_selected(mean_returns, cov_matrix, risk_free_rate):
    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(
        max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(
        max_sharpe.x, index=data.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [
        round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(
        min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(
        min_vol.x, index=data.columns, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    an_vol = np.std(returns) * np.sqrt(252)
    an_rt = mean_returns * 252
    print("-" * 80)
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualised Return:", round(rp, 2))
    print("Annualised Volatility:", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Minimum Volatility Portfolio Allocation\n")
    print("Annualised Return:", round(rp_min, 2))
    print("Annualised Volatility:", round(sdp_min, 2))
    print("\n")
    print(min_vol_allocation)
    print("-" * 80)
    print("Individual Stock Returns and Volatility\n")
    for i, txt in enumerate(data.columns):
        print(txt, ":", "annuaised return", round(
            an_rt[i], 2), ", annualised volatility:", round(an_vol[i], 2))
    print("-" * 80)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(an_vol, an_rt, marker='o', s=200)

    for i, txt in enumerate(data.columns):
        ax.annotate(txt, (an_vol[i], an_rt[i]), xytext=(
            10, 0), textcoords='offset points')
    ax.scatter(sdp, rp, marker='*', color='r',
               s=500, label='Maximum Sharpe ratio')
    ax.scatter(sdp_min, rp_min, marker='*', color='g',
               s=500, label='Minimum volatility')

    target = np.linspace(rp_min, 0.34, 50)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)
    ax.plot([p['fun'] for p in efficient_portfolios], target,
            linestyle='-.', color='black', label='efficient frontier')
    ax.set_title('Portfolio Optimization with Individual Stocks')
    ax.set_xlabel('annualised volatility')
    ax.set_ylabel('annualised returns')
    ax.legend(labelspacing=0.8)

    plt.show()


def get_optimized_portfolio(tickers, num_portfolios=25000, risk_free_rate=0.017):
    load_dotenv()
    client = pymongo.MongoClient(os.getenv("MONGO_NORM_USER"))
    num_tickers = len(tickers)
    data = []
    for ticker in tickers:
        db = client['test'][ticker]
        cursor = db.find()
        df = pd.DataFrame(list(cursor))
        data.append(df)
    # Now reformat dataset
    stocks_df = pd.concat(data, ignore_index=True)
    stocks_df = stocks_df.set_index("date")

    dataset = stocks_df.drop(['change', '_id', 'high', 'open', 'low'], axis=1)
    dataset = dataset.pivot(columns="ticker")
    dataset.columns = [col[1] for col in dataset.columns]

    returns = dataset.pct_change()
    cov_matrix = returns.cov()
    mean_returns = returns.mean()

    def calc_ef(data, mean_returns, cov_matrix, num_portfolios, risk_free_rate):
        max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
        sdp, rp = portfolio_annualised_performance(
            max_sharpe['x'], mean_returns, cov_matrix)
        max_sharpe_allocation = pd.DataFrame(
            max_sharpe.x, index=data.columns, columns=['allocation'])
        max_sharpe_allocation.allocation = [
            round(i * 100, 2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T

        min_vol = min_variance(mean_returns, cov_matrix)
        sdp_min, rp_min = portfolio_annualised_performance(
            min_vol['x'], mean_returns, cov_matrix)
        min_vol_allocation = pd.DataFrame(
            min_vol.x, index=data.columns, columns=['allocation'])
        min_vol_allocation.allocation = [
            round(i * 100, 2) for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T

        an_vol = np.std(returns) * np.sqrt(252)
        an_rt = mean_returns * 252

        return rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation, an_rt, an_vol

    rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation, an_rt, an_vol = calc_ef(
        dataset, mean_returns, cov_matrix, num_portfolios, risk_free_rate)

    portfolio = {}
    portfolio['Maximum Sharpe Ratio Portfolio Allocation'] = {'Annualised Return': round(
        rp, 2), 'Annualised Volatility': round(sdp, 2), 'Allocation': max_sharpe_allocation.to_dict()}
    portfolio['Minimum Volatility Portfolio Allocation'] = {'Annualised Return': round(
        rp_min, 2), 'Annualised Volatility': round(sdp_min, 2), 'Allocation': min_vol_allocation.to_dict()}
    portfolio['Individual Stock Returns and Volatility'] = {}
    for i, txt in enumerate(dataset.columns):
        portfolio['Individual Stock Returns and Volatility'][txt] = {
            'Annualised Return': round(an_rt[i], 2), 'Annualised Volatility': round(an_vol[i], 2)}

    portfolio_json = json.dumps(portfolio, indent=4, sort_keys=True)

    return portfolio_json


if __name__ == "__main__":
    # data = gen_dataset(tickers=['AAPL', 'AMZN', 'GOOGL', 'FB', 'MSFT', 'TSLA', 'NFLX', 'ADBE', 'SBUX', 'INTC'],
    #                   start='2017-09-06', end='2019-09-09')

    #returns = data.pct_change()
    #cov_matrix = returns.cov()
    #mean_returns = returns.mean()
    #num_portfolios = 25000
    #import quandl
    #rates = quandl.get("USTREASURY/BILLRATES")
    #today = datetime.datetime.today()

    #risk_free_rate = rates.loc[pd.to_datetime(rates.index) == datetime.datetime(today.year, today.month, 5), "52 Wk Bank Discount Rate"].values[0]
    #risk_free_rate /= 100
    risk_free_rate = 0.017

    tickers = ['AAPL', 'AMZN', 'GOOGL', 'FB', 'MSFT',
               'TSLA', 'NFLX', 'ADBE', 'SBUX', 'INTC']
    get_optimized_portfolio(tickers)

    """
    print(cov_matrix)
    print(cov_matrix.shape)
    print(np.trace(cov_matrix))

    # Attempt to calculate multivariate skew and kurtosis
    # Transpose is needed to match that of calculations for pandas dataframe
    X = np.nan_to_num(returns.to_numpy()).T
    #print(X)

    n, p = X.shape

    difT = []
    for i in range(0, p):
        difT.append(X[..., i] - np.mean(X[..., i]))

    # Covariance matrix
    S = np.cov(X)
    # Conv from list to np.ndarray
    difT = np.asarray(difT).T
    # Mahalanobis distance
    #D = np.dot(difT.T, np.dot(np.linalg.inv(S), difT))
    D = np.dot(np.dot(difT.T, np.linalg.inv(S)), difT)

    b1p = (np.sum(np.sum(D ** 3))) / n**2
    # Kurtosis coefficient
    b2p = np.trace(D ** 2) / n
    print(b1p)
    print(b2p)

    #arr_lens = [X.shape, difT.shape, S.shape, D.shape]
    print('Dims of X are {} \n Dims of difT are {} \n Dims of S are {} \n, Dims of D are {}'.format(X.shape, difT.shape, S.shape, D.shape))


    k = ((p+1)*(n+1)*(n+3)) / (n * (((n+1)* (p+1)) - 6))  # sample sample correction
    v = ( p * (p + 1) * (p + 2)) / 6  # deg of freedom
    g1 = (n*b1p) / 6
    p1 = sp.stats.chi2.sf(g1, v)
    print(p1)

    g2 = (b2p - (p * (p+2))) / (np.sqrt((8 * p * (p + 2))/ n))
    p2 = 1 - sp.stats.norm.cdf(abs(g2))
    print(p2)
    """

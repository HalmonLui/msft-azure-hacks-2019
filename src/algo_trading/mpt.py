
import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
np.random.seed(777)
import sys

sys.path.insert(
    1, '/Users/sonamghosh/Desktop/msft_azure_hackathon_2019/exploratory_analysis/msft-azure-hacks-2019/src/pipeline/')

from utils import *


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
    plt.figure(figsize=(14, 7))
    for c in data.columns.values:
        plt.plot(data.index, data[c], lw=3, alpha=0.8, label=c)
    plt.legend(loc='upper left', fontsize=12)
    plt.ylabel('price in $')
    plt.show()


def plot_daily_returns(data):
    # plot daily returns
    returns = data.pct_change()
    plt.figure(figsize=(14,7))
    for c in returns.columns.values:
        plt.plot(returns.index, returns[c], lw=3, alpha=0.8, label=c)
    plt.legend(loc='upper right', fontsize=12)
    plt.ylabel('daily returns')
    plt.show()


def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    # Calculatew the returns and volatility and turn it into an
    returns = np.sum(mean_returns*weights) * 252  # number of trading days in a year
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns

def random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
    # generate portfolios with random weights assigned to each stock
    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(7)
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_std_dev
        results[1, i] = portfolio_return
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record


def calc_sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std_dev):
    print('Hello World')


if __name__ == "__main__":
    print("Hello world")
    data = gen_dataset(tickers=['AAPL', 'AMZN', 'GOOGL', 'FB', 'MSFT', 'TSLA', 'NFLX'],
                       start='2017-09-06', end='2019-09-03')

    returns = data.pct_change()
    cov_matrix = returns.cov()
    print(cov_matrix)
    print(cov_matrix.shape)
    print(np.trace(cov_matrix))

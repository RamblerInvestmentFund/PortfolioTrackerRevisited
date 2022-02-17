import pandas as pd
from yahoo_fin import stock_info as si
import yfinance as yf
from tqdm import tqdm


def pull_data(file):
    """
    returns data from portfolio specified as a file
    pandas dataframe containing basis and weight info
    """

    print('Pulling Tickers, Shares, and Calculating Basis Data...')

    df = pd.read_csv(filepath_or_buffer=file, index_col=False)

    tickers = df["Ticker"].tolist()
    shares = df["Shares"].tolist()
    prices = [si.get_live_price(f"{ticker}") for ticker in tickers]
    basis = [price * share for price, share in zip(prices, shares)]

    df["Basis"] = basis
    valueFolio = sum(basis)
    df["Weight"] = [item / valueFolio for item in basis]


    '''returns historical data from yfinance'''
    print('Creating Historical Dataframe of Price Values and Portfolio Values...')

    historicalValue = yf.download(tickers=tickers, start="2021-06-21")["Close"]
    historicalValue = historicalValue.mul(shares, axis=1)

    portfolioValue = pd.DataFrame(columns=["Portfolio"], index=historicalValue.index)
    portfolioValue["Portfolio"] = historicalValue.sum(axis=1)

    historicalValueExtended = yf.download(tickers=tickers, start="2021-01-01")["Close"]
    historicalValueExtended = historicalValueExtended.mul(shares, axis=1)

    portfolioValueExtended = pd.DataFrame(
        columns=["Portfolio"], index=historicalValueExtended.index
    )
    portfolioValueExtended["Portfolio"] = historicalValueExtended.sum(axis=1)
    portfolioValueExtended.dropna(axis=0)

    return df, portfolioValue, historicalValue, portfolioValueExtended


def topGainersLosers(historicalValue, totalHoldingStart):
    """Creates Table for Top Gainers/Losers"""

    print("Creating Top Gainers Table and Top Losers Table")

    priceDifference = historicalValue.iloc[-1].subtract(totalHoldingStart)
    percentChange = round(priceDifference.divide(totalHoldingStart) * 100, 2)
    stockChanges = pd.DataFrame(
        data=percentChange, index=percentChange.index, columns=["% Change"]
    )

    formatter = lambda x: "{:.2f}".format(x) + "%"

    topGainers = stockChanges[stockChanges["% Change"] > 0].sort_values(by=["% Change"], ascending=False)
    topGainers["% Change"] = ("+" + topGainers["% Change"].apply(formatter))  # Lambda conversion keeps trailing 0's

    topLosers = stockChanges[stockChanges["% Change"] < 0].sort_values(by=["% Change"])
    topLosers["% Change"] = topLosers["% Change"].apply(formatter)

    return topGainers, topLosers


def main():
    pull_data("assets/portfolio.csv")


if __name__ == "__main__":
    main()

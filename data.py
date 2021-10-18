import pandas as pd
from yahoo_fin import stock_info as si
import yfinance as yf


def pull_data(file):
    # ---- Creates DataFrame with Tickers, Shares, and Basis
    print('Pulling Tickers, Shares, and Calculating Basis Data...')
    df = pd.read_csv(filepath_or_buffer=file, index_col=False)
    tickerString = []
    shares = []
    basis = []
    for idx in df.index:
        tickerString.append(df['Ticker'][idx])
        shares.append(df['Shares'][idx])
        price = si.get_live_price('{ticker}'.format(ticker = df['Ticker'][idx]))
        basisPrice = price * df['Shares'][idx]
        basis.append(basisPrice)
    df['Basis'] = basis

    print('Creating Historical Dataframe of Price Values and Portfolio Values...')
    # ---- Creates Historical DataFrame of price data and Portfolio Value Data Frame from the rebalance
    historicalValue = yf.download(tickers=tickerString, start = '2021-06-21')
    historicalValue = historicalValue['Close']
    historicalValue = historicalValue.mul(shares, axis=1)
    portfolioValue = pd.DataFrame(columns=['Portfolio'], index=historicalValue.index)
    portfolioValue['Portfolio'] = historicalValue.sum(axis=1)

    return df, portfolioValue, historicalValue




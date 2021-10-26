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

    valueFolio = sum(basis)

    print('Creating Historical Dataframe of Price Values and Portfolio Values...')
    # ---- Creates Historical DataFrame of price data and Portfolio Value Data Frame from the rebalance
    historicalValue = yf.download(tickers=tickerString, start = '2021-06-21')
    historicalValue = historicalValue['Close']
    historicalValue = historicalValue.mul(shares, axis=1)
    portfolioValue = pd.DataFrame(columns=['Portfolio'], index=historicalValue.index)
    portfolioValue['Portfolio'] = historicalValue.sum(axis=1)

    historicalValueExtended = yf.download(tickers=tickerString, start='2021-01-01')
    historicalValueExtended = historicalValueExtended['Close']
    historicalValueExtended = historicalValueExtended.mul(shares, axis=1)
    portfolioValueExtended = pd.DataFrame(columns=['Portfolio'], index=historicalValueExtended.index)
    portfolioValueExtended['Portfolio'] = historicalValueExtended.sum(axis=1)
    portfolioValueExtended.dropna(axis=0)

    # ---- Adds Weights to the DF
    weightList = []

    for i in df['Basis']:
        weight = i / valueFolio
        weightList.append(weight)
    df['Weight'] = weightList

    return df, portfolioValue, historicalValue, portfolioValueExtended

def topGainersLosers(historicalValue, totalHoldingStart):
    print('Creating Top Gainers Table and Top Losers Table')
    # ---- Creates Table for Top Gainers/Losers
    priceDifference = historicalValue.iloc[-1].subtract(totalHoldingStart)
    percentChange = round(priceDifference.divide(totalHoldingStart) * 100, 2)
    stockChanges = pd.DataFrame(data=percentChange, index=percentChange.index, columns=['% Change'])

    topGainers = stockChanges[stockChanges['% Change'] > 0].sort_values(by=['% Change'], ascending=False)
    topGainers['% Change'] = '+' + topGainers['% Change'].apply(lambda x: '{:.2f}'.format(x)) + '%' # Lambda conversion keeps trailing 0's

    topLosers = stockChanges[stockChanges['% Change'] < 0].sort_values(by=['% Change'])
    topLosers['% Change'] = topLosers['% Change'].apply(lambda x: '{:.2f}'.format(x)) + '%'

    return topGainers, topLosers




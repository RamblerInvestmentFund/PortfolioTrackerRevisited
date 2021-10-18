import yfinance as yf
import pandas as pd

def create_benchmark(df, historicalValue):
    # ---- Creates Benchmark Portfolio Value
    totalHoldingStart = historicalValue.iloc[0]

    sumEquity = 0
    sumREIT = 0
    sumCommodity = 0
    sumBond = 0
    i = 0
    for idx in totalHoldingStart.index:
        if idx == df['Ticker'][i]:
            type = df['Type'][i]
            if type == 'Equity':
                sumEquity += totalHoldingStart[i]
                i+=1
            elif type == 'Commodity':
                sumCommodity += totalHoldingStart[i]
                i+=1
            elif type == 'REIT':
                sumREIT += totalHoldingStart[i]
                i+=1
            elif type == 'Bond':
                sumBond += totalHoldingStart[i]
                i+=1

    startSum = [sumEquity, sumREIT, sumCommodity, sumBond]
    ECRB_ETF = ['SPY', 'USCI', 'VNQ', 'TLT']
    benchmarkHistorical = yf.download(ECRB_ETF, start='2021-06-21')
    benchmarkHistorical = benchmarkHistorical['Close']
    benchmarkStart = benchmarkHistorical.iloc[0]
    benchmarkShares = [(sumEquity/benchmarkStart['SPY']), (sumBond/benchmarkStart['TLT']), (sumCommodity/benchmarkStart['USCI']), (sumREIT/benchmarkStart['VNQ'])]
    benchmarkHistorical = benchmarkHistorical.mul(benchmarkShares, axis=1)
    benchPortfolioValue = pd.DataFrame(columns=['Portfolio'], index=benchmarkHistorical.index)
    benchPortfolioValue['Portfolio'] = benchmarkHistorical.sum(axis=1)

    return totalHoldingStart, benchPortfolioValue
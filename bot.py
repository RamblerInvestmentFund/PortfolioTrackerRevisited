import slack
import quandl
import os
from fpdf import FPDF
from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import pandas as pd
import matplotlib.pyplot as plt


today = datetime.date.today()
print('Running...')
# ---- Creates DataFrame with Tickers, Shares, and Basis
df = pd.read_csv(filepath_or_buffer='portfolio.csv', index_col=False)
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

# ---- Creates Historical DataFrame of price data and Portfolio Value Data Frame from the rebalance
historicalValue = yf.download(tickers=tickerString, start = '2021-06-21')
historicalValue = historicalValue['Close'] 
historicalValue = historicalValue.mul(shares, axis=1)
portfolioValue = pd.DataFrame(columns=['Portfolio'], index=historicalValue.index)
portfolioValue['Portfolio'] = historicalValue.sum(axis=1)

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


# ---- Create benchmark 
# historicalValBench = pd.DataFrame(columns=['Equity', 'Commodity', 'REIT', 'Bond'])

# benchmarkShares = [(sumEquity/si.get_live_price(ticker='SPY')), (sumBond/si.get_live_price(ticker='TLT')), (sumCommodity/si.get_live_price(ticker='USCI')),(sumREIT/si.get_live_price(ticker='VNQ'))]
# sumBasisSeries = pd.Series(basisList, index=(historicalValBench.columns))
# basisPercentageSeries = pd.Series([(sumEquity/sumBasis), (sumCommodity/sumBasis), (sumREIT/sumBasis), (sumBond/sumBasis)], index=historicalValBench.columns)
# historicalValBench = historicalValBench.append(sumBasisSeries, ignore_index=True)
# historicalValBench = historicalValBench.append(basisPercentageSeries, ignore_index=True)

# ECRB_ETF = ['SPY', 'USCI', 'VNQ', 'TLT']
# benchmarkHistorical = yf.download(ECRB_ETF, start='2021-06-21')
# benchmarkHistorical = benchmarkHistorical['Close']
# benchmarkHistorical = benchmarkHistorical.mul(benchmarkShares, axis=1)
# benchPortfolioValue = pd.DataFrame(columns=['Portfolio'], index=benchmarkHistorical.index)
# benchPortfolioValue['Portfolio'] = benchmarkHistorical.sum(axis=1)
# # !!!!!!!! Benchmark is wrong. Needs to instead, find the sum of the basis at the beginning of the rebalance,
# # then it needs to put those sums into the sumBasisSeries, into the Historicalvalbench, calculate benchmark shares by dividing each
# # sector sum by the price at start of rebalance, not at the end. Then multiply those shares throughout the table. Sum the rows of the table, and plot



# # ---- Creates Plot of Portfolio
# plt.style.use('Solarize_Light2')
# plt.plot(portfolioValue, color='red')
# plt.plot(benchPortfolioValue, color='blue')
# plt.xticks(rotation = 20)
# plt.ylabel('Portfolio Change')
# plt.xlabel('Days Since Rebalance')
# plt.legend(['RIF', 'Benchmark'])
# plt.title('Portfolio Growth Since The Rebalance V.S. Benchmark', y=1.05)
# plt.show()
# plt.savefig('portfolioVSbenchmark.png')


# # ---- Cover Page

# pdf = FPDF(orientation='landscape')
# pdf.set_margin(2)
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# # ---- Date
# pdf.set_font("Times", size=22)
# pdf.set_font(style='B')
# pdf.set_text_color(237, 232, 228)
# pdf.cell(txt=str(today), align='C')
# # ----
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.image(x = -0.5, y = 12, w = pdf.w + 1, name='RIFLogo(B&W).png')

# # ---- Second Page
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.set_fill_color(0, 0, 0)
# pdf.rect(x = 0, y = 12, w = pdf.w, h = 186, style = 'F')
# pdf.image(x=-0.5, y=12, w=(pdf.w+1)/2, name='portfolioVSbenchmark.png')

# # ---- Third Page
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.set_fill_color(0, 0, 0)
# pdf.rect(x = 0, y = 12, w = pdf.w + 1, h = 186, style = 'F')

# # ---- PDF Output
# pdf.output('pdf_1.pdf')




#### Call Bot and Send Portfolio
# client = slack.WebClient(token = '####')
# client.chat_postMessage(channel = '#sector-materials', text='Hello World!')
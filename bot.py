import slack
import quandl
import os
import logging
from fpdf import FPDF
from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import pandas as pd
import matplotlib.pyplot as plt

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

# ---- Creates Table for Top Gainers/Losers
priceDifference = historicalValue.iloc[-1].subtract(totalHoldingStart)
percentChange = round(priceDifference.divide(totalHoldingStart) * 100, 2)
stockChanges = pd.DataFrame(data=percentChange, index=percentChange.index, columns=['% Change'])

topGainers = stockChanges[stockChanges['% Change'] > 0].sort_values(by=['% Change'], ascending=False)
topGainers['% Change'] = '+' + topGainers['% Change'].apply(lambda x: '{:.2f}'.format(x)) + '%' # Lambda conversion keeps trailing 0's

topLosers = stockChanges[stockChanges['% Change'] < 0].sort_values(by=['% Change'])
topLosers['% Change'] = topLosers['% Change'].apply(lambda x: '{:.2f}'.format(x)) + '%'


# # ---- Creates Plot of Portfolio
# plt.style.use('Solarize_Light2')
# plt.plot(portfolioValue, color='red')
# plt.plot(benchPortfolioValue, color='blue')
# plt.xticks(rotation = 20)
# plt.ylabel('Portfolio Change')
# plt.xlabel('Days Since Rebalance')
# plt.legend(['RIF', 'Benchmark'])
# plt.title('Portfolio Growth Since The Rebalance V.S. Benchmark', y=1.05)
# plt.savefig('portfolioVSbenchmark.png')
# #plt.show()


today = datetime.date.today()
# ---- Cover Page
pdf = FPDF(orientation='landscape')
pdf.set_margin(2)
pdf.add_page()
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# ---- Date
pdf.set_font("Times", size=22)
pdf.set_font(style='B')
pdf.set_text_color(237, 232, 228)
pdf.cell(txt=str(today), align='C')
# ----
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
pdf.image(x = -0.5, y = 12, w = pdf.w + 1, name='RIFLogo(B&W).png')

# ---- Second Page
pdf.add_page()
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
pdf.set_fill_color(0, 0, 0)
pdf.rect(x = 0, y = 12, w = pdf.w, h = 186, style = 'F')
pdf.image(x=135, y=47, w=(pdf.w+1)/2, name='portfolioVSbenchmark.png')

pdf.set_font("Times", size=16)
pdf.set_font(style='BU')
pdf.set_text_color(248, 240, 227)
pdf.cell(0, 13, ln=1)
pdf.cell(125, 8, 'Top Gainers / Top Losers', ln=1, align='C')
pdf.set_font("Times", size=14)

losersList = topLosers.to_records()
losersList = list(losersList)
i = 0
for row in topGainers.iterrows():
    pChange = str(row[1])
    pChange = pChange.split()
    pdf.set_text_color(0, 255, 0)
    pdf.cell(25, 8, str(row[0]))
    pdf.cell(50, 8, pChange[2])
    pdf.set_text_color(255, 0, 0)
    pdf.cell(25, 8, losersList[i][0])
    pdf.cell(25, 8, losersList[i][1], ln=1)
    i+=1

# ---- Third Page
pdf.add_page()
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
pdf.set_fill_color(0, 0, 0)
pdf.rect(x = 0, y = 12, w = pdf.w + 1, h = 186, style = 'F')

# ---- PDF Output
pdf.output('pdf_1.pdf')


# # ---- Call Bot and Send Portfolio
# # client = slack.WebClient(token = '####')
# # client.files_upload(channels = '#sector-materials', file='./pdf_1.pdf')


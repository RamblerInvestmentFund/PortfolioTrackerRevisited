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
import data
import benchmark
import quantstats as qs


df, portfolioValue, historicalValue, portfolioValueExtended = data.pull_data('portfolio.csv')
totalHoldingStart, benchPortfolioValue = benchmark.create_benchmark(df, historicalValue)
benchmark.plot_benchmark(portfolioValue, benchPortfolioValue)
topGainers, topLosers = data.topGainersLosers(historicalValue, totalHoldingStart)

qs.extend_pandas()
# print(df)
print(portfolioValue)
# print(historicalValue)
print(portfolioValueExtended)
# print(totalHoldingStart)
# print(benchPortfolioValue)

qs.reports.html(portfolioValueExtended['Portfolio'], "SPY", output='rif_vs_bench.html')

# Individual graphs from .html report, no option for Cumulative Returns v Benc (Volatility Matched)
qs.plots.returns(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/YTD_rif_vs_bench.png')
qs.plots.log_returns(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/YTD_rif_vs_bench_log.png')
qs.plots.yearly_returns(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/EOY_rif_vs_bench.png')
qs.plots.histogram(portfolioValueExtended['Portfolio'],savefig='Figures/rif_monthly_dist.png')
qs.plots.daily_returns(portfolioValueExtended['Portfolio'],savefig='Figures/rif_daily_returns.png')
qs.plots.rolling_beta(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/rol_beta.png')
qs.plots.rolling_volatility(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/rol_vol.png')
qs.plots.rolling_sharpe(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/rol_beta_sharpe.png')
qs.plots.rolling_sortino(portfolioValueExtended['Portfolio'], "SPY", savefig='Figures/rol_beta_sortino.png')
qs.plots.drawdowns_periods(portfolioValueExtended['Portfolio'], savefig='Figures/drawdown_periods.png')
qs.plots.drawdown(portfolioValueExtended['Portfolio'], savefig='Figures/drawdown_plot.png')
qs.plots.monthly_returns(portfolioValueExtended['Portfolio'], savefig='Figures/monthly_returns.png')
qs.plots.distribution(portfolioValueExtended['Portfolio'], savefig='Figures/return_quantiles.png')


# #### ---------------- Creating PDF ---------------- ####
# today = datetime.date.today()
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
# pdf.cell(0, 13, ln=1)
# pdf.set_font("Times", size=16, style='BU')
# pdf.cell(125, 8, 'Top Gainers / Top Losers', align='C')
# pdf.set_font("Times", size=20, style='BU')
# percentGain = (((portfolioValue['Portfolio'][len(portfolioValue)-1] - portfolioValue['Portfolio'][0])/portfolioValue['Portfolio'][0])*100).round(2)
# pdf.cell(((pdf.w/2) + (pdf.w/2 - 125)), 8, 'Performance for the current period: {change}%'.format(change = percentGain), ln=1, align='C')
# pdf.image(x=135, y=47, w=(pdf.w+1)/2, name='portfolioVSbenchmark.png')

# pdf.set_text_color(248, 240, 227)
# pdf.set_font("Times", size=14)

# losersList = topLosers.to_records()
# losersList = list(losersList)
# gainersList = topGainers.to_records()
# gainersList = list(gainersList)

# if len(gainersList) > len(losersList):
#     gainersList = gainersList[0:len(losersList)]
# elif len(gainersList) < len(losersList):
#     losersList = losersList[0:len(gainersList)]

# j = 0
# for i in gainersList:
#     pdf.set_text_color(0, 255, 0)
#     pdf.cell(25, 8, str(i[0]))
#     pdf.cell(50, 8, i[1])
#     pdf.set_text_color(255, 0, 0)
#     pdf.cell(25, 8, losersList[j][0])
#     pdf.cell(25, 8, losersList[j][1], ln=1)
#     j+=1

# # ---- Third Page
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0,  w = pdf.w, h = 12, style = 'F')
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.set_fill_color(0, 0, 0)
# pdf.rect(x = 0, y = 12, w = pdf.w + 1, h = 186, style = 'F')

# # ---- PDF Output
# pdf.output('pdf_1.pdf')

# # # # ---- Call Bot and Send Portfolio
# # # client = slack.WebClient(token = '####')
# # # client.files_upload(channels = '#sector-materials', file='./pdf_1.pdf')


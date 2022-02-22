import datetime
import logging
import os

from fpdf import FPDF
import quandl
import quantstats as qs
# import slack

import benchmark
import data
import metrics


class Document(FPDF):
    '''extended FPDF class with custom functions'''

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    HALF_RED = (128, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    def banner(self, *, top):
        '''
        creates a dark red banner at the top or bottom of the page
        '''

        self.set_fill_color(*self.HALF_RED)
        y = 0 if top else 198
        self.rect(x=0, y=y, w=self.w, h=12, style='F')

    def add_page_banners(self):
        '''creates a new page with banners at the top and bottom'''

        self.add_page()
        self.banner(top=True)
        self.set_fill_color(*self.BLACK)
        self.rect(x=0, y=12, w=self.w, h=186, style='F')
        self.banner(top=False)


def build_pdf():
    '''generates pdf report'''

    '''TODO: write to json for quicker intermediate loading ... try excepts'''
    df, portfolioValue, historicalValue, portfolioValueExtended = data.pull_data(
        'assets/portfolio.csv')
    totalHoldingStart, benchPortfolioValue = benchmark.create_benchmark(df, historicalValue)
    benchmark.plot_benchmark(portfolioValue, benchPortfolioValue)
    topGainers, topLosers = data.topGainersLosers(historicalValue, totalHoldingStart)

    metrics.create_performance_plots(portfolioValueExtended)
    metrics.create_corr_heatmap(list(df['Shares']), historicalValue)

    # # writes html
    # qs.extend_pandas()
    # qs.reports.html(portfolioValueExtended['Portfolio'], "SPY", output='rif_vs_bench.html')

    'Cover Page'
    pdf = Document(orientation='landscape')

    pdf.add_page_banners()

    pdf.set_font("Times", size=20, style='B')
    pdf.set_text_color(*pdf.WHITE)
    pdf.cell(0, -5, txt=str(datetime.date.today()), align='L')

    pdf.image(x=-0.5, y=12, w=pdf.w + 1, name='assets/RIFLogo(B&W).png')

    'Second Page'
    pdf.add_page_banners()
    pdf.cell(0, 13, ln=1)

    pdf.set_font("Times", size=20, style='BU')
    pdf.cell(125, 8, 'Top Gainers / Top Losers', align='C')

    port = portfolioValue['Portfolio']
    percentGain = round(100*(port[-1] - port[0])/port[0], 2)

    pdf.cell(((pdf.w/2) + (pdf.w/2 - 125)), 8,
             f'Performance for the current period: {percentGain}%', ln=1, align='C')

    losers = list(topLosers.to_records())
    gainers = list(topGainers.to_records())
    minlen = min(len(losers), len(gainers))
    losers, gainers = losers[:minlen], gainers[:minlen]

    pdf.set_font("Times", size=14)
    for gainer, loser in zip(gainers, losers):
        pdf.set_text_color(*pdf.GREEN)
        pdf.cell(25, 8, gainer[0])
        pdf.cell(50, 8, gainer[1])

        pdf.set_text_color(*pdf.RED)
        pdf.cell(25, 8, loser[0])
        pdf.cell(25, 8, loser[1], ln=1)

    pdf.image(x=135, y=47, w=(pdf.w+1)/2, name='img/portfolioVSbenchmark.png')

    'Third Page'
    pdf.add_page_banners()
    pdf.image(x=-0.5, y=12, w=pdf.w + 1, name='img/monthly_returns.png')

    'Fourth Page'
    pdf.add_page_banners()
    pdf.image(x=-0.5, y=12, w=pdf.w + 1, name='img/return_quantiles.png')

    'Fifth Page'
    pdf.add_page_banners()
    pdf.image(x=-0.5, y=12, w=pdf.w + 1, name='img/portfolio_corr.png')

    'Sixth Page'
    pdf.add_page_banners()
    pdf.image(x=-0.5, y=pdf.h-100, w=pdf.w + 1, name='img/rol_beta_sharpe.png')
    pdf.image(x=-0.5, y=12, w=pdf.w + 1, name='img/rol_beta_sortino.png')

    pdf.output('assets/testpdf.pdf')

    '''TODO: send to slack_sdk'''
    # Call Bot and Send Portfolio
    # client = slack.WebClient(token = '####')
    # client.files_upload(channels = '#sector-materials', file='assets/testpdf.pdf')


def main():
    build_pdf()


if __name__ == '__main__':
    main()

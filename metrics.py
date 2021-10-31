import quantstats as qs
import matplotlib.pyplot as plt
import seaborn as sns

def create_performance_plots(portfolioValueExtended):
    # ---- Extracting individual graphs from .html report, no option for Cumulative Returns v Benc (Volatility Matched)
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

def create_corr_heatmap(numShares, historicalValue):
    avgStockPrice = historicalValue.divide(numShares, axis = 1)
    stockCorr = avgStockPrice.corr(method='pearson')
    sns.heatmap(stockCorr, annot=False, cmap='coolwarm', xticklabels=True, yticklabels=True, vmin=-1, vmax=1)
    plt.title('Portfolio Correlation')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.savefig('Figures/portfolio_corr.png')
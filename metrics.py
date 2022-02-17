import matplotlib.pyplot as plt
import quantstats as qs
import seaborn as sns


def create_performance_plots(portfolioValueExtended):
    """TODO: docstring
    Extracting individual graphs from .html report
    no option for Cumulative Returns v Benc (Volatility Matched)
    """

    """TODO: only p['Portfolio'] is used ... change param"""

    port = portfolioValueExtended["Portfolio"]

    qs.plots.returns(port, "SPY", savefig="img/YTD_rif_vs_bench.png")
    qs.plots.log_returns(port, "SPY", savefig="img/YTD_rif_vs_bench_log.png")
    qs.plots.yearly_returns(port, "SPY", savefig="img/EOY_rif_vs_bench.png")

    qs.plots.histogram(port, savefig="img/rif_monthly_dist.png")
    qs.plots.daily_returns(port, savefig="img/rif_daily_returns.png")

    qs.plots.rolling_beta(port, "SPY", savefig="img/rol_beta.png")
    qs.plots.rolling_volatility(port, "SPY", savefig="img/rol_vol.png")
    qs.plots.rolling_sharpe(port, "SPY", savefig="img/rol_beta_sharpe.png")
    qs.plots.rolling_sortino(port, "SPY", savefig="img/rol_beta_sortino.png")

    qs.plots.drawdowns_periods(port, savefig="img/drawdown_periods.png")
    qs.plots.drawdown(port, savefig="img/drawdown_plot.png")
    qs.plots.monthly_returns(port, savefig="img/monthly_returns.png")
    qs.plots.distribution(port, savefig="img/return_quantiles.png")


def create_corr_heatmap(numShares, historicalValue):
    """TODO: docstring"""

    avgStockPrice = historicalValue.divide(numShares, axis=1)
    stockCorr = avgStockPrice.corr(method="pearson")
    sns.heatmap(
        stockCorr,
        annot=False,
        cmap="coolwarm",
        xticklabels=True,
        yticklabels=True,
        vmin=-1,
        vmax=1,
    )
    plt.title("Portfolio Correlation")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.savefig("img/portfolio_corr.png")

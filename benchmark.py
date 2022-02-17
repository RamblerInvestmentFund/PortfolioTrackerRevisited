import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from tqdm import tqdm


def create_benchmark(df, historicalValue):
    """Creates Benchmark Portfolio Value"""

    totalHoldingStart = historicalValue.iloc[0]

    sums = {k: 0 for k in ["Equity", "Commodity", "REIT", "Bond"]}
    for i, (ticker, asset_class) in enumerate(zip(df["Ticker"], df["Type"])):
        if asset_class in sums.keys():
            sums[asset_class] += totalHoldingStart[i]

    "TODO: not used"
    startSum = [v for v in sums.values()]

    ECRB_ETF = ["SPY", "USCI", "VNQ", "TLT"]

    benchmarkHistorical = yf.download(ECRB_ETF, start="2021-06-21")["Close"]
    benchmarkStart = benchmarkHistorical.iloc[0]

    benchmarkShares = [
        (sums["Equity"] / benchmarkStart["SPY"]),
        (sums["Bond"] / benchmarkStart["TLT"]),
        (sums["Commodity"] / benchmarkStart["USCI"]),
        (sums["REIT"] / benchmarkStart["VNQ"]),
    ]

    benchmarkHistorical = benchmarkHistorical.mul(benchmarkShares, axis=1)
    benchPortfolioValue = pd.DataFrame(
        columns=["Portfolio"], index=benchmarkHistorical.index
    )
    benchPortfolioValue["Portfolio"] = benchmarkHistorical.sum(axis=1)

    '''TODO: not used'''
    benchmarkValue = benchPortfolioValue["Portfolio"][-1]

    "TODO: Ask lab director about hosting"
    # - UUP (.05), REET(.05), USCI(.15), TLT(0.25), SPY(0.5)

    return totalHoldingStart, benchPortfolioValue


def plot_benchmark(portfolioValue, benchPortfolioValue):
    """TODO: docstring"""

    print("Plotting Benchmark against Portfolio")

    plt.style.use("Solarize_Light2")
    plt.plot(portfolioValue, color="red", label="RIF")
    plt.plot(benchPortfolioValue, color="blue", label="Benchmark")
    
    plt.title("Portfolio Growth Since The Rebalance V.S. Benchmark", y=1.05)
    plt.ylabel("Portfolio Change")
    plt.xlabel("Days Since Rebalance")

    plt.legend()
    plt.xticks(rotation=20)

    plt.tight_layout()
    plt.savefig("img/portfolioVSbenchmark.png")
    # plt.show()


def main():
    pass


if __name__ == "__main__":
    main()

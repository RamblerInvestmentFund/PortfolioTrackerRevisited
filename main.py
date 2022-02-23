"""generates html tearsheet"""

import quantstats as qs

from data import pull_data


def tearsheet():
    """generates html tearsheet"""

    """TODO
    - portfolio.csv file
        - update for this semester
        - currently just have 2020
    - go to slack for history google slides
    - portfolio semester [1..4]
        - read it seperately
        - then concatenate
        - name them as [equity .. REIT] if convenient otw dw

    nextsteps:
        - all available methods
            [f for f in dir(qs.stats) if f[0] != '_']
            [f for f in dir(qs.plots) if f[0] != '_']

        - full automation
            https://developers.google.com/sheets/api/quickstart/python
    """

    *_, portfolioValueExtended = pull_data("assets/portfolio.csv")
    port = portfolioValueExtended['Portfolio']

    # writes html
    qs.extend_pandas()
    filename = "rif_vs_bench.html"
    qs.reports.html(port, "SPY", output=filename, download_filename=filename)


def main():
    tearsheet()


if __name__ == "__main__":
    main()

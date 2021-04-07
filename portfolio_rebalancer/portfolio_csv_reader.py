import csv

from click import ClickException

from portfolio_rebalancer.portfolio import Portfolio
from portfolio_rebalancer.portfolio_asset import PortfolioAsset


class PortfolioCsvReader:
    '''Reads and verifies the CSV-file containing the following info on each
    row in the following order:
    - Asset name/ticker
    - Current number of shares owned of the asset
    - Target allocation for the assert (expressed as a percentage value)
    '''

    def __init__(self, portfolio_csv):
        self._portfolio_csv = portfolio_csv

    @property
    def portfolio_csv(self):
        return self._portfolio_csv

    def _sanitize_shares(self, shares, line_num):
        try:
            return float(shares)
        except ValueError:
            raise ClickException(
                "Row {} - Shares is not a float/integer".format(line_num))

    def _sanitize_target_allocation(self, target_allocation, line_num):
        try:
            return float(target_allocation)
        except ValueError:
            raise ClickException(
                "Row {} - Target allocation is not a float/integer".format(
                    line_num))

    def get_portfolio(self):
        portfolio = Portfolio()
        total_allocation_pct = 0.0
        seen_assets = set()
        with open(self.portfolio_csv, newline='') as f:
            reader = csv.reader(f)
            for line_num, row in enumerate(reader):
                if len(row) != 3:
                    raise ClickException(
                        "Row {} malformed - expecting row in this format: "
                        "TICKER SHARES_OWNED TARET_ALLOCATION".format(
                            line_num))
                name = row[0]
                shares = self._sanitize_shares(row[1], line_num)
                target_allocation = self._sanitize_target_allocation(row[2],
                                                                     line_num)
                asset = PortfolioAsset(name, shares, target_allocation)
                if name not in seen_assets:
                    seen_assets.add(name)
                    portfolio.add_asset(asset)
                else:
                    raise ClickException("Asset name {} appears twice on row "
                                         "{}".format(name, line_num))
                total_allocation_pct += target_allocation
        if total_allocation_pct != 100:
            raise ClickException("Total combined allocation percentage of all "
                                 "rows is over 100%.")
        return portfolio

import click
import csv

from ws_rebalancer.position import Position
from ws_rebalancer.security import Security


class TargetAllocationsCsvReader:
    '''Reads and verifies the CSV-file containing the following info on each
    row in the following order:
    1. Asset name/ticker
    2. Target allocation for the assert (expressed as a percentage value)

    Will compare the ticker to see if it can be found in your current
    portfolio. If it can be found, it will extract the number of shares owned.
    Otherwise, it will assume that you own 0 shares of the asset.
    '''

    def __init__(self, target_allocations_csv, ws):
        self._target_allocations_csv = target_allocations_csv
        self._ws = ws

    def _verify_columns_in_row(self, row, row_num):
        """Ensure that the number of the columns in the row is expected."""
        if len(row) != 2:
            raise click.ClickException(
                "Row {} malformed - expecting row in this format: "
                "TICKER TARET_ALLOCATION".format(row_num))

    def _verify_all_positions_have_target_allocation(self, portfolio):
        """Ensure that every position in the portfolio has a target
        allocation.
        """
        for position in portfolio.positions.values():
            if not position.target_allocation:
                raise click.ClickException(
                    "Ticker {} does not have a target allocation".format(
                        position.ticker))

    def _verify_total_target_allocation(self, total_target_allocation):
        """Ensure that the total target allocation of all positions in the
        portfolio is exactly 100.
        """
        if total_target_allocation != 100:
            raise click.ClickException(
                "Total combined allocation percentage ({}) of all rows is not "
                "100%".format(total_target_allocation))

    def _sanitize_ticker(self, row):
        """Ticker should be in the first column of the CSV."""
        return row[0]

    def _sanitize_target_allocation(self, row, row_num):
        """Target allocation should be in the second column of the CSV."""
        try:
            target_allocation = row[1].strip('%')
            return float(target_allocation)
        except ValueError:
            raise click.ClickException(
                "Row {} - Target allocation is not a float/integer".format(
                    row_num))

    def _get_security(self, ticker_query, row_num):
        """Search for the security on WealthSimple given a ticker query."""
        securities = self._ws.get_securities_from_ticker(ticker_query)
        if len(securities) == 0:
            raise click.ClickException(
                "Row {} - ticker '{}' cannot be found".format(row_num,
                                                              ticker_query))
        for security_num, security in enumerate(securities):
            ticker = security['stock']['symbol']
            name = security['stock']['name']
            exchange = security['stock']['primary_exchange']
            click.echo("{}. Ticker: {}, Name: {}, Exchange: {}".format(
                security_num, ticker, name, exchange))
        security_idx = click.prompt("Please input the security you want",
                                    type=int)
        security_id = securities[security_idx]['id']
        security = self._ws.get_security(security_id)
        ticker = security['stock']['symbol']
        price = float(security['quote']['amount'])
        return Security(security_id, ticker, price)

    def update_portfolio(self, portfolio):
        """Assign target allocations to the positions in the portfolio and add
        any new positions that are present in the target-allocations CSV but
        not in the current portfolio. These are new positions that we want to
        open in our portfolio.
        """
        seen_tickers = set()
        total_allocation_pct = 0.0
        with open(self._target_allocations_csv, newline='') as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader):
                self._verify_columns_in_row(row, row_num)
                ticker = self._sanitize_ticker(row)
                target_allocation = self._sanitize_target_allocation(row,
                                                                     row_num)
                if ticker not in portfolio.positions:
                    # Ticker cannot be found in the current portfolio
                    security = self._get_security(ticker, row_num)
                    if ticker != security.ticker:
                        # Ticker is not spelled correctly in the target
                        # allocations CSV file - needs to be renamed
                        raise click.ClickException(
                            "Row {} - rename ticker '{}' to '{}'".format(
                                row_num, ticker, security.ticker))
                    click.secho(
                        "Warning: '{}' is not in your portfolio".format(
                            ticker),
                        fg='red')
                    position = Position(
                        security.ticker,
                        0,
                        security.price,
                        target_allocation=target_allocation)
                    portfolio.add_position(position)
                else:
                    # Ticker exists in the portfolio
                    position = portfolio[ticker]
                    position.target_allocation = target_allocation
                if ticker in seen_tickers:
                    raise click.ClickException(
                        "Duplicate entry of ticker '{}' on row {}".format(
                            ticker, row_num))
                seen_tickers.add(ticker)
                total_allocation_pct += target_allocation
        self._verify_all_positions_have_target_allocation(portfolio)
        self._verify_total_target_allocation(total_allocation_pct)
        return portfolio

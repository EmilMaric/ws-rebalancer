import click

from ws_rebalancer.portfolio import Portfolio
from ws_rebalancer.position import Position


class WealthSimplePortfolioReader:
    """Reads in the selected WealthSimple account along with the buying power
    and positions in that account and generates a Portfolio object with this
    information to be used for rebalancing.
    """

    def __init__(self, ws):
        self._ws = ws

    def _generate_portfolio(self, buying_power, positions):
        portfolio = Portfolio(buying_power)
        for position in positions:
            ticker = position['stock']['symbol']
            qty = position['quantity']
            price = float(position['quote']['amount'])
            position = Position(ticker, qty, price)
            portfolio.add_position(position)
        return portfolio

    def get_portfolio(self):
        account_ids = self._ws.get_account_ids()
        for account_num, account_id in enumerate(account_ids):
            click.echo("{}. {}".format(account_num, account_id))
        account_idx = click.prompt("Please input the account you want",
                                   type=int)
        account_id = account_ids[account_idx]
        account = self._ws.get_account(account_id)
        buying_power = float(account['buying_power']['amount'])
        positions = self._ws.get_positions(account_id)
        return self._generate_portfolio(buying_power, positions)

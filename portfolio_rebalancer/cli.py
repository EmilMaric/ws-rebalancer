import click

from portfolio_rebalancer.portfolio_csv_reader import PortfolioCsvReader
from portfolio_rebalancer.rebalancer import Rebalancer


@click.group()
def portfolio_rebalancer():
    pass


@portfolio_rebalancer.command(help=("Generate the recommended buys to get "
                                    "your portfolio as close as possible to "
                                    "your target allocation given a sum to "
                                    "invest."))
@click.argument('sum-to-invest', type=click.INT)
@click.option('-p', '--portfolio', 'portfolio_csv', required=True,
              help="CSV-file containing the portfolio and target allocations.")
def calc(sum_to_invest, portfolio_csv):
    portfolio = PortfolioCsvReader(portfolio_csv).get_portfolio()
    rebalancer = Rebalancer(portfolio)
    rebalancer.get_buys_for_rebalancing(sum_to_invest)

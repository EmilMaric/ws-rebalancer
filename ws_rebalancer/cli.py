import click

from ws_rebalancer.target_allocations_csv_reader import (
    TargetAllocationsCsvReader
)
from ws_rebalancer.rebalancer import Rebalancer
from ws_rebalancer.wealthsimple_login import WealthSimpleLogin
from ws_rebalancer.wealthsimple_portfolio_reader import (
    WealthSimplePortfolioReader
)


@click.group()
def ws_rebalancer():
    pass


@ws_rebalancer.command(help=(
    "Generate the recommended buys to get your portfolio as close as possible "
    "to your target allocation."))
@click.option('-t', '--target-allocations-csv', 'target_allocations_csv',
              required=True,
              help="CSV-file containing the target allocations for each "
                   "ticker")
@click.option('--email', required=True, help="Email for WealthSimple login")
@click.password_option(help="Password for WealthSimple login", required=True)
@click.option('--2fa', 'two_factor_auth', is_flag=True,
              help="Enable this flag if your WealthSimple login requires 2FA")
def rebalance(target_allocations_csv, email, password, two_factor_auth):
    try:
        ws = WealthSimpleLogin(email, password,
                               two_factor_auth=two_factor_auth)
    except Exception as e:
        raise click.ClickException("{}".format(str(e)))
    portfolio = WealthSimplePortfolioReader(ws).get_portfolio()
    TargetAllocationsCsvReader(target_allocations_csv, ws).update_portfolio(
        portfolio)
    Rebalancer.print_buys_for_rebalancing(portfolio)

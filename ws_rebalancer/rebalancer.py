import click
import copy


class Rebalancer:
    """Prints a list of buys that will help the current portfolio move closest
    to the target allocations.
    """

    @staticmethod
    def _position_with_highest_drift(portfolio):
        """Finds the position within the portfolio with the highest drift
        percentage. Positions that can not be bought because the price of
        acquiring a single share is more than the remaining cash amount are not
        considered.
        """
        def valid_drift_pct(drift_pcts):
            ticker = drift_pcts[0]
            position_pct = drift_pcts[1]
            price = portfolio[ticker].price
            return price <= portfolio.buying_power and position_pct <= 0.0
        position_with_highest_drift = None
        highest_drift_pct = None
        drift_percentages = portfolio.drift_percentages()
        # filter out positions where the current allocation is bigger than the
        # target allocation since a buy will only make this drift bigger, and
        # where the price to acquire a single share of the asset is bigger than
        # the remaining cash available
        drift_percentages = dict(filter(valid_drift_pct,
                                        drift_percentages.items()))
        for ticker, drift_pct in drift_percentages.items():
            position = portfolio[ticker]
            if not position_with_highest_drift:
                position_with_highest_drift = position
                highest_drift_pct = drift_pct
            elif drift_pct < highest_drift_pct:
                position_with_highest_drift = position
                highest_drift_pct = drift_pct
            elif (drift_pct == highest_drift_pct and
                  position.price < position_with_highest_drift.price):
                position_with_highest_drift = position
                highest_drift_pct = drift_pct
        return position_with_highest_drift

    @staticmethod
    def print_buys_for_rebalancing(old_portfolio):
        """Prints a list of buys needed to bring the portfolio as close as
        possible to the target allocations.
        """
        new_portfolio = copy.deepcopy(old_portfolio)
        buys = {}
        while new_portfolio.buying_power > 0.0:
            position = Rebalancer._position_with_highest_drift(new_portfolio)
            if not position:
                # No positions remain that are below the target allocation and
                # have a unit price less than the remaning cash amount
                break
            new_portfolio[position.ticker].qty += 1
            new_portfolio.buying_power -= position.price
            if position.ticker not in buys:
                buys[position.ticker] = 0
            buys[position.ticker] += 1
        for ticker, buy_amount in buys.items():
            position = new_portfolio[ticker]
            allocation = new_portfolio.get_current_allocation(ticker)
            click.echo("Buy {}X {} @ {:.2f} - New allocation {:.2f}%".format(
                buy_amount, ticker, position.price, round(allocation, 2)))
        click.echo("Remaining cash ${:.2f}".format(new_portfolio.buying_power))

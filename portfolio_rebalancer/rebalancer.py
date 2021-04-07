import click


class Rebalancer:
    """Generates a list of buys that will help the current portfolio move
    closer to the target allocations.
    """

    def __init__(self, portfolio):
        self._portfolio = portfolio

    def _get_asset_with_highest_drift_pct(self, remaining_cash_amount):
        def valid_drift_pct(drift_pcts):
            asset_name = drift_pcts[0]
            drift_pct = drift_pcts[1]
            price = self._portfolio[asset_name].price
            return price <= remaining_cash_amount and drift_pct < 0.0
        asset_with_highest_drift_pct = None
        highest_drift_pct = None
        drift_percentages = self._portfolio.drift_percentages()
        # filter out drifts where the current allocation is bigger than the
        # target allocation since a buy will only make this drift bigger, and
        # where the price to acquire a single unit of the asset is bigger than
        # the remaining cash available
        drift_percentages = dict(filter(valid_drift_pct,
                                        drift_percentages.items()))
        for asset_name, drift_pct in drift_percentages.items():
            asset = self._portfolio[asset_name]
            if not asset_with_highest_drift_pct:
                asset_with_highest_drift_pct = asset
                highest_drift_pct = drift_pct
            elif drift_pct < highest_drift_pct:
                asset_with_highest_drift_pct = asset
                highest_drift_pct = drift_pct
            elif (drift_pct == highest_drift_pct and
                  asset.price < asset_with_highest_drift_pct.price):
                asset_with_highest_drift_pct = asset
                highest_drift_pct = drift_pct
        return asset_with_highest_drift_pct

    def get_buys_for_rebalancing(self, cash_amount):
        remaining_cash = cash_amount
        buys = {}
        while remaining_cash > 0:
            asset = self._get_asset_with_highest_drift_pct(remaining_cash)
            if not asset:
                # No assets remain that are below the target allocation and
                # have a unit price less than the remaning cash amount
                break
            self._portfolio.buy_asset(asset)
            if asset.name not in buys:
                buys[asset.name] = 0
            buys[asset.name] += 1
            remaining_cash -= asset.price

        for asset_name, buy_amount in buys.items():
            asset = self._portfolio[asset_name]
            asset_allocation = self._portfolio.get_allocation(asset)
            click.echo("Buy {}X {} @ {:.2f} - New allocation {:.2f}%".format(
                buy_amount, asset_name, asset.price, round(asset_allocation,
                                                           2)))
        click.echo("Remaining cash ${:.2f}".format(remaining_cash))

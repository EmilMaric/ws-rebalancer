class Portfolio:
    """Represents a collection of portfolio assets."""

    def __init__(self):
        self._assets = {}
        self._total = 0.0

    def __getitem__(self, asset_name):
        return self._assets[asset_name]

    def add_asset(self, asset):
        self._total += asset.price * asset.qty
        self._assets[asset.name] = asset

    def buy_asset(self, asset):
        asset.qty += 1
        self._total += asset.price

    def drift_percentages(self):
        drift_pcts = {}
        for asset in self._assets.values():
            current_allocation_pct = 0.0
            if self._total > 0.0:
                current_allocation_pct = asset.price * asset.qty / self._total
                current_allocation_pct *= 100
            drift = current_allocation_pct - asset.target_allocation
            drift_pct = (drift * 100) / asset.target_allocation
            drift_pcts[asset.name] = drift_pct
        return drift_pcts

    def get_allocation(self, asset):
        return (asset.price * asset.qty * 100) / self._total

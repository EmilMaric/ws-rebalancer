import yfinance as yf


class PortfolioAsset:
    """Holds information about each asset in the portfolio."""

    def __init__(self, name, qty, target_allocation):
        self._name = name
        self._price = self._fetch_asset_price()
        self._qty = qty
        self._target_allocation = target_allocation

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def qty(self):
        return self._qty

    @property
    def target_allocation(self):
        return self._target_allocation

    @qty.setter
    def qty(self, qty):
        self._qty = qty

    def _fetch_asset_price(self):
        asset = yf.Ticker(self._name)
        return asset.info['regularMarketPrice']

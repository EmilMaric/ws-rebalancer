class Position:
    """Holds information about a position in the portfolio."""

    def __init__(self, ticker, qty, price, target_allocation=None):
        self._ticker = ticker
        self._qty = qty
        self._price = price
        self._target_allocation = target_allocation

    @property
    def ticker(self):
        return self._ticker

    @property
    def qty(self):
        return self._qty

    @property
    def price(self):
        return self._price

    @property
    def target_allocation(self):
        return self._target_allocation

    @qty.setter
    def qty(self, qty):
        self._qty = qty

    @target_allocation.setter
    def target_allocation(self, target_allocation):
        self._target_allocation = target_allocation

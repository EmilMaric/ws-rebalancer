class Security:
    """Contains information about a security on WealthSimple."""

    def __init__(self, security_id, ticker, price):
        self._security_id = security_id
        self._ticker = ticker
        self._price = price

    @property
    def ticker(self):
        return self._ticker

    @property
    def price(self):
        return self._price

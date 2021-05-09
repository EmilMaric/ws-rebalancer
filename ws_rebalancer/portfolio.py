class Portfolio:
    """Represents a collection of positions in a portfolio."""

    def __init__(self, buying_power):
        self._positions = {}
        self._buying_power = buying_power

    def __getitem__(self, ticker):
        return self._positions[ticker]

    def _total(self):
        """The total value of the portfolio."""
        total = 0.0
        for position in self._positions.values():
            total += position.price * position.qty
        return total

    @property
    def positions(self):
        """Get the positions that are a part of this portfolio."""
        return self._positions

    @property
    def buying_power(self):
        """Get the amount of cash that is available to be used for trading."""
        return self._buying_power

    @buying_power.setter
    def buying_power(self, buying_power):
        """Set the new amount of cash that is available to be used for
        trading.
        """
        self._buying_power = buying_power

    def add_position(self, position):
        """Add a position to the portfolio."""
        self._positions[position.ticker] = position

    def drift_percentages(self):
        """Get the drift percentages for all the positions in this portfolio.
        Drift percentage is defined by how far away a position is from its
        target allocation.
        A negative drift percentage means that the current position allocation
        is under the target allocation.
        A positive drift percentage means that the current position allocation
        is over the target allocation.
        """
        drift_pcts = {}
        for position in self._positions.values():
            current_allocation_pct = 0.0
            if self._total() > 0.0:
                position_value = position.price * position.qty
                current_allocation_pct = position_value / self._total()
                current_allocation_pct *= 100
            drift = current_allocation_pct - position.target_allocation
            drift_pct = (drift * 100) / position.target_allocation
            drift_pcts[position.ticker] = drift_pct
        return drift_pcts

    def get_current_allocation(self, ticker):
        """Returns the portion of the current portfolio that is comprised of
        the queried ticker.
        """
        position = self._positions[ticker]
        return (position.price * position.qty * 100) / self._total()

import pytest

from unittest.mock import MagicMock


class MockTicker(MagicMock):
    def __init__(self, name):
        MagicMock.__init__(self)
        self._name = name
        self._info = {'regularMarketPrice': self.test_prices[name]}

    @property
    def info(self):
        return self._info


@pytest.fixture(scope="session")
def testfiles_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("testfiles")


@pytest.fixture(scope='function')
def ticker_mock(mocker):
    mock_obj = mocker.patch('portfolio_rebalancer.portfolio_asset.yf.Ticker',
                            new=MockTicker)
    return mock_obj

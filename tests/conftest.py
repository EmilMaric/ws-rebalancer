import pytest

from ws_rebalancer.wealthsimple_login import WealthSimpleLogin


class WealthSimpleLoginMock:
    """Mocks the WealthSimpleLogin class which provides the WSTrade API. This
    allows us to mock out the API calls we make in the app so that we don't
    actually make calls to the WealthSimple Trade API backend as that would
    get us rate-limited pretty quickly, or even blocke if they think we're
    DDOSing them.
    """
    def __init__(self, email, password, two_factor_callback=None):
        self._accounts = {}
        self._positions = {}
        self._securities = []
        # build the dict containing info on the positions held by the client
        # in the tests
        if hasattr(self, 'test_positions'):
            for account_id, account in self.test_positions.items():
                self._positions[account_id] = []
                buying_power = account['buying_power']
                self._accounts[account_id] = {
                    'buying_power': {'amount': buying_power}}
                for ticker, position in account['positions'].items():
                    position_dict = {'stock': {}, 'quote': {}}
                    position_dict['stock']['symbol'] = ticker
                    position_dict['quantity'] = position['qty']
                    position_dict['quote']['amount'] = position['price']
                    self._positions[account_id].append(position_dict)
        # build the dict containing info on the securities used in the tests
        if hasattr(self, 'test_securities'):
            for ticker, security_info in self.test_securities.items():
                security_dict = {'id': None, 'stock': {}, 'quote': {}}
                security_dict['id'] = security_info['id']
                security_dict['stock']['symbol'] = ticker
                security_dict['stock']['name'] = security_info['name']
                security_dict['stock']['primary_exchange'] = (
                    security_info['exchange'])
                security_dict['quote']['amount'] = security_info['price']
                self._securities.append(security_dict)
        # simulate calling the sample two_factor_auth function
        two_factor_callback()

    def get_account_ids(self):
        return list(self._accounts.keys())

    def get_account(self, account_id):
        return self._accounts[account_id]

    def get_positions(self, account_id):
        return self._positions[account_id]

    def get_securities_from_ticker(self, ticker):
        securities = []
        for security in self._securities:
            if ticker in security['stock']['symbol']:
                securities.append(security)
        return securities

    def get_security(self, security_id):
        for security in self._securities:
            if security['id'] == security_id:
                return security


@pytest.fixture(scope="session")
def testfiles_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("testfiles")


@pytest.fixture(scope="session", autouse=True)
def wslogin_base_patch():
    # We need to manually set the base class of WealthSimpleLogin class to be
    # the mock class because otherwise it will keep using the WSTrade class
    # even after patching
    WealthSimpleLogin.__bases__ = (WealthSimpleLoginMock,)


@pytest.fixture(scope='function')
def wslogin_mock(mocker):
    mock_obj = mocker.patch(
        'ws_rebalancer.wealthsimple_login.wealthsimple.WSTrade',
        new=WealthSimpleLoginMock)
    mock_obj.test_positions = {}
    mock_obj.test_securities = {}
    yield mock_obj
    # Everything past this point occurs once the test using this fixture has
    # completed. Delete any class attributes we may have set in our tests
    if hasattr(mock_obj, 'test_positions'):
        del mock_obj.test_positions
    if hasattr(mock_obj, 'test_securities'):
        del mock_obj.test_securities

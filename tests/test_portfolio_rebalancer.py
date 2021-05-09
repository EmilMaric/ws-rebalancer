from click.testing import CliRunner

from ws_rebalancer.cli import ws_rebalancer as wr
from tests.helpers import create_csv_file


def test_multiple_buys(testfiles_dir, wslogin_mock):
    """Basic verification test that verifies that the functionality of the app
    is correct when we have multiple different tickers to buy.
    """
    # To buy with lump sum:
    # 5X MSFT
    # 1X APPL
    # 1X GOOG
    test_portfolio = [
        ['MSFT', '50'],
        ['APPL', '30'],
        ['GOOG', '20'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 100.00,
            'positions': {
                'MSFT': {
                    'price': 10.00,
                    'qty': 3,
                },
                'APPL': {
                    'price': 20.00,
                    'qty': 2,
                },
                'GOOG': {
                    'price': 30.00,
                    'qty': 1,
                },
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 0
    assert """\
Buy 5X MSFT @ 10.00 - New allocation 40.00%
Buy 1X APPL @ 20.00 - New allocation 30.00%
Buy 1X GOOG @ 30.00 - New allocation 30.00%
Remaining cash $0.00
""" in result.output


def test_same_drift(testfiles_dir, wslogin_mock):
    """Test that the app correctly picks stock with lower price to buy if
    drifts are identical. This test also additionally tests the case where we
    have some cash remaining, but aren't able to allocate it to any asset.
    """
    test_portfolio = [
        ['MSFT', '40'],
        ['APPL', '40'],
        ['GOOG', '20'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 30.00,
            'positions': {
                'MSFT': {
                    'price': 55.00,
                    'qty': 1,
                },
                'APPL': {
                    'price': 30.00,
                    'qty': 1,
                },
                'GOOG': {
                    'price': 15.00,
                    'qty': 1,
                },
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 0
    assert """\
Buy 1X GOOG @ 15.00 - New allocation 26.09%
Remaining cash $15.00
""" in result.output


def test_malformed_target_allocation_value(testfiles_dir, wslogin_mock):
    """Test that the app correctly prints a message informing the user that
    they have entered a non-intenger or non-float for the target allocation
    column of a particular asset.
    """
    test_portfolio = [
        ['MSFT', 'BLAH'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 30.00,
            'positions': {
                'MSFT': {
                    'price': 55.00,
                    'qty': 1,
                },
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Row 0 - Target allocation is not a float/integer
"""


def test_same_asset_multiple_times(testfiles_dir, wslogin_mock):
    """Test that the app correctly prints a message informing the user that
    they have entered the same asset twice on separate lines in the portfolio
    CSV file.
    """
    test_portfolio = [
        ['MSFT', '40'],
        ['APPL', '40'],
        ['MSFT', '20'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 30.00,
            'positions': {
                'MSFT': {
                    'price': 55.00,
                    'qty': 1,
                },
                'APPL': {
                    'price': 30.00,
                    'qty': 1,
                },
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Duplicate entry of ticker 'MSFT' on row 2
"""


def test_portfolio_target_allocation_over_100(testfiles_dir, wslogin_mock):
    """Test that the app correctly prints a message informing the user that
    the sum of all target allocations for the assets in the portfolio is over
    100 percent.
    """
    test_portfolio = [
        ['MSFT', '60'],
        ['APPL', '50'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 30.00,
            'positions': {
                'MSFT': {
                    'price': 55.00,
                    'qty': 1,
                },
                'APPL': {
                    'price': 30.00,
                    'qty': 1,
                },
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Total combined allocation percentage (110.0) of all rows is not 100%
"""


def test_no_assets(testfiles_dir, wslogin_mock):
    """Test that the app correctly prints a message informing the user that
    row is badly formatted.
    """
    test_portfolio = [[]]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 30.00,
            'positions': {
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Row 0 malformed - expecting row in this format: TICKER TARET_ALLOCATION
"""


def test_invalid_login(testfiles_dir, mocker):
    """Test that if the login raises an error, the app handles it correctly.
    """
    test_portfolio = [
        ['MFST', '100']
    ]
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    mock_obj = mocker.patch('ws_rebalancer.cli.WealthSimpleLogin')
    mock_obj.side_effect = Exception("Invalid login")

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Invalid login
"""


def test_no_target_allocation(testfiles_dir, wslogin_mock):
    """Test that we raise an error when our portfolio contains assets without
    a designated target allocation.
    """
    test_portfolio = [
        ['GOOG', '100'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 100.00,
            'positions': {
                'MSFT': {
                    'price': 55.00,
                    'qty': 1,
                },
                'GOOG': {
                    'price': 30.00,
                    'qty': 1,
                },
            }
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Ticker MSFT does not have a target allocation
"""


def test_multiple_accounts(testfiles_dir, wslogin_mock):
    """Test that we are able to select a single account when multiple are
    present.
    """
    test_portfolio = [
        ['GOOG', '100'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 100.00,
            'positions': {
                'MSFT': {
                    'price': 50.00,
                    'qty': 1,
                },
            }
        },
        1: {
            'buying_power': 50.00,
            'positions': {
                'GOOG': {
                    'price': 30.00,
                    'qty': 1,
                },
            }
        },
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n1\n',
                           catch_exceptions=False)

    assert result.exit_code == 0
    assert """\
Buy 1X GOOG @ 30.00 - New allocation 100.00%
Remaining cash $20.00
""" in result.output


def test_ticker_not_found(testfiles_dir, wslogin_mock):
    """Test that error is thrown when ticker in the target-allocations file
    cannot be found.
    """
    test_portfolio = [
        ['GOOG', '100'],
    ]
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 50.00,
            'positions': {}
        }
    }
    wslogin_mock.test_securities = {}
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.stderr == """\
Error: Row 0 - ticker 'GOOG' cannot be found
"""


def test_multiple_tickers_not_in_portfolio(testfiles_dir, wslogin_mock):
    """Test that when Wealthsimple portfolio is missing multiple tickers from
    the target allocations CSV-file, the app correctly assumes that our
    position is 0 shares in it with the current price.
    """
    test_portfolio = [
        ['MSFT', '100'],
    ]
    wslogin_mock.test_securities = {
        'MSFT': {
            'id': '123456',
            'name': 'Microsoft',
            'price': 100.00,
            'exchange': 'NYSE',
        },
        'MSFT.TO': {
            'id': '123457',
            'name': 'Macrosoft',
            'price': 200.00,
            'exchange': 'TSX',
        },
    }
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 100.00,
            'positions': {}
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n0\n',
                           catch_exceptions=False)

    assert result.exit_code == 0
    assert """\
Buy 1X MSFT @ 100.00 - New allocation 100.00%
Remaining cash $0.00
""" in result.output


def test_mistyped_ticker_not_in_portfolio(testfiles_dir, wslogin_mock):
    """Test case where the target allocations CSV has a ticker that is wrongly
    spelled and doesn't exist in portfolio.
    """
    test_portfolio = [
        ['MSF', '100'],
    ]
    wslogin_mock.test_securities = {
        'MSFT': {
            'id': '123456',
            'name': 'Microsoft',
            'price': 100.00,
            'exchange': 'NYSE',
        },
        'MSFT.TO': {
            'id': '123457',
            'name': 'Macrosoft',
            'price': 200.00,
            'exchange': 'TSX',
        },
    }
    wslogin_mock.test_positions = {
        0: {
            'buying_power': 100.00,
            'positions': {}
        }
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(wr,
                           ['rebalance', '-t', test_portfolio_csv, '--email',
                            'test@mail.com', '--2fa'],
                           input='password\npassword\n12345\n0\n0\n',
                           catch_exceptions=False)
    assert result.exit_code == 1
    assert result.stderr == """\
Error: Row 0 - rename ticker 'MSF' to 'MSFT'
"""

from click.testing import CliRunner

from portfolio_rebalancer.cli import portfolio_rebalancer as pr
from tests.helpers import create_csv_file


def test_multiple_buys(testfiles_dir, ticker_mock):
    """Basic verification test that verifies that the functionality of the app
    is correct when we have multiple different tickers to buy.
    """
    # To buy with lump sum:
    # 5X MSFT
    # 1X APPL
    # 1X GOOG
    test_portfolio = [
        ['MSFT', '3', '50'],
        ['APPL', '2', '30'],
        ['GOOG', '1', '20'],
    ]
    ticker_mock.test_prices = {
        'MSFT': 10.00,
        'APPL': 20.00,
        'GOOG': 30.00,
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '100'],
                           catch_exceptions=False)

    assert result.exit_code == 0
    assert result.output == """\
Buy 5X MSFT @ 10.00 - New allocation 40.00%
Buy 1X APPL @ 20.00 - New allocation 30.00%
Buy 1X GOOG @ 30.00 - New allocation 30.00%
Remaining cash $0.00
"""


def test_same_drift(testfiles_dir, ticker_mock):
    """Test that the app correctly picks stock with lower price to buy if
    drifts are identical. This test also additionally tests the case where we
    have some cash remaining, but aren't able to allocate it to any asset.
    """
    test_portfolio = [
        ['MSFT', '1', '40'],
        ['APPL', '1', '40'],
        ['GOOG', '1', '20'],
    ]
    ticker_mock.test_prices = {
        'MSFT': 55.00,
        'APPL': 30.00,
        'GOOG': 15.00,
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '30'],
                           catch_exceptions=False)

    assert result.exit_code == 0
    assert result.output == """\
Buy 1X GOOG @ 15.00 - New allocation 26.09%
Remaining cash $15.00
"""


def test_malformed_shares_value(testfiles_dir, ticker_mock):
    """Test that the app correctly prints a message informing the user that
    they have entered a non-intenger or non-float for the shares column of a
    particular asset.
    """
    test_portfolio = [
        ['MSFT', 'BLAH', '40'],
    ]
    ticker_mock.test_prices = {
        'MSFT': 55.00,
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '30'])

    assert result.exit_code == 1
    assert result.output == """\
Error: Row 0 - Shares is not a float/integer
"""


def test_malformed_target_allocation_value(testfiles_dir, ticker_mock):
    """Test that the app correctly prints a message informing the user that
    they have entered a non-intenger or non-float for the target allocation
    column of a particular asset.
    """
    test_portfolio = [
        ['MSFT', '1', 'BLAH'],
    ]
    ticker_mock.test_prices = {
        'MSFT': 55.00,
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '30'])

    assert result.exit_code == 1
    assert result.output == """\
Error: Row 0 - Target allocation is not a float/integer
"""


def test_same_asset_multiple_times(testfiles_dir, ticker_mock):
    """Test that the app correctly prints a message informing the user that
    they have entered the same asset twice on separate lines in the portfolio
    CSV file.
    """
    test_portfolio = [
        ['MSFT', '1', '40'],
        ['APPL', '1', '40'],
        ['MSFT', '1', '20'],
    ]
    ticker_mock.test_prices = {
        'MSFT': 55.00,
        'APPL': 30.00,
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '30'])

    assert result.exit_code == 1
    assert result.output == """\
Error: Asset name MSFT appears twice on row 2
"""


def test_portfolio_target_allocation_over_100(testfiles_dir, ticker_mock):
    """Test that the app correctly prints a message informing the user that
    the sum of all target allocations for the assets in the portfolio is over
    100 percent.
    """
    test_portfolio = [
        ['MSFT', '1', '60'],
        ['APPL', '1', '50'],
    ]
    ticker_mock.test_prices = {
        'MSFT': 55.00,
        'APPL': 30.00,
    }
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)

    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '30'])

    assert result.exit_code == 1
    assert result.output == """\
Error: Total combined allocation percentage of all rows is over 100%.
"""


def test_no_assets(testfiles_dir, ticker_mock):
    """Test that the app correctly prints a message informing the user that
    the sum of all target allocations for the assets in the portfolio is over
    100 percent.
    """
    test_portfolio = [[]]
    test_portfolio_csv = create_csv_file(testfiles_dir,
                                         "test_portfolio.csv",
                                         data=test_portfolio)
    runner = CliRunner()
    result = runner.invoke(pr, ['calc', '-p', test_portfolio_csv, '30'],
                           catch_exceptions=False)

    assert result.exit_code == 1
    assert result.output == """\
Error: Row 0 malformed - expecting row in this format: TICKER SHARES_OWNED TARET_ALLOCATION
"""  # noqa: E501

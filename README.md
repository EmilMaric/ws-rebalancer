WealthSimple Portfolio Rebalancer
=
[![Build](https://github.com/EmilMaric/ws-rebalancer/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/EmilMaric/ws-rebalancer/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/EmilMaric/ws-rebalancer/branch/main/graph/badge.svg?token=XJ371LIRJB)](https://codecov.io/gh/EmilMaric/ws-rebalancer)

A CLI tool that helps you rebalance your WealthSimple portfolio. The tool takes in a CSV-file that contains the target allocations for your
portfolio, and prints out a list of buys you should make to bring your portfolio closer to the target allocations you specified.

The tool will log you in to your WealthSimple account, where it will fetch your current positions & buying power, and will parse the CSV-file you defined to determine how far away each position is from the target allocation. It will then select the positions that are the farthest away from their target positions iteratively, until your buying power is used up.

## Limitations
- Currently the tool only supports doing buy-only rebalancing, meaning __it won't__ try to simulate any sells in order to rebalance.
- The tool only works with CAD denominated stocks and assumes your buying power is in CAD. If there is appetite for supporting other currencies then I can try to support that as well.
- Prices for the stocks are fetched off the WealthSimple Trade API as well, so the quotes may be delayed by 15 minutes.

# Installation
```
# To get the latest release
pip install ws-rebalancer
```

# CSV-file requirements
To start, create a CSV file that will contain tickers from assets in your current portfolio, as well as tickers for any new assets you would like to add.
In the CSV file, each line will represent a unique asset you own or want to own. On each line, you need to include the correct ticker for the asset and the target allocation for that asset. The format for each line is as follows:
```
<stock ticker>, <target allocation>
```

Here is a sample CSV file:
```
# sample-target-allocations.csv
MSFT, 50%
APPL, 30%
GOOG, 20%
```

In other words, I want my sample portfolio to be 50% Microsoft, 30% Apple, and 20% Google.

Make sure that the target allocations add up to 100%. The tool will raise an error and quit if that is not the case. You can also use decimals to represent fractional target allocations. Also don't repeat the same ticker twice. I've tried my best to sanitize the input and raise any errors that I can forsee with the CSV-file, but there may be some things that I didn't catch so please be careful.

# Usage
To generate the buys that will rebalance your portfolio as close as possible to the target allocation, run the tool as follows:
```
$ ws-rebalancer rebalance -t <target-allocations-CSV-file> --email <WealthSimple-email-login> [--2fa]
```

Using our `sample-target-allocations.csv` as above, a sample run could look as follows:
```
$ ws-rebalancer rebalance -t sample-target-allocations.csv --email test@gmail.com --2fa
Password:
Repeat for confirmation:
Enter 2FA code: 12345
0. non-registered
Please input the account you want: 0
Buy 5X MSFT @ 10.00 - New allocation 40.00%
Buy 1X APPL @ 20.00 - New allocation 30.00%
Buy 1X GOOG @ 30.00 - New allocation 30.00%
Remaining cash $0.00
```
Note that in this example, `MSFT` price was $10.00, `APPL` price was $20.00, and `GOOG` price was $30.00, and we had a buying power of $60.00 in this
account (although it is not shown). The tool also fetched our current positions and buying power for the specified account and then provided a list of
buys we should make in order to try to meet the specified target allocations.

# Finding Issues
If you find issues using this tool, please create an Issue using the [Github issue tracker](https://github.com/EmilMaric/ws-rebalancer/issues)
and I will try to address it as soon as I can.

# Contributing
If you would like to contribute, please read the [CONTRIBUTING.md](https://github.com/EmilMaric/ws-rebalancer/blob/main/CONTRIBUTING.md) page

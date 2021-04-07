# Portfolio Rebalancer
A CLI tool that informs you what buys you need to make to best rebalance your portfolio. The tool requires the following information in the form of a
CSV file:
- What assets you currently own. In the latest version, we only support putting a stock ticker here.
- How much of the asset you currently own.
- What the target allocation is of the asset in question
- A lump sum of cash that you're looking to invest in this portfolio

The tool will do the calculations necessary to tell you how much of each asset you need to buy (if at all) to bring your portfolio as close as 
possible to the target allocations you defined.

# Installation
# CSV-file requirements
To start, create a CSV file that will contain all of your portfolio. In the CSV file, each line will represent a unique asset you own. In the latest
version, asset is synonymous for stock, so just use the ticker. The format for each line is as follows:
```
<stock ticker>, <shares owned>, <target allocation>
```

Here is a sample CSV file:
```
# sample-portfolio.csv
MSFT, 3, 50
APPL, 2, 30
GOOG, 1, 20
```

In other words, in my current portfolio, I own 3 shares of MSFT, 2 shares of APPL, and 1 share of GOOG. I want my portfolio to be 40% MSFT, 40% APPL,
and 20% GOOG.

Without knowing the current prices, we can't say anything about the current allocations of our portfolio. However, this tool will pull
the latest prices from Yahoo Finance for each stock ticker in the portfolio list when doing it's calculations (so you don't need to provide it
yourself).

# Usage
To generate the buys that will move your portfolio as close as possible to the target allocation, run the tool as follows:
```
$ portfolio-rebalancer -p <portfolio CSV-file> <lump sum to invest>
```

Using our `sample-portfolio.csv` as above, a sample run could look as follows:
```
$ portfolio-rebalancer -p sample-portfolio.csv 
Buy 5X MSFT @ 10.00 - New allocation 40.00%
Buy 1X APPL @ 20.00 - New allocation 30.00%
Buy 1X GOOG @ 30.00 - New allocation 30.00%
Remaining cash $0.00
```
Note that in this example, MSFT price was $10.00, APPL price was $20.00, and GOOG price was $30.00.

# Finding Issues
If you find issues using this tool, please create an Issue using the [Github issue tracker](https://github.com/EmilMaric/portfolio-rebalancer/issues)
and I will try to address it as soon as I can.

# Contributing
If you would like to contribute, please read the [CONTRIBUTING.md](https://github.com/EmilMaric/portfolio-rebalancer/blob/main/CONTRIBUTING.md) page

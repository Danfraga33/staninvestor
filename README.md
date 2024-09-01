# Investment Analysis App

## Overview

This app performs investment analysis based on Stan Weinstein's approach. It calculates key indicators such as Relative Strength and Moving Averages using stock data and benchmarks. The app integrates data from Finnhub API and Yahoo Finance.

## Features

- **Calculate Relative Strength**: Computes the relative strength of a stock compared to a benchmark.
- **Calculate 30-Week Moving Average**: Computes the 30-week moving average of a stock.
- **Fetch Stock Symbols**: Retrieves a list of stock symbols from the Finnhub API.
- **Download Historical Data**: Downloads historical stock data from Yahoo Finance.

## Configuration

- **API Keys**: Replace `"your_api_key_here"` in the script with your actual Finnhub API key.

## Example

```python
import finnhub
import yfinance as yf

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key="your_api_key_here")

# Fetch stock symbols
us_symbols = finnhub_client.stock_symbols('US')

# Download historical data
df = yf.download("^SPX", start="2023-01-01")

# Calculate relative strength
# (Implement the functions from the script)
```

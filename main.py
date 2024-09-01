import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import yfinance as yf
import finnhub
import json

finnhub_client = finnhub.Client(api_key="co44i4hr01qqksebmuggco44i4hr01qqksebmuh0")
us_symbols = finnhub_client.stock_symbols('US')

tickers = []
for stock in us_symbols: 
   ticker = stock.get("displaySymbol", "Unknown")
   tickers.append(ticker)
   
print(tickers)

df = yf.download("^SPX", start="2023-01-01")

def calculate_relative_strength(stock_prices, benchmark_prices, window=50):
   df = pd.DataFrame({
      "Stock":stock_prices,
      "Benchmark":benchmark_prices
   })

   df["RS"] = df["Stock"]/df["Benchmark"]
   
   df["RS_MA"] = df["RS"].rolling(window=window).mean()
   
   return df[["RS", "RS_MA"]]


def thirty_week_MA(stock_prices, window=30):
   df = pd.DataFrame({
      "Stock_Prices":stock_prices
   })
   df["ThirtyW_MA"] = df["Stock_Prices"].rolling(window=window).mean()
   
   return df[["ThirtyW_MA"]]







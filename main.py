import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import yfinance as yf
import finnhub
import json
import os


finnhub_client = finnhub.Client(api_key="co44i4hr01qqksebmuggco44i4hr01qqksebmuh0")

us_sectors = [  
    'XLC',  
    'XLY',  
    'XLP',  
    'XLE',  
    'XLB',  
    'XLF', 
    'XLV' 
    'XLI',
    'XLRE',
    "XLK", 
    'XLU'] 




            
# US STOCKS
arcx_data = finnhub_client.stock_symbols('US', "ARCX")
df_arcx = pd.DataFrame(arcx_data)
us_sector_indicies = df_arcx[df_arcx["symbol"].isin(us_sectors)]
df_sectors = pd.DataFrame(us_sector_indicies)
df_sectors.to_csv('us_sectors.csv', index=False)

# NASDAQ TICKERS
nasdaq_symbols = finnhub_client.stock_symbols('US', "XNAS")
df_tickers = pd.DataFrame(nasdaq_symbols)
df_tickers.to_csv('tickers.csv', index=False)

tickers = pd.read_csv('tickers.csv')['symbol'].tolist()
sectors = pd.read_csv("us_sectors.csv")


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







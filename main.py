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

nasdaq_100_symbols = pd.read_excel("nasdaq_100_stocks.xlsx")
df_nasdaq_100 = pd.DataFrame(nasdaq_100_symbols)

# NASDAQ SECTOR MAPPING (GSIC to SPDR)
gics_to_spdr = {
    'Consumer Cyclical': 'XLC', 
    'Consumer Staples': 'XLP',  
    'Energy': 'XLE',  
    'Financials': 'XLF',  
    'Healthcare': 'XLV',  
    'Industrials': 'XLI',  
    'Technology': 'XLK',  
    'Utilities': 'XLU',  
    'Real Estate': 'XLRE',  
    'Communication Services': 'XLC',
    'Materials': 'XLB'  }

# CLEANING NASDAQ DATA
df_nasdaq_100["Sector"] = df_nasdaq_100["Sector"].map(gics_to_spdr)
df_nasdaq_100_cleaned = df_nasdaq_100.dropna(subset=['Sector'])
df_nasdaq_100_cleaned.to_csv("nasdaq100.csv")
nasdaq_tickers = pd.read_csv("nasdaq100.csv")



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







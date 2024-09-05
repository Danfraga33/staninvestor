import pandas as pd
# 30 Week MA
def thirty_week_MA(stock_prices, window=30):
   df = pd.DataFrame({
      "Stock_Prices":stock_prices
   })
   df["ThirtyW_MA"] = df["Stock_Prices"].rolling(window=window).mean()
   
   return df[["ThirtyW_MA"]]


# Relative Strength Indicator
def calculate_relative_strength(stock_prices, benchmark_prices, window=30):
   df = pd.DataFrame({
      "Stock":stock_prices,
      "Benchmark":benchmark_prices
   })

   df["RS"] = df["Stock"]/df["Benchmark"]
   
   df["RS_MA"] = df["RS"].rolling(window=window).mean()
   
   return df[["RS", "RS_MA"]]
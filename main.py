import pandas as pd
import streamlit as st
import numpy as np
import yfinance as yf
import finnhub
import plotly.express as px
import requests
import os
from datetime import datetime
from sector import gics_to_spdr
from indicators import calculate_relative_strength, thirty_week_MA
from flask import Flask,jsonify
from flask_cors import CORS

finnhub_client = finnhub.Client(api_key="co44i4hr01qqksebmuggco44i4hr01qqksebmuh0")
pd.set_option('display.max_rows', None)

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


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

            
# US SECTORS
arcx_data = finnhub_client.stock_symbols('US', "ARCX")
df_arcx = pd.DataFrame(arcx_data)
us_sector_indicies = df_arcx[df_arcx["symbol"].isin(us_sectors)]
df_sectors = pd.DataFrame(us_sector_indicies)
df_sectors.to_csv('us_sectors.csv', index=False)
# SPDR SECTORS
sector_data = pd.read_excel("sectors.xlsx")


# NASDAQ 100 TICKERS
nasdaq_100_symbols = pd.read_excel("nasdaq_100_stocks.xlsx")
df_nasdaq_100 = pd.DataFrame(nasdaq_100_symbols)

# CLEANING NASDAQ DATA
df_nasdaq_100["Sector"] = df_nasdaq_100["Sector"].map(gics_to_spdr)
df_nasdaq_100_cleaned = df_nasdaq_100.dropna(subset=['Sector'])
df_nasdaq_100_cleaned.to_csv("nasdaq100.csv")
nasdaq_tickers = pd.read_csv("nasdaq100.csv")
    
#  Comment out as it runs and slows down each code run. 
# for ticker in nasdaq_tickers["Ticker"]:
#    try:
#       data = yf.download(ticker, "2015-01-01", interval="5d")
#       file_path = os.path.join(output_dir, f"{ticker}.csv")   
#       data.to_csv(file_path)
#    except Exception as e:
#       print(f"Could not download data for {ticker}: {e}")


# Constants
default_start_date = "2022-01-01"
window = 30
volume_window = 12
spx_ticker = "^GSPC"     
ndx_ticker = "^NDX"
# Chart
selected_stock = st.sidebar.selectbox("Stocks", placeholder="Choose a stock", options=nasdaq_tickers["Ticker"])
st.title("Stan Weinstein Stock Analysis")
start_date = st.sidebar.date_input("Start Date", value=datetime.strptime(default_start_date, "%Y-%m-%d"))
ma, rs, volume = st.tabs(["MA", "RS", "Volume"])
# Data
stock_price_data = yf.download(selected_stock, start_date, interval="5d")
ma_data = stock_price_data.rolling(window).mean()
market_price_data = yf.download(spx_ticker, start_date, interval="5d")  
nasdaq_price_data = yf.download(ndx_ticker, start_date, interval="5d")  
selected_stock_volume = stock_price_data["Volume"]
volume_ma = selected_stock_volume.rolling(volume_window).mean() 
df_volume = pd.DataFrame({
    "Volume": selected_stock_volume,
    "Volume Moving Average": volume_ma
})

stock = nasdaq_tickers[nasdaq_tickers["Ticker"] == selected_stock]
stock_sector = stock["Sector"].values[0]
sector_price_data = yf.download(stock_sector, start_date, interval="5d")  
market_relative_trend = calculate_relative_strength(stock_price_data["Close"].values,market_price_data["Close"])
nasdaq_relative_trend = calculate_relative_strength(stock_price_data["Close"].values,nasdaq_price_data["Close"])
sector_relative_trend = calculate_relative_strength(stock_price_data["Close"].values,sector_price_data["Close"])

checkbox = {
    "Moving Average": False,
    "Relative Strength": False,
    "Volume Trend": False,
} 

with ma:
    moving_average_indicator_description = "Price must close above the 30-week SMA and the SMA must be rising"
    df_price_MA = pd.DataFrame({
      "Date":stock_price_data.index,
      "Stock Price": stock_price_data["Close"],
      "Moving Average": ma_data["Close"]
    })
    if df_price_MA["Moving Average"][-1] > sum(df_price_MA["Moving Average"][-3:])/len(df_price_MA["Moving Average"][-3:]):
        checkbox["Moving Average"] = True
        st.markdown("Positive")
        st.markdown(checkbox)
    else:
        st.markdown("No")
         
    # print(df_price_MA["Moving Average"][-1] > sum(df_price_MA["Moving Average"][-3:])/len(df_price_MA["Moving Average"][-3:]))
    figMA = px.line(df_price_MA, x = stock_price_data.index, y=["Stock Price",'Moving Average'], color_discrete_map={
        "Stock Price": "blue", "Moving Average":'orange'} , title=selected_stock)
    st.markdown(moving_average_indicator_description)
    st.plotly_chart(figMA)
    
with rs:
    # TEXT
    relative_strength_indicator_defintion = "The relative strength line tells you how strong a stock is relative to every other stock on the market"
    guide_step1 = "1. The RS Line is rising."
    guide_step2 = "2. The RS line is rising, showing outperformance."
    guide_step3 = "3. The RS line confirms the price breakout, indicating strength relative to the market."
    # DATA
    if(market_relative_trend["RS_MA"][-1] > sum(market_relative_trend["RS_MA"][-3:])/len(market_relative_trend["RS_MA"][-3:])):
        st.markdown("Yes")
        checkbox["Relative Strength"] = True
        st.markdown(checkbox)
    fig_SPX = px.line(stock_price_data, x=stock_price_data.index, y=market_relative_trend["RS_MA"], title=f"{selected_stock} vs SPX")
    fig_NDX = px.line(stock_price_data, x=stock_price_data.index, y=nasdaq_relative_trend["RS_MA"], title=f"{selected_stock} vs NDX")
    fig_sector = px.line(stock_price_data, x = stock_price_data.index, y=sector_relative_trend["RS_MA"], title=f"{selected_stock} vs Sector: {stock_sector}")
    st.markdown(relative_strength_indicator_defintion)
    st.markdown(guide_step1)
    st.markdown(guide_step2)
    st.markdown(guide_step3)
    
    st.plotly_chart(fig_SPX)
    st.plotly_chart(fig_NDX)
    st.plotly_chart(fig_sector)

with volume:
    # print(df_volume["Volume"])
    # print(df_volume["Volume"][-1])
    if df_volume["Volume"][-1] > 2* (sum(df_volume["Volume Moving Average"][-3:])/len(df_volume["Volume Moving Average"][-4:])):
        checkbox["Volume Trend"] = True
        st.markdown("Positive")
    
    fig_volume = px.line(df_volume ,x=selected_stock_volume.index, y=["Volume", "Volume Moving Average"], color_discrete_map={
        "Volume": "gray", "Volume Moving Average": "red"}, title=f"{selected_stock} Volume && MA")
    st.plotly_chart(fig_volume)



@app.route("/data")
def get_data():
    df = pd.DataFrame(stock_price_data["Close"])
    result = [{date.strftime('%Y-%m-%d'): close} for date, close in df['Close'].items()]
    print(result)
    
    return jsonify({"stockData": result})


if __name__ == "__main__":
    app.run(debug=True)
import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
 # Simple Stock Price App
 
 Shown are the stock **closing prices** and **volumes** of Google
 
 """)
 
 #tickersymbol - Ticker symbols are used to identify specific publicly traded companies and the securities they issue.
tickerSymbol = "GOOGL"
 
# Getting data on this tickersymbol - 
 
tickerData = yf.Ticker(tickerSymbol)
 
# getting historic prices for this ticker - 
 
tickerDf = tickerData.history(period="1d", start='2010-05-31', end='2020-05-31')
 
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
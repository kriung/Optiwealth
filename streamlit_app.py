import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px
import streamlit as st
from PIL import Image
from stocknews import StockNews

st.set_page_config(page_title = "Optiwealth Stock Prediction App", layout = 'wide', initial_sidebar_state= 'expanded' )
img = Image.open("Risk Vs Reward.JPG")
st.sidebar.image(img, width= 300)
img2 = Image.open("bears.jpeg")
st.image(img2, width=300)
st.title("Welcome to Optiwealth ")
st.header("Demystifying Stock Markets!")
st.sidebar.title("For stock Advisory")
st.sidebar.header("A product of Team FaPhy")
ticker = st.sidebar.selectbox("Select a Stock ticker ", ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'COST', 'CSCO', 'BTC-USD'])
#ticker = st.sidebar.text_input('Choose Your Stock')
start_date = st.sidebar.date_input('Start Date')
end_date =st.sidebar.date_input('End Date')
data = yf.download(ticker, start = start_date, end =end_date)
fig = px.line(data, x= data.index, y = data['Close'], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs(["pricing_data", "Fundamental_data", "Top 10 News"])
with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2['%change'] = data['Adj Close']/ data['Adj Close'].shift(1) -1
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2['%change'].mean()*252*100
    st.write('Annual Return is:', annual_return, '%')
    stdev = np.std(data2['%change'])* np.sqrt(252)
    st.write('Standard Deviation is:', stdev * 100, '%')
    st.write('Risk Adj. Return is:', annual_return/(stdev*100))
with fundamental_data:
    st.write('Fundamental')
with news:
    st.header(f'news of {ticker}')
    sn= StockNews(ticker, save_news = False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment{title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News sentiment {news_sentiment}')
st.sidebar.selectbox("Indicate your Investment Horizon", ['Short Term', 'Mid Term', 'Long Term'])
st.sidebar.number_input("Specify the Number of Months:")
capital =st.sidebar.slider("Indicate Amount of Capital you wish to Invest", 10000, 100000)
st.sidebar.write("YOUR CAPITAL:", capital)
st.sidebar.button("Click Here to get our BUY/SELL Advice")
st.sidebar.button("CLICK HERE FOR EXPECTED RETURNS")
st.balloons()






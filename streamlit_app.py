import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
import streamlit as st
from stocknews import StockNews

st.set_page_config(page_title = "Optiwealth Stock Prediction App", layout = 'wide', initial_sidebar_state= 'expanded' )

#Loading the dataset
ticker = 'GOOG'
df = yf.download(tickers = ticker)

#Compute 'change_tomorrow' feature
df['change_tomorrow'] = df['Close'].pct_change(-1)
df.change_tomorrow = df.change_tomorrow * -1
df.change_tomorrow = df.change_tomorrow * 100
df['direction'] = np.where(df.change_tomorrow>0, 'UP', 'DOWN')

#Compute Machine Learning Model 'Decision Tree'
# The target feature is the Market Direction
y = df.direction

# The predictor variables will be the OHLCV variables
X = df.drop(columns = ['change_tomorrow', 'Adj Close', 'direction'])

model = DecisionTreeClassifier(max_depth =20, min_samples_split = 5, random_state =42)
model.fit(X, y)
result = model.predict(X)
print(result)

st.title("Welcome to Optiwealth ")
st.header("Where Stock investment Decisions are Made!")
st.sidebar.title("For stock Advisory")
st.sidebar.header("A product of Team FaPhy")
ticker = st.sidebar.text_input('Choose Your Stock')
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

st.sidebar.button("Click Here to Predict BuY Advice")
st.balloons()



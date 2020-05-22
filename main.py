import streamlit as st
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

#TODO:  Your Portfolio - YN
#TODO: https://www.youtube.com/watch?v=cjcUVCtVbuc
def authenticate():
    return

#TODO:  Authenticated - YN
def personalAccount():
    return

def resources():
    return

# Stock Management - SS
def checkStock():
    st.title('Check Stock')
    selected = st.sidebar.text_input("Search Stock by Code", "TSLA",)
    start = st.sidebar.date_input("Start Date",dt.date(2005, 1, 1))
    end = st.sidebar.date_input("End Date",dt.date(2020, 1, 1))
    agree = st.sidebar.checkbox('Use today\'s date')
    end = dt.datetime.now()
    show = st.sidebar.slider('How many days from end date', 0, 100, 10)

    df = web.DataReader(selected, 'yahoo', start, end)
    st.markdown('The data here is for **'+selected+'**.')
    # A calculation to analyze data points by creating a series of averages of
    # different subsets of the full data set.
    df['100ma'] = df['Adj Close'].rolling(window=100).mean()
    # df.dropna(inplace=True)
    oparr = list(df.columns.values)
    options = st.multiselect('What columns to keep in dataset',oparr,[oparr[0], oparr[1]])
    dfx = df[options]
    st.line_chart(dfx)
    st.write(df.tail(show))

#Main - SS
def main():
    style.use('ggplot')
    arr = ['Check Stock','Resources']
    st.sidebar.title('FinTrac')
    st.sidebar.markdown("FinTrac is my personal finance tracker and notebook for refference material")
    option = st.sidebar.selectbox('What are you looking for?',arr)
    st.sidebar.markdown('You selected: **'+option+'**.')
    if(option == 'Check Stock'):
        checkStock()
    else:
        resources()

main()
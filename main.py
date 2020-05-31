import streamlit as st
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from plotly import graph_objs as go
import numpy as np
from firebase import firebase
import json

#TODO:  Your Portfolio - YN
#TODO: https://www.youtube.com/watch?v=cjcUVCtVbuc
def authenticate():
    return

#TODO:  Authenticated - YN

secret = 'bingaroo'


def personalAccount():
    return

    

def resource_sidebar_info():

    option = st.sidebar.selectbox('Add Expense/ Income',('Income','Expense'))
    title = st.sidebar.empty()
    exp_inc_type = st.sidebar.empty()
    date = st.sidebar.empty()
    source_place = st.sidebar.empty()
    amount_of = st.sidebar.empty()
    execute = st.sidebar.empty()
    
    if (option == 'Income'): #adding income form
        title.markdown('New Income')
        income_type = exp_inc_type.selectbox('Type',
        (
            'Employment',
            'Self-Employment',
            'Investment',
            'Pension and Other'
        )
        )
        income_date = date.date_input('Date Recieved')
        source = source_place.text_input('Income Source')
        amount = amount_of.number_input('Amount')
        amount_str = "%.2f" % amount
        add = execute.button('Add Income')
        if (add):

            addIncome([amount_str, income_date, source, income_type])
    else: # adding expense form
        title.markdown('New Expense')
        expense_type = exp_inc_type.selectbox('Type',
            (
                'Rent',
                'Groceries',
                'Restaurants and Outings',
                'Goodies',
                'Phone Plan',
                'Clothing',
                'Other'
            )
        )

        expense_date = date.date_input('Expense Date')
        place = source_place.text_input('Expense Place')
        amount = amount_of.number_input('Amount spent')
        amount_str = "%.2f" % amount
        add = st.sidebar.button('Add Expense')
        if (add):

            addExpense([amount_str, expense_date, place, expense_type])
        
    
    return



def updateTable():

    return

def addExpense(expense_data):

    frbase = firebase.FirebaseApplication("https://fintrac-edb12.firebaseio.com/")
    data = {
        'amount':expense_data[0],
        'date':expense_data[1],
        'expense_income':0,
        'place':expense_data[2],
        'type':expense_data[3]
    }
    
    with st.spinner('Executing...'):
        result = frbase.post('fintrac-edb12/expenses_income',data)
    st.sidebar.success('Expense added')      

    return
    
def addIncome(income_data):
   
    frbase = firebase.FirebaseApplication("https://fintrac-edb12.firebaseio.com/")
    data = {
        'amount':income_data[0],
        'date':income_data[1],
        'expense_income':1,
        'place':income_data[2],
        'type':income_data[3]
    }
        
    with st.spinner('Executing...') :
        result = frbase.post('fintrac-edb12/expenses_income',data) 
    st.sidebar.success('Income added')
    st.sidebar.balloons()   

    return



def sortDataByDate(data):
    new_data = []
    dates = []
    input_data = data

    data_empty = not data
    if data_empty == False:
        #get the dates
        for entry in data:
            dates.append(entry[2])
    
        # sort the dates
        sorted_dates = sorted(dates, reverse = True)

        # make a new list with sorted entries by date
        for date in sorted_dates:
            for entry in input_data:
                if date == entry[2]:
                    new_data.append(entry)
                    input_data.remove(entry)
                    break

  
    return new_data

def summary_account():

    # connect to firebase
    frbase = firebase.FirebaseApplication("https://fintrac-edb12.firebaseio.com/")

    # get the data
    results = frbase.get('fintrac-edb12/expenses_income','')
    empty_dict = not results
    total_available = 0
    if empty_dict == False:
        for key, value in results.items():
            total_available += float(value["amount"])

    bank = 'Bank: $' + str(total_available)

    st.header('Summary of account')
    st.write(bank)
    st.write('Savings: $')
    st.write('Budget: $')
    
    return

def adjustSavingsBudget():
    return

def resources():
    summary_account()
    # connect to firebase
    frbase = firebase.FirebaseApplication("https://fintrac-edb12.firebaseio.com/")

    # get the data
    results = frbase.get('fintrac-edb12/expenses_income','')

    #fetch the data of each entry
    data = []
    for key, value in results.items():
        temp_data = []
       
        temp_data.append(value["type"])
        temp_data.append(value["place"])
        temp_data.append(value["date"])
        if value["expense_income"] == 1:#this is an income
            # add value for income
            temp_data.append(value["amount"])
            # add empty for expense
            temp_data.append(" ")
        else: #this is an expense
            #add nothing for income
            temp_data.append(" ")

            #add value for expense
            temp_data.append(value["amount"])

        #add to overall data
        data.append(temp_data)

        #make temp empty again
        temp_data = []
    
    sorted_data = sortDataByDate(data)
    #st.write(sorted_data)
    st.header('Income and Expenses')
    df = pd.DataFrame(sorted_data, columns = ['Type','Where','Date','Income','Expense'])
    st.table(df)
    resource_sidebar_info()
    st.sidebar.markdown('')    

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
    df['100ma'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()
    # df.dropna(inplace=True)
    oparr = list(df.columns.values)
    options = st.multiselect('What columns to keep in dataset',oparr,[oparr[0], oparr[1]])
    dfx = df[options]
    st.line_chart(dfx)
    st.write(df.tail(show))
    st.subheader("Data Since Day 1")
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])

    st.plotly_chart(fig)


#Main - SS
def main():
    style.use('ggplot')
    arr = ['Resources','Check Stock','Add Expense/Income']
    st.sidebar.title('FinTrac')
    st.sidebar.markdown("FinTrac is my personal finance tracker and notebook for refference material")
    option = st.sidebar.selectbox('What are you looking for?',arr)
    st.sidebar.markdown('You selected: **'+option+'**.')
    if(option == 'Resources'):
        
        resources()
    elif (option == 'Check Stock'):
        checkStock()
    else:
        expenseOrIncome()

main()
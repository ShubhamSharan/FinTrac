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
import seaborn as sns

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

            addIncome([amount_str, income_date, source, income_type, amount])
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

            addExpense([amount_str, expense_date, place, expense_type, amount])
        
    
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

        #update bank and budget
        prev_bank = frbase.get('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','bank')
        prev_budget = frbase.get('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','budget')
        new_bank = prev_bank - expense_data[4]
        new_budget = prev_budget - expense_data[4]
        frbase.put('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','bank',new_bank)
        frbase.put('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','budget',new_budget)
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
        #add income
        result = frbase.post('fintrac-edb12/expenses_income',data) 

        #update bank
        prev_bank = frbase.get('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','bank')
        new_bank = prev_bank + income_data[4]
        st.write(new_bank)
        frbase.put('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','bank',new_bank)
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



def adjustSavingsBudget():
    
    return

def getBankInformation():
    
    # connect to firebase
    frbase = firebase.FirebaseApplication("https://fintrac-edb12.firebaseio.com/")

    # get the data
    bank = frbase.get('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','bank')
    budget = frbase.get('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','budget')
    savings = frbase.get('fintrac-edb12/bank_info/-M8nTKSEMzg5rKW2YX4r','savings')

    data = [bank, budget, savings]
    
    return data

def summary_account():

    data = getBankInformation()
    bank = 'Bank: $' + str(data[0])
    budget = 'Budget: $' + str(data[1])
    savings = 'Savings: $' + str(data[2])

    st.header('Summary of account')
    st.write(bank)
    st.write(savings)
    st.write(budget)
    
    return

def setBankInformation(bank_data):
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

def setSavings():
    # connect to firebase
    frbase = firebase.FirebaseApplication("https://fintrac-edb12.firebaseio.com/")

    # get the data
    curr_employ_saving = frbase.get('fintrac-edb12/bank_info/save_budget_set/employment','')
    curr_invest_saving = frbase.get('fintrac-edb12/bank_info/save_budget_set/investment','')
    curr_pens_saving = frbase.get('fintrac-edb12/bank_info/save_budget_set/pension_other','')
    curr_self_employ_saving = frbase.get('fintrac-edb12/bank_info/save_budget_set/self_employment','')
    #results = frbase.get('fintrac-edb12/bank_info/save_budget_set','')

    st.header('Set savings')
    st.write('The values in each box are your current set savings percentage for each category')
    st.subheader('Employment')
    st.number_input('What percentage of your employment income do you want to save?',curr_employ_saving)

    st.subheader('Investment')
    st.number_input('What percentage of your investment income do you want to save?',curr_invest_saving)

    st.subheader('Pension/Other')
    st.number_input('What percentage of your pension/other income do you want to save?',curr_pens_saving)

    st.subheader('Self Employment')
    st.number_input('What percentage of your self employment income do you want to save?',curr_self_employ_saving )

    save = st.button('Save Changes')

    return

def setBudget():
    st.header('Set Monthly budget')
    monthly_budget = st.number_input('The amount in the box below is your current set monthly budget',400)

    save = st.button('Save Changes')
    st.write('The monthly budget that you specify here will be taken from your primary source of income. By default, this is your employment income. You can change your primary source of income in the "Add income/expense" page on the sidebar')
 
    return

def setSavingsBudget():
    
    st.header('Set Savings and Budget Amount')
    savingsOrBudget = ['Savings','Budget']
    option = st.selectbox('Choose what to set', savingsOrBudget)
    if (option == 'Savings'):
        setSavings()
    else:
        setBudget()
    

    return
  
def expenseOrIncome():
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
    arr = ['Resources','Check Stock','Add Expense/Income','Set Savings and Budget']
    st.sidebar.title('FinTrac')
    st.sidebar.markdown("FinTrac is my personal finance tracker and notebook for refference material")
    option = st.sidebar.selectbox('What are you looking for?',arr)
    st.sidebar.markdown('You selected: **'+option+'**.')
    if(option == 'Resources'):
        
        resources()
    elif (option == 'Check Stock'):
        checkStock()
    elif (option == 'Set Savings and Budget'):
        setSavingsBudget()
    else:
        expenseOrIncome()

main()
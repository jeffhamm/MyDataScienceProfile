
# This program uses pandas profiling with streamlit to help speed up Exploratory Data Analysis (EDA)
# It allows the user to select either csv or a database as the source of data

from ydata_profiling.config import Correlation, Correlations
import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
#from streamlit.caching import cache

import pyodbc
from PIL import Image



#image = Image.open('MYLOGO.jpg')
#st.image(image,caption='MYCAPTION',width=100) # ada a logo

st.title('Exploratory Data Analysis Tool with Streamlit')
st.write('This tool is designed to speed up the EDA process from multiple data sources') 

st.sidebar.markdown("""Exploratory data analysis with ydata_profiling""")
option = st.sidebar.selectbox('select data source', ['csv', 'sql'])

# based on the nature of data, you may want to turn correlation off for pandas profiling

cor = st.sidebar.radio('Include correlations', ['False', 'True']) 

# based on the nature of data, you may want to use the minimal analysis option

mini = st.sidebar.radio('Do minimal Analysis', ['True', 'False']) 

# based on the nature of data, you may want to turn exploration off

explo = st.sidebar.radio('Do exploration', ['False', 'True'])

# you may want to use a sample of the entire data for the exploration

sample_percent = st.sidebar.select_slider('select % of Date as sample', [5, 10, 25, 50, 75, 100])



if option == 'csv':
    uploaded_file = st.sidebar.file_uploader('Upload File')
    

elif  option == 'sql':

    serv = st.text_input('Enter server address')
    db = st.text_input('Enter database')
    schema = st.text_input('Enter Schema')
    table = st.text_input('Enter Table')

           
 
# function to load data

def load_data():

    df = None
    if option == 'csv':
        if uploaded_file is not None :

            try:
                df = pd.read_csv(uploaded_file)
            except:
                st.write('File Not a CSV')
            return df
            
    elif option == 'sql' and schema and table and serv and db:

        try:

            sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                                SERVER=serv; \
                                DATABASE=db; \
                                Trusted_Connection=yes')
        except:
            st.write('Check your database settings')
        
        else:
            query = "SELECT * FROM "+schema+"."+table

            try:       
                df = pd.read_sql(query, sql_conn,coerce_float=True)
            except:
                st.write('no connection')

            return df

fulldf = load_data()


if fulldf is not None:
    y = []
    newdf = fulldf.sample(frac=sample_percent/100)

    # drop columns that are all nulls

    newdf.dropna(axis='columns', how='all', inplace=True)

    st.write(newdf.head())
    
    st.write(newdf.columns)
    
    x = list(newdf.columns)
    
    with st.form(key='form_one'):
        y = st.multiselect('Choose colums for Analysis',x) # chose columns to use for analysis
        submit_button = st.form_submit_button(label='Ok')

    exp_data = newdf.loc[:,y]
    z = list(exp_data.columns)

    with st.form(key = 'form_two'):
        deccols = st.multiselect('Choose columns to treat as Numbers', z) # choose columns that are to be treated as numeric
        submit_button = st.form_submit_button(label = 'Submit')

    
    exp_data[deccols].apply(pd.to_numeric)
    if not  exp_data.empty:
        rp = ProfileReport(exp_data, minimal = mini, Correlations = cor).to_html()

    #st_profile_report(rp)
        #rp.to_file('profile output.html') # run exploration to html output
        components.html(rp, height=1200, width=800, scrolling = True)
        


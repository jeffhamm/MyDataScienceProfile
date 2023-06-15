import dash
import pandas as pd
import numpy as np
from dash import html, Output, Input, dcc, callback
from dash import dash_table as dt
from ydata_profiling import ProfileReport
import plotly.express as px
import dash_bootstrap_components as dbc
import pyodbc

uploaded_file = 'https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv'



app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

my_title = dcc.Markdown(children = '# OPSBENTECH - An App For Speeding Exploratory Data Exploration')
server = dcc.Input(id = 'server', type = 'text', value = 'server', debounce = False)
database = dcc.Input(id = 'database', type = 'text', value = 'database',  debounce = False)
query = dcc.Input(id = 'query', type = 'text', value = 'type query here',  debounce = False, size ='170' )
sample_percent = dcc.Input(id  = 'sample', type = 'number', value = 1,  debounce = False)
selection = dcc.Dropdown(options = ['csv', 'Database'], value = 'csv', id = 'source_type')


preview_table = dt.DataTable(id = 'data1', page_size = 10)

app.layout = dbc.Container(
    [dbc.Row([
        dbc.Col([my_title], width = 12)], justify='Center') 
     , html.Hr(), 
     dbc.Row([
         dbc.Col([server], width = 4), dbc.Col([database], width = 4), dbc.Col([sample_percent], width = 4)]),
         dbc.Row([
             dbc.Col([query], width = 12)
         ]),
      selection, 
     
     preview_table,
     html.Div(
    children = ['Data Exploration Tool',  html.Iframe(
          src="assets/report.html",  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"})]
)
   ]      

          
    )


@app.callback(
    Output(component_id = 'data1', component_property = 'data'),
    Input(component_id = 'source_type', component_property = 'value')

)
def update_table(selection):
    df = load_data(selection)
    return df.to_dict()
    

def load_data(selection):

    df = None
    if selection == 'csv':
        if uploaded_file is not None :
            df = pd.read_csv(uploaded_file)
            
    elif selection == 'sql' and database and server and query:
         sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                            SERVER=server; \
                            DATABASE=database; \
                            Trusted_Connection=yes')
      
         df = pd.read_sql(query, sql_conn,coerce_float=True)
        

    return df

fulldf = load_data(selection)

if fulldf is not None:
    y = []
    newdf = fulldf.sample(frac=sample_percent/100)

    # drop columns that are all nulls

    newdf.dropna(axis='columns', how='all', inplace=True)
  
 
    
    profile = ProfileReport(fulldf, title="Pandas Profiling Report")
    profile.to_file("assets/report.html")



if __name__ == "__main__":
    app.run_server(debug=True)
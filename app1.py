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
server = dcc.Input(id = 'server', type = 'text', value = 'server')
database = dcc.Input(id = 'database', type = 'text', value = 'database')
query = dcc.Input(id = 'query', type = 'text', value = 'type query here', size ='170' )
sample_percent = dcc.Input(id  = 'sample', type = 'number', value = 50)
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
    Input(component_id = 'source_type', component_property = 'value'),
    Input(component_id = 'sample', component_property = 'value')

)
def update_table(selected, samples):
    df = load_data(selected, samples)
    return df.to_dict()
    

def load_data(selected, samples):

    fulldf = None
    if selected == 'csv':
        if uploaded_file is not None :
            fulldf = pd.read_csv(uploaded_file)
            
    elif selected == 'sql' and database and server and query:
         sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                            SERVER=server; \
                            DATABASE=database; \
                            Trusted_Connection=yes')
      
         fulldf = pd.read_sql(query, sql_conn,coerce_float=True)

    if fulldf is not None:   
        newdf = fulldf.sample(frac=samples/100)

        # drop columns that are all nulls

        newdf = newdf.dropna(axis='columns', how='all', inplace=True)
    
    
        
        profile = ProfileReport(newdf, title="Pandas Profiling Report")
        profile.to_file("assets/report.html")

    return newdf
    




if __name__ == "__main__":
    app.run_server(debug=True)
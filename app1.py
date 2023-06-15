import dash
import pandas as pd
import numpy as np
from dash import html, Output, Input, dcc, callback
from dash import dash_table as dt
from ydata_profiling import ProfileReport
import plotly.express as px
import pyodbc

uploaded_file = 'https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv'



app = dash.Dash(__name__)

server = dcc.Input(id = 'server', type = 'text')
database = dcc.Input(id = 'database', type = 'text')
query = dcc.Input(id = 'query', type = 'text')
sample_percent = dcc.Input(id  = 'sample', type = 'float')
selection = dcc.Dropdown(options = ['csv', 'Database'], value = 'csv', id = 'source_type'),

app.layout = html.Div(
 
    
    children = ['Data Exploration Tool',
                html.Hr(),
                selection,
                server,
                database,
                query,
                
                dt.DataTable(id = 'data1', page_size = 10),

            html.Iframe(
          src="assets/report.html",  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"}
    )]
)

@app.callback(
    Output(component_id = 'data1', component_property = 'data'),
    Input(component_id = 'source_type', component_property = 'value')

)
def update_table(selection):
    df = load_data()
    return df.to_dict('records')
    

def load_data():

    df = None
    if selection == 'csv':
        if uploaded_file is not None :
            df = pd.read_csv(uploaded_file)
            
    elif selection == 'sql' and database and server and query:
         sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                            SERVER=10.1.1.5; \
                            DATABASE=obt; \
                            Trusted_Connection=yes')
      
         df = pd.read_sql(query, sql_conn,coerce_float=True)
        

    return df

fulldf = load_data()

if fulldf is not None:
    y = []
    newdf = fulldf.sample(frac=sample_percent/100)

    # drop columns that are all nulls

    newdf.dropna(axis='columns', how='all', inplace=True)

    
    
 
    
profile = ProfileReport(fulldf, title="Pandas Profiling Report")
profile.to_file("assets/report.html")



if __name__ == "__main__":
    app.run_server(debug=True)
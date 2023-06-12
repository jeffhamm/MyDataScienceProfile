import dash
import pandas as pd
import numpy as np
from dash import html, Output, Input, dcc, callback, dash_table
from ydata_profiling import ProfileReport
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
profile = ProfileReport(df, title="Pandas Profiling Report")
profile.to_file("assets/report.html")



app = dash.Dash(__name__)

app.layout = html.Div(
 
    
    children = ['Data Exploration Tool',
                html.Hr(),
                dcc.RadioItems(options = ['csv', 'Database'], value = 'csv', id = 'control-radio'),
                dash_table.DataTable(data = df.to_dict('record'), page_size = 10),
            html.Iframe(
          src="assets/report.html",  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"},
    )]
)

@callable(
    Output(component_id = )
    Input(component_id = 'control-radio', component_property = 'value')
)
def load_data():

    df = None
    if option == 'csv':
        if uploaded_file is not None :
            df = pd.read_csv(uploaded_file)
            
    elif option == 'sql' and schema and table:
               
        df = pd.read_sql(query, sql_conn,coerce_float=True)
    return df



if __name__ == "__main__":
    app.run_server(debug=True)
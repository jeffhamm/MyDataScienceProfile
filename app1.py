import dash
import pandas as pd
import numpy as np
from dash import html, Output, Input, dcc, callback, State
from dash import dash_table as dt 
from ydata_profiling import ProfileReport
import plotly.express as px
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy import sql

uploaded_file = 'employees.csv'
#df = pd.read_csv(uploaded_file)
df = pd.DataFrame()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

my_title = dcc.Markdown(
    children='# OPSBENTECH - An App For Speeding Exploratory Data Exploration')

#query1 = sql.text("select * from compdata.prosecutions_performance")

query = dcc.Input(id='query', type='text', value='type query here', size='170')
sample_percent = dcc.Input(id='sample', type='number', value=50)
selection = dcc.Dropdown(id='source_type',
    options=['csv', 'Database'])


app.layout = dbc.Container(
    [dbc.Row([
        dbc.Col([my_title], width=12)], justify='Center'), html.Hr(),
     dbc.Row([
          dbc.Col([sample_percent], width=4)]),
     dbc.Row([
             dbc.Col([query], width=12)
             ]),
     selection,
     html.Div([dbc.Button('Submit',id = 'submit', color = 'primary', className = 'me-1', n_clicks = 0, outline = True)]),
    
     #html.Table(id = 'data1' , children = 'value'),
     html.Div([
         dt.DataTable(id = 'dt1')
     ]),
     html.Div(
        children=['Data Exploration Tool',  html.Iframe(
            src="assets/report.html",  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"})]
    )
    ]
)


@app.callback(
    Output(component_id='dt1', component_property='data'),
    Input(component_id='submit', component_property='n_clicks'),
    Input(component_id = 'source_type', component_property = 'value'),
    Input(component_id = 'sample', component_property = 'value'),
    Input(component_id = 'query', component_property = 'value')
   
)
def on_button_click(n, selected, samples, query):
    if n:
        df = load_data(selected, samples, query)
        
        #ample_table = dbc.Table.from_dataframe(df, size='md', striped = True)
        return html.Div([dt.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_header={'backgroundColor': "#FFD700",
                              'fontWeight': 'bold',
                              'textAlign': 'center',},
                style_table={'overflowX': 'scroll'},  
                style_cell={'minWidth': '180px', 'width': '180px',
                        'maxWidth': '180px','whiteSpace': 'normal'},                        
                         filtering=True,
                 row_selectable="multi",
                 n_fixed_rows=1),
               html.Hr()
        ])


def load_data(selected, samples,query):

    fulldf = None
    if selected == 'csv':
        if uploaded_file is not None:
            fulldf = pd.read_csv(uploaded_file)
            newdf = fulldf.sample(frac=samples/100)

            # drop columns that are all nulls

            #newdf = newdf.dropna(axis='columns', how='all', inplace=True)

            profile = ProfileReport(newdf, title="Pandas Profiling Report")
            profile.to_file("assets/report.html")

    elif selected == 'Database':
        DB_SERVER = '10.1.1.5'
        DB_NAME = 'OBT'

        # Construct the connection string
        db_url = f'mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

        # Create the SQLAlchemy engine
        engine = create_engine(db_url)

        try:
            with engine.connect() as  connection:
                fulldf = pd.read_sql(sql.text(query), connection, coerce_float=True)
        except Exception as e:
            print('Error execution the query:', str(e))
         

        newdf = fulldf.sample(frac=samples/100)

        # drop columns that are all nulls

        #newdf = newdf.dropna(axis='columns', how='all', inplace=True)

        profile = ProfileReport(newdf, title="Pandas Profiling Report")
        profile.to_file("assets/report.html")

        return newdf


if __name__ == "__main__":
    app.run_server(debug=True)

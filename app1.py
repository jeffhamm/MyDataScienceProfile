import dash
import pandas as pd
import numpy as np
from dash import html
from ydata_profiling import ProfileReport

df = pd.DataFrame(np.random.rand(100, 5), columns=["a", "b", "c", "d", "e"])
profile = ProfileReport(df, title="Pandas Profiling Report")
profile.to_file("assets/report.html")

app = dash.Dash(__name__)

app.layout = html.Div(
    children = [html.Iframe(
          src="assets/report.html",  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"},
    )]
)

if __name__ == "__main__":
    app.run_server(debug=True)
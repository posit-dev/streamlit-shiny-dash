import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(children=[
     dcc.Input(id='sample',
               type='number', 
               min=0, 
               max=1, 
               value=0.1, 
               step=0.01),
     html.Div("Plot scale"),
     dcc.RadioItems(["Linear", "Log"], id='scale')
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE,
                   children=[
                       html.Div(id='max-value', style={"padding-top": "50px"}),
                       dcc.Graph(id='scatter-plot'),
                       dcc.Graph(id='histogram'),

                       # In order to get the sampling to work we need to stick the data in browser cache
                       dcc.Store(id='sampled-dataset')
                   ])

app.layout = html.Div(
    [dcc.Location(id="url"), sidebar, content])


@app.callback(Output('sampled-dataset', 'data'),
              Input('sample', 'value'))
def cache_dataset(sample):
    df = pd.read_csv("nyc-taxi.csv")
    df = df.sample(frac=sample)

    # To cache data in this way we need to seiralize it to json which can be expensive 
    # and doesn't work for all object types.
    json = df.to_json(date_format='iso', orient='split')
    return json


@app.callback(Output('max-value', 'children'),
              Input('sampled-dataset', 'data'))
def update_max_value(sampled_df):
    df = pd.read_json(sampled_df, orient='split')
    return f'First taxi id: {df["taxi_id"].iloc[0]}'


@app.callback(Output('scatter-plot', 'figure'),
              Input('sampled-dataset', 'data'),
              Input('scale', 'value'))
def update_scatter(sampled_df, scale):
    df = pd.read_json(sampled_df, orient='split')
    scale = scale == 'Log'
    fig = px.scatter(df,
                     x='total_amount',
                     y='tip_amount',
                     log_x=scale,
                     log_y=scale)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(Output('histogram', 'figure'),
              Input('sampled-dataset', 'data'))
def update_histogram(sampled_df):
    df = pd.read_json(sampled_df, orient='split')
    fig = px.histogram(df, x='total_amount')
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

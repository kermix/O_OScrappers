import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

from pages import paa, page2, main

app = Dash(
    __name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        ]
    )

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Container(id='page-content', fluid=True)
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/paa':
        return paa.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return main.layout


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8049)

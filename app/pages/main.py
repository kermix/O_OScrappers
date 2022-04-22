from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3('Choose the app'),
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("People also Ask", active=True, href="/paa")),
        dbc.NavItem(dbc.NavLink("A link", href="#")),
        dbc.NavItem(dbc.NavLink("Another link", href="#")),
    ]
)
])
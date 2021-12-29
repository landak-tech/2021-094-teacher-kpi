from dash import dcc,html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask_login import current_user

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pages import error, dashboard, nilai, kelola
from server import app
from src.utils import nav, CONTENT_STYLE

layout = dbc.Container([
    nav,
    html.Div(id='content')
], style=CONTENT_STYLE, fluid=True)

@app.callback(
    Output('content','children'),
    [
        Input('url','pathname'),
    ]
)
def pages(pathname):
    if pathname == '/main' or pathname == '/' or pathname == '/home':
        return dashboard.layout()
    elif pathname == '/nilai':
        if current_user.username == "kepsek":
            return nilai.layout()
        else:
            return error.layout()
    elif pathname == '/kelola':
        return kelola.layout()
    else:
        return error.layout()

@app.callback(
    [
        Output('nilai-btn','disabled'),
        Output('nilai-btn','style'),
    ],
    Input('url','pathname')
)
def button(url):
    if current_user.username == "kepsek":
        return False, {}
    else:
        return True, {'backgroundColor':'gray', 'color':'lightgray'}
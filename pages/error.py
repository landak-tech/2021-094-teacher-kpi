from dash import dcc, html
import dash_bootstrap_components as dbc

def layout():
    return html.Div(
        dbc.Row(html.H3(html.B("Anda tidak punya akses ke halaman ini")), justify="center", style={"padding":20})
    )
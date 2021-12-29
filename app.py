import warnings
warnings.filterwarnings("ignore")

from flask_login import logout_user, current_user

from dash import dcc,html
from dash.dependencies import Input, Output

from pages import main, login, error, kelola,nilai
from server import app, server
from src.config import DEV

content = html.Div(id='pageContent')

app.layout = html.Div([
    dcc.Location(id='url'),
    content
])

@app.callback(
    Output('pageContent', 'children'),
    [
        Input('url', 'pathname'),
    ]
)
def displayPage(pathname):
    if DEV:
        return nilai.layout()
    else:
        if pathname == '/main':
            if current_user.is_authenticated:
                return main.layout
            else:
                return login.layout
        elif pathname == '/logout':
            if current_user.is_authenticated:
                logout_user()
                return login.layout
            else:
                return login.layout
        else:
            if current_user.is_authenticated:
                return main.layout
            else:
                return login.layout

if __name__ == '__main__':
    app.run_server(debug=True)
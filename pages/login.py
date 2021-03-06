from dash import dcc,html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from server import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout = dbc.Container([
    html.Br(),
    dbc.Row(
        dbc.Container([
            dcc.Location(id='urlLogin', refresh=True),
            dbc.Card(
                dbc.CardBody(
                    dbc.Col([
                        dbc.Row([
                            dbc.Label("Email", className="mr-2"),
                            dbc.Input(type="text", id='usernameBox', placeholder="Enter your username", n_submit=0, className='form-control'),
                        ], className="mr-3", style={'margin':10}),
                        dbc.Row([
                            dbc.Label("Password", className="mr-2"),
                            dbc.Input(type="password", id='passwordBox', placeholder="Enter your password", n_submit=0, className='form-control'),
                        ], className="mr-3", style={'margin':10}),
                        dbc.Button(html.B("Login", style={'padding-left': 20, 'padding-right': 20, 'font-size': 'large'}), id='loginButton', color="primary", n_clicks=0, className='mr-2')
                    ], className='form-group', style={'padding':40})
                )
            )
        ], className='jumbotron'),
        justify='center', align='center',style={'height':'80vh'}
    )
])

################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - REDIRECT TO PAGE1 IF LOGIN DETAILS ARE CORRECT
################################################################################
@app.callback(Output('urlLogin', 'pathname'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def sucess(n_clicks, usernameSubmit, passwordSubmit, username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return '/home'
        else:
            pass
    else:
        pass


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT
################################################################################
@app.callback(Output('usernameBox', 'className'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT
################################################################################
@app.callback(Output('passwordBox', 'className'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'

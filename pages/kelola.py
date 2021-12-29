from dash import dcc,html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask_login import current_user
import pandas as pd

from src.config import engine
from server import app

def layout():
    nama = pd.read_sql_query("select nama from profil where bidang_yang_diampu != 'Kepala Sekolah' and bidang_yang_diampu is not Null", con=engine)['nama'].unique()
    nama_opt = [{'label':f'{n}', 'value':n} for n in nama]
    field = pd.read_sql_query("PRAGMA table_info(profil)", con=engine)
    fn = ['UID', 'NIP', 'Karpeg','NUPTK','NRG','Nama','Tempat & Tgl. Lahir','Golongan','TMT','Mulai Bekerja di Sekolah','Pendidikan','Jenis Kelamin','Mata Pelajaran','Bidang yang Diampu']
    return dbc.Container([
        dbc.Row([
            dbc.Col(
               dcc.Dropdown(
                    id='nama-opt-kel',
                    options=nama_opt,
                    style={
                        # 'width': '135px',
                        'color': '#212121',
                        'background-color': '#FFFFFF',
                    },
                ), md=6, style={'padding':20}
            ),
            dbc.Col(
                dbc.Checklist(
                    options=[
                        {"label": "Edit", "value": True},
                    ],
                    value=False,
                    id="switches-edit",
                    switch=True,
                    style={'text-align':'center'},
                ), align='center', md=3, style={'padding':20}
            ),
            dbc.Col(
                dbc.Button("Perbaharui", id="update-btn"),
                align='center', md=3, style={'padding':20}
            )
        ], align='center',justify='center'),
        dbc.Container([
            dbc.InputGroup([
                dbc.InputGroupText(f"{m}", style={'width':'20vh'}),
                dbc.Input(id=f"{n}-field")
            ],className="mb-3") for m,n in zip(fn,field.name.values)], fluid=True
        ),
        dbc.Row([
            dbc.Col(
                dbc.Button("Hapus",id="hapus-btn"),
                align='center', md=6, style={'padding':20}
            ),
            dbc.Col(
                dbc.Button("Tambahkan",id="tambah-btn"),
                align='center', md=6, style={'padding':20}
            )
        ], align='center',justify='center', style={'text-align':'center'})
    ], fluid=True)

@app.callback(
    [Output(f'{n}-field','placeholder') for n in pd.read_sql_query("PRAGMA table_info(profil)", con=engine).name.values],
    Input('nama-opt-kel','value')
)
def kelola(nama):
    if nama != None:
        return pd.read_sql_query(f"select * from profil where nama='{nama}'", con=engine).values.tolist()[0]
    else:
        return ['.....' for n in range(len(pd.read_sql_query("PRAGMA table_info(profil)", con=engine).name.values))]

@app.callback(
    Output('switches-edit','options'),
    Input('url','pathname')
)
def disable_edit(url):
    if current_user.username == "kepsek":
        return [{"label": "Edit", "value": True, "disabled":True}]
    else:
        return [{"label": "Edit", "value": True, "disabled":False}]

@app.callback(
    [Output(f'{n}-field','disabled') for n in pd.read_sql_query("PRAGMA table_info(profil)", con=engine).name.values],
    Input('switches-edit','value')
)
def disable_edit(val):
    if val:
        return [True] + [False for n in range(len(pd.read_sql_query("PRAGMA table_info(profil)", con=engine).name.values)-1)]
    else:
        return [True for n in range(len(pd.read_sql_query("PRAGMA table_info(profil)", con=engine).name.values))]

@app.callback(
    [
        Output("hapus-btn",'disabled'),
        Output("tambah-btn",'disabled'),
        Output("update-btn",'disabled')
    ],
    [
        Input('nama-opt-kel','value'),
        Input('switches-edit','value')
    ]
)
def button_below(val,sw):
    if val == None and sw:
        return True, False, True
    elif (val == None and not sw) or current_user.username == 'kepsek':
        return True, True, True
    elif val != None and sw:
        return True, True, False
    else:
        return False, True, True

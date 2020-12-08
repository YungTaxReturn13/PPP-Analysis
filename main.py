import numpy as np
import pandas as pd
import zipfile
import os
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table



pd.set_option('display.float_format', lambda x: '%.3f' % x)

# arr = os.listdir(r"C:\Users\justi\Python Projects\PPP\PPP-Analysis\PPP Data\All Data 1201")
# dff = pd.DataFrame()
# for i in arr:
#     zf = zipfile.ZipFile(f'C://Users//justi//Python Projects//PPP//PPP-Analysis//PPP Data//All Data 1201//{i}')
#     file_list = zf.namelist()
#     file_list = [k for k in file_list if '.csv' in k]
#     file_list = [k for k in file_list if '_MACOSX' not in k]
#     for j in file_list:
#         df = pd.read_csv(zf.open(f'{j}'))
#         dff = dff.append(df)

#using the sample dataset
dff = pd.read_csv('sample.csv')

zips = dff['Zip'].dropna().unique()

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Data visualization of PPP Loans based on ZIP code'),
    html.Div(children="Please enter a valid Zip Code"),
    dcc.Input(id='input', value='', type='text'),
    html.Div(
        id='output'
    )
])

@app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(input_data):
    try:
        if int(input_data) in zips:
            return 'it is working'
    except:
        return "Not a Valid zip code"

if __name__=="__main__":
    app.run_server()



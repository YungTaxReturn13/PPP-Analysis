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
import base64

zipcode = 22152

naics = pd.read_csv(r'C:\Users\justi\Python Projects\PPP\PPP-Analysis\PPP Data\6-digit_2017_Codes.csv',encoding='latin1')
naics = naics.drop('Unnamed: 2',axis=1)
naics = naics[1:]
naics.columns = ['NAICSCode', '2017 NAICS Title']



image = r'C:\Users\justi\Python Projects\PPP\PPP-Analysis\crying-cat-meme-lede.jpg'
encode_image = base64.b64encode(open(image, 'rb').read()).decode('ascii')

pd.set_option('display.float_format', lambda x: '%.3f' % x)

arr = os.listdir(r"C:\Users\justi\Python Projects\PPP\PPP-Analysis\PPP Data\All Data 1201")
dff = pd.DataFrame()
for i in arr:
    zf = zipfile.ZipFile(f'C://Users//justi//Python Projects//PPP//PPP-Analysis//PPP Data//All Data 1201//{i}')
    file_list = zf.namelist()
    file_list = [k for k in file_list if '.csv' in k]
    file_list = [k for k in file_list if '_MACOSX' not in k]
    for j in file_list:
        df = pd.read_csv(zf.open(f'{j}'))
        dff = dff.append(df)

dff = dff[dff['Zip'] == zipcode]

dff = dff.merge(naics, on = 'NAICSCode')

# #using the sample dataset
# dff = pd.read_csv('sample.csv')

zips = dff['Zip'].dropna().unique()

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Data visualization of PPP Loans based on ZIP code'),
    html.Div(children="Please enter how many loans you would like to see"),
    dcc.Input(id='input', value='10', type='text'),
    html.Div(id='total_number'),
    html.Div(id='total_amount'),
    html.H3(id="top"),
    dash_table.DataTable(
        id='datatable',
        columns = [
            {'name': i, 'id': i} for i in dff.columns],
        data=dff.to_dict('records')
    ),

    html.Img(src='data:image/png;base64,{}'.format(encode_image),height=100,width=50)
])

@app.callback(
    [Output(component_id='total_number', component_property='children'),
     Output(component_id='total_amount', component_property='children'),
    Output(component_id='top', component_property='children'),
     Output(component_id='datatable', component_property='data')],
    [Input(component_id='input', component_property='value')])
def update_values(input_data):
    return (f"Total Number of Businesses within {zipcode}: {str(len(dff[dff['Zip']==int(zipcode)]))}", #Returns the total amount of businesses that recieved help in the zip
            f"Total amount of money lent within {zipcode}: {round(dff[dff['Zip'] == int(zipcode)]['LoanAmount'].sum(),2):,}",
            f"Top {input_data} Businesses that recieved PPP Loans by the amount recieved:",
            dff[dff['Zip']==int(zipcode)][:min(len(dff),int(input_data))].sort_values('LoanAmount',ascending=False).to_dict('records'))




if __name__=="__main__":
    app.run_server()



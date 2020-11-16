import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from urllib.request import urlopen
from collections import Counter
import json
import geopandas as gpd

url = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search?resource_id=b64ba3c4-9e41-41b8-b3fd-2da21d627558&limit=10000'  
datos = urlopen(url).read()
data = json.loads(datos)
resultados = data['result']

resultsBta_df = pd.DataFrame.from_records(resultados['records'])
bta_df = resultsBta_df

localidades=[] 
x=bta_df['LOCALIDAD_ASIS']  
c=Counter(x)

local = pd.DataFrame() #Se crea una nueva referencia del DataFrame
local['Localidades']=c.keys() #Se extraen los elementos únicos
local['No. Casos']=c.values()

gpf = gpd.read_file('poligonos-localidades.geojson')

gdf = gpf.sort_values(by='Nombre de la localidad') #Se ordenan según la localidad
gdf = gdf.reset_index(drop=True)

localidades=[] 
x=bta_df['LOCALIDAD_ASIS']  
c=Counter(x) #Se cuentan los datos según las localidades
local1 = pd.DataFrame() #Se crea una nueva referencia del DataFrame
local1['Localidades']=c.keys() #Se extraen los elementos únicos
local1['No. Casos']=c.values() #Se extrae la frecuencia de cada elemento único
local1 = local1.replace({'La Candelaria':'Candelaria'})
local1 = local1.replace({'Fuera de Bogotá':'Sumapaz'})
local1 = local1.sort_values(by='Localidades')
local1 = local1.reset_index(drop=True)
local1 = local1.drop([14], axis=0)
local1 = local1.reset_index(drop=True)
gdf['No. Casos'] = local1['No. Casos']

bins = [0, 9, 19, 29, 39, 49, 59,69,79,89] #Se establecen los intervalos 
names = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89"] #Se establecen los nombres de los intervalores
bta_df["EDAD"] = bta_df["EDAD"].astype(float)
bta_df["EDAD"] = pd.cut(bta_df["EDAD"],bins,labels=names)
genero_ob=bta_df.groupby(['EDAD','SEXO']).size()
genero_ob=genero_ob.reset_index()

app = dash.Dash()

fig = px.bar(local, x='Localidades', y='No. Casos')
fig2 = px.bar(genero_ob, x='EDAD', y=0, color='SEXO', title='Género y edad')

app.title = 'Dash covid'

app.layout = html.Div([
    html.Div(
        className='app-header',
        children=[
            html.Div('Data covid', className="app-header--title")
        ]
    ),
    
    html.Div(children='''
        A web application for show the information of Covid in Colombia
        '''),

    dcc.Graph(
        id='localidades_graph',
        figure=fig
    ),

    dcc.Graph(
        id='edad_sexo_graph',
        figure=fig2
    )
]
)

if __name__ == '__main__':
    app.run_server(debug=True)
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
from sodapy import Socrata
from datetime import datetime
import base64

# Colombia -------------------------------------------------------

client = Socrata("www.datos.gov.co", None) #Se determina la dirección de la cual se extraeran los datos
results = client.get("gt2j-8ykr", limit=5000) #Se obtienen los datos y se establece un límite

# Convertir a dataframe de pandas
results_df = pd.DataFrame.from_records(results)
df=results_df
df = df.replace({'LEVE':'Leve'})
df = df.replace({'leve':'Leve'})
df = df.replace({'moderado':'Moderado'})
df = df.replace({'En Estudio':'En estudio'})
df = df.replace({'EN ESTUDIO':'En estudio'})
df = df.replace({'relacionado':'Relacionado'})
df = df.replace({'RELACIONADO':'Relacionado'})

df.columns

df=results_df

df=df.fillna('No Definido') #Se llenan los datos vacíos
tupla = (("T00:00:00.000", ""),("-", "/"))
for c in df.index:
    for a, b in tupla:
        df['fecha_de_notificaci_n'][c] = df['fecha_de_notificaci_n'][c].replace(a, b)
        df['fecha_inicio_sintomas'][c] = df['fecha_inicio_sintomas'][c].replace(a, b)
        df['fecha_diagnostico'][c] = df['fecha_diagnostico'][c].replace(a, b)
        df['fecha_recuperado'][c] = df['fecha_recuperado'][c].replace(a, b)
        df['fecha_reporte_web'][c] = df['fecha_reporte_web'][c].replace(a, b)
        df['fecha_muerte'][c] = df['fecha_muerte'][c].replace(a, b)
df.head()
for c in df.index:
    if(df['fecha_de_notificaci_n'][c]!='No Definido'):
        df['fecha_de_notificaci_n'][c]=datetime.strptime(df['fecha_de_notificaci_n'][c], '%d/%m/%Y %H:%M:%S')
    if(df['fecha_inicio_sintomas'][c]!='No Definido'):
        df['fecha_inicio_sintomas'][c]=datetime.strptime(df['fecha_inicio_sintomas'][c], '%d/%m/%Y %H:%M:%S')
    if(df['fecha_recuperado'][c]!='No Definido'):
        df['fecha_recuperado'][c]=datetime.strptime(df['fecha_recuperado'][c], '%d/%m/%Y %H:%M:%S')
    if(df['fecha_reporte_web'][c]!='No Definido'):
        df['fecha_reporte_web'][c]=datetime.strptime(df['fecha_reporte_web'][c], '%d/%m/%Y %H:%M:%S')
    if(df['fecha_muerte'][c]!='No Definido'):
        df['fecha_muerte'][c]=datetime.strptime(df['fecha_muerte'][c], '%d/%m/%Y %H:%M:%S')
 #Se llena con la fecha de notificación 
c=list()
for a in df.index:
  l=df['fecha_de_notificaci_n'].iloc[a]
  c.append(l.month)
  #c.append(l.strftime('%B')) -- Te da el nombre del mes
df['Mes_Notificacion']=c

d=Counter(c) #Se cuentan los datos según la fecha de notificación
df1 = pd.DataFrame() #Se crea una nueva referencia del DataFrame
df1['Mes']=d.keys() #Se extraen los elementos únicos
df1['No. Casos']=d.values() #Se extrae la frecuencia de cada elemento único

df1=df1.sort_values(by='Mes') #Se ordenan según la fecha 
df1.columns

#-------------------------------------------------------

fecha=[]
fecha=df['fecha_de_notificaci_n']
d=Counter(fecha)
df_fechas = pd.DataFrame()
df_fechas['Fecha']=d.keys()
df_fechas['No. Casos']=d.values()
df_fechas=df_fechas.sort_values(by='Fecha',ascending=False) #Se ordenan según la fecha

#--------------------------------------------------

y=[]
y=df['ciudad_municipio_nom'] #Se llena con la ciudad
d=Counter(y) #Se cuentan los datos según la ciudad

df2 = pd.DataFrame()
df2['Ciudad']=d.keys() #Se extraen los elementos únicos
df2['No. Casos']=d.values() #Se extrae la frecuencia de cada elemento único
df2=df2.sort_values(by='No. Casos',ascending=False) #Se ordena según el número de casos 

#-------------------------------------------------------
tipo=[]
tipo=df['fuente_tipo_contagio']
#Se cuentan los casos según el tipo de contagio
e=Counter(tipo)
df3 = pd.DataFrame()
#Se establecen los elementos y la frecuencia de cada uno
df3['Tipo']=e.keys()
df3['No. Casos']=e.values()
#Se ordenan
df3=df3.sort_values(by='No. Casos',ascending=False)

#-------------------------------------------------------
estado=[]
estado=df['estado']
#Se cuentan los casos según el estado de los pacientes 
f=Counter(estado)
df4 = pd.DataFrame()
#Se establecen los elementos y la frecuencia de cada uno
df4['Estado']=f.keys()
df4['No. Casos']=f.values()
df4=df4.sort_values(by='No. Casos',ascending=False)
#------------------------------------------------------
muertes=[]
muertes=df['fecha_muerte']
#Se cuentan los casos según la fecha de muerte
g=Counter(muertes)
df5 = pd.DataFrame()
#Se establecen los elementos y la frecuencia de cada uno
df5['Muertes']=g.keys()
df5['No. Casos']=g.values()
df5=df5.sort_values(by='No. Casos',ascending=False)
#Se hace una copia del data frame 
copiamuertes=df5.iloc[1::].copy()
#--------------------------------------------------------
pais=[]
pais=df['pais_viajo_1_nom']
#Se cuentan los casos según el país de procedencia 
h=Counter(pais)
df6 = pd.DataFrame()
#Se establecen los elementos y la frecuencia de cada uno
df6['Pais de Procedencia']=h.keys()
df6['No. Casos']=h.values()
df6=df6.sort_values(by='No. Casos',ascending=False)
#Se hace una copia del data frame 
df6copy = df6.iloc[1:8].copy()
#Se organizan según el número de casos 
df6copy=df6copy.sort_values(by='No. Casos')

#------------------------------------------------------

#Se organiza según el número de muertes 
copiamuertes=copiamuertes.sort_values(by='Muertes')
x = copiamuertes['Muertes'] #Se extraen los elementos únicos
y = copiamuertes['No. Casos'] #Se extrae la frecuencia de cada elemento único 
df5.columns

#------------------------------------------------------

figC = px.line(df1, x='Mes', y='No. Casos',title='Número de Casos')
figC2 = px.bar(df2, x='Ciudad', y='No. Casos',title='Ciudades con mayor número de Contagiados')
figC3 = px.pie(df3, values='No. Casos' , names='Tipo',title='Casos Totales por tipo de contagio')
figC4 = px.pie(df4, values='No. Casos' , names='Estado',title='Estado de los pacientes')
figC6 = px.bar(df6,  x='Pais de Procedencia', y='No. Casos',title='País de Procedencia')
figC7 = px.line(df5,  x=x, y=y,title='Fallecimientos')
figC8 = px.line(df_fechas, x='Fecha', y='No. Casos', title='Evolución de casos')

# Bogotá ------------------------------------------------------- 

url = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search?resource_id=b64ba3c4-9e41-41b8-b3fd-2da21d627558&limit=10000'  
datos = urlopen(url).read()
data = json.loads(datos)
resultados = data['result']

resultsBta_df = pd.DataFrame.from_records(resultados['records'])
bta_df = resultsBta_df

bta_df=bta_df.fillna('No Definido') #Se llenan los datos vacíos
tupla = (("T00:00:00.000", ""),("-", "/"))
for c in bta_df.index:
    for a, b in tupla:
        bta_df['FECHA_DIAGNOSTICO'][c] = bta_df['FECHA_DIAGNOSTICO'][c].replace(a, b)
        bta_df['FECHA_INICIO_SINTOMAS'][c] = bta_df['FECHA_INICIO_SINTOMAS'][c].replace(a, b)

for c in bta_df.index:
    if(bta_df['FECHA_DIAGNOSTICO'][c]!='No Definido'):
        bta_df['FECHA_DIAGNOSTICO'][c]=datetime.strptime(bta_df['FECHA_DIAGNOSTICO'][c], '%d/%m/%Y')
    if(bta_df['FECHA_INICIO_SINTOMAS'][c]!='No Definido'):
        bta_df['FECHA_INICIO_SINTOMAS'][c]=datetime.strptime(bta_df['FECHA_INICIO_SINTOMAS'][c], '%d/%m/%Y')

#-------------------------------------------------------

localidades=[] 
x=bta_df['LOCALIDAD_ASIS']  
c=Counter(x)

local = pd.DataFrame() #Se crea una nueva referencia del DataFrame
local['Localidades']=c.keys() #Se extraen los elementos únicos
local['No. Casos']=c.values()

#-------------------------------------------------------

gpf = gpd.read_file('poligonos-localidades.geojson')

gdf = gpf.sort_values(by='Nombre de la localidad') #Se ordenan según la localidad
gdf = gdf.reset_index(drop=True)

#-------------------------------------------------------

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

#-------------------------------------------------------

bins = [0, 9, 19, 29, 39, 49, 59,69,79,89] #Se establecen los intervalos 
names = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89"] #Se establecen los nombres de los intervalores
bta_df["EDAD"] = bta_df["EDAD"].astype(float)
bta_df["EDAD"] = pd.cut(bta_df["EDAD"],bins,labels=names)
genero_ob=bta_df.groupby(['EDAD','SEXO']).size()
genero_ob=genero_ob.reset_index()

#-------------------------------------------------------

fecha=[] 
fecha=bta_df['FECHA_DIAGNOSTICO'] #Se llena con la fecha de notificación 
c=Counter(fecha) #Se cuentan los datos según la fecha de notificación
fechaN = pd.DataFrame() #Se crea una nueva referencia del DataFrame
fechaN['Fecha']=c.keys() #Se extraen los elementos únicos
fechaN['No. Casos']=c.values() #Se extrae la frecuencia de cada elemento único
fechaN=fechaN.sort_values(by='Fecha',ascending=False) #Se ordenan según la fecha

#-------------------------------------------------------

figB = px.bar(local, x='Localidades', y='No. Casos', title='Casos por localidad')
figB2 = px.bar(genero_ob, x='EDAD', y=0, color='SEXO', title='Género y edad')
figB3 = px.line(fechaN, x='Fecha', y='No. Casos', title='Evolución de casos')

#-------------------------------------------------------

image_filename = 'MapaColombia.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash()

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

    html.Br(),

    html.Img(src='data:image/png;base64,{}'.format(encoded_image)),

    html.Div(children='''
        Colombia graphs
        '''),

    dcc.Graph(
        id='Número de Casos_graph',
        figure=figC
    ),

    dcc.Graph(
        id='Ciudades con mayor número de Contagiados_graph',
        figure=figC2
    ),

    dcc.Graph(
        id='Casos Totales por tipo de contagio_graph',
        figure=figC3
    ),

    dcc.Graph(
        id='Estado de los pacientes',
        figure=figC4
    ),

    dcc.Graph(
        id='Muertes',
        figure=figC6
    ),

    dcc.Graph(
        id='falle',
        figure=figC7
    ),
    
    dcc.Graph(
        id='evolucion',
        figure=figC8
    ),

    html.Div(children='''
        Bogotá graphs
        '''),

    dcc.Graph(
        id='localidades_graph',
        figure=figB
    ),

    dcc.Graph(
        id='edad_sexo_graph',
        figure=figB2
    ),

    dcc.Graph(
        id='evolucion_tiempo_graph',
        figure=figB3
    )
]
)

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from urllib.request import urlopen
from collections import Counter
import json
from sodapy import Socrata
from datetime import datetime


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


app = dash.Dash()

fig = px.line(df1, x='Mes', y='No. Casos',title='Número de Casos')
fig2 = px.bar(df2, x='Ciudad', y='No. Casos',title='Ciudades con mayor número de Contagiados')
fig3 = px.pie(df3, values='No. Casos' , names='Tipo',title='Casos Totales por tipo de contagio')
fig4 = px.pie(df4, values='No. Casos' , names='Estado',title='Estado de los pacientes')
fig6 = px.bar(df6,  x='Pais de Procedencia', y='No. Casos',title='País de Procedencia')
fig7 = px.line(df5,  x=x, y=y,title='Fallecimientos')
fig8 = px.line(df_fechas, x='Fecha', y='No. Casos', title='Evolución de casos')

app.title = 'Dash covid'
 
app.layout = html.Div(
    
    html.Div([
        
        html.H1(children='Hello there :D'),
    
        html.Div(children='''
        Dash: A web application framework for python
        '''),

        dcc.Graph(
            id='Número de Casos_graph',
            figure=fig
        ),
        dcc.Graph(
            id='Ciudades con mayor número de Contagiados_graph',
            figure=fig2
        ),
        dcc.Graph(
            id='Casos Totales por tipo de contagio_graph',
            figure=fig3
        ),
         dcc.Graph(
            id='Estado de los pacientes',
            figure=fig4
        ),
        dcc.Graph(
            id='Muertes',
            figure=fig6
        ),
        dcc.Graph(
            id='falle',
            figure=fig7
        ),
        dcc.Graph(
            id='evolucion',
            figure=fig8
        )
    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)
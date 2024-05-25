import pandas as pd
import requests
import plotly.express as px
from dash import Dash, dcc, html

# Se llaman los CSVs que se van a utilizar
df= pd.read_csv("IED-segun-entidad-federativa-en-2023.csv") # Map

geo= 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
mx_geo= requests.get(geo).json()

df_anual = pd.read_csv("Flujo-anual-de-IED-en-Servicios-Financieros-y-de-Seguros.csv") # Static

df_anual_tipo_inver = pd.read_csv("Flujo-anual-de-IED-en-Servicios-Financieros-y-de-Seguros+.csv")

df_tri= pd.read_csv("Flujo-trimestral-de-IED-en-Servicios-Financieros-y-de-Seguros.csv") # Static

df_tri_tipo_inver= pd.read_csv("Flujo-trimestral-de-IED-en-Servicios-Financieros-y-de-Seguros-.csv") 

# Dashboard
app= Dash(__name__) # Inicializa Dash

fig_map= px.choropleth(
    data_frame= df,
    geojson= mx_geo, 
    featureidkey='properties.name', # Ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
    locations= 'State', # Cambiamos las localizaciones para que sean nyestra columna de Códigos de Estado
    # Tienen que ser los códigos de Estado, no pueden ser los nombres
    scope="north america", # Región de mapeado
    color= 'Investment (USD)',
    hover_data=['State ID', 'State'], # Definicmos los valores que aparecerán al poner el mouse por encima 
    color_continuous_scale= "matter", # Como cambia el color con % de Inverisón
    template= 'plotly_dark',)    
    # Lo que quieres que se vea o no en el mapa:
fig_map.update_geos(showcountries= True, showcoastlines= True, showland= True, fitbounds="locations")   
fig_map.update_layout(height=750, margin={'l': 2, 'b': 5, 'r': 2, 't': 1}, 
                      hoverlabel= dict(font_size= 20))    
    
# Annual Static
fig_annual= px.scatter(df_anual, x='Year_', y='Investment (USD)',)
         
fig_annual.update_traces(mode='markers+lines') # Grafica líneas y muestra en los picos marcas
    
fig_annual.update_xaxes(showgrid= False, showspikes=True)
fig_annual.update_yaxes(type= 'linear', showspikes=True)

fig_annual.update_layout(height=600, margin={'l': 5, 'b': 5, 'r': 5, 't': 35},
                        title= '1999-2023 IED', xaxis_title= 'Años', yaxis_title= 'Inversión',
                        plot_bgcolor="rgba(0, 0, 0, 0)",  # Fondo transparente
                        paper_bgcolor="rgba(0, 0, 0, 0)", 
                        hoverlabel= dict(font_size= 20)) 

# Annual: Type_Investment
fig_t_investment= px.scatter(df_anual_tipo_inver, y='Investment (USD)', x='Year_', color='Investment Type')
fig_t_investment.update_traces(mode="lines")

# Traza línea de la coordenada x en el cursor
fig_t_investment.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", 
                    spikemode="across", showgrid= False, spikethickness=.5
                    )
# Traza línea de la coordenada y en el cursor
fig_t_investment.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=.5)
    
# Le agrega unos ajustes a la gráfica  (forma, título, nombre x-y, fondo)  
fig_t_investment.update_layout(height=600, margin={'l': 5, 'b': 5, 'r': 5, 't': 50},
                        title= '1999-2023 Tipo de IED', xaxis_title= 'Años', yaxis_title= 'Inversión',
                        plot_bgcolor="rgba(0, 0, 0, 0)",  
                        paper_bgcolor="rgba(0, 0, 0, 0)", 
                        hoverlabel= dict(font_size= 20)) # Tamaño de etiquetas al poner el cursor encima de los datos  

# Quarter: Type_Investment
fig_tri= px.scatter(df_tri_tipo_inver, x='Quarter_', y='Investment (USD)', color='Investment Type')
    
fig_tri.update_traces(mode='lines')
    
fig_tri.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", 
                    spikemode="across", showgrid= False, spikethickness=.5)
fig_tri.update_yaxes(showspikes=True, spikecolor="red", spikethickness=.5)

fig_tri.update_layout(height=600, margin={'l': 5, 'b': 5, 'r': 5, 't': 50},
                        title= '1999-2023 Trimestral IED', xaxis_title= 'Años', yaxis_title= 'Inversión',
                        plot_bgcolor="rgba(0, 0, 0, 0)",  
                        paper_bgcolor="rgba(0, 0, 0, 0)", 
                        hoverlabel= dict(font_size= 20)) 

# Static Quarter
fig_static_tri= px.scatter(df_tri, x='Quarter_', y='Investment (USD)')
    
fig_static_tri.update_traces(mode='lines')
    
fig_static_tri.update_xaxes(showgrid= False, showspikes=True)
fig_static_tri.update_yaxes(type= 'linear', showspikes=True)

fig_static_tri.update_layout(height=600, margin={'l': 5, 'b': 5, 'r': 5, 't': 35},
                        title= '1999-2023 IED', xaxis_title= 'Años', yaxis_title= 'Inversión',
                        plot_bgcolor="rgba(0, 0, 0, 0)", 
                        paper_bgcolor="rgba(0, 0, 0, 0)", 
                        hoverlabel= dict(font_size= 20)) 

# App Layout
app.layout= html.Div([ # Diseño de la Página  
    html.Div([      
    # Map
        html.Div([
            html.Br(), # Espacio en blanco
            html.H1("IED Según Entidad Federativa 2023:)", style={'text-align': 'center', 'color': 'green'}
                    ), # Título
        html.Br(), # Espacio en blanco 
        dcc.Graph(id='Mexico_Map', figure=fig_map, style={'float':'center'}), # Dibuja el mapa
        ]),
    # Annual
        html.Div([    
            html.H1('Datos Por Año', style= {'text-align': 'center', 'color': 'green'}),
            html.H3(children='Presionar el Investment Type que se desea ocultar',
                    style={'color': '#7FDBFF', 'text-align': 'center'}),
            dcc.Graph(id='indicator_investment_annual', style={'float': 'left', 'width': '60%',}, figure= fig_t_investment),
            dcc.Graph(id='static_annual', style={'float':'right', 'width': '40%'}, figure=fig_annual),
        ]),
    # Quarter
        html.Div([       
            html.H1('Datos Por Trimestre', style= {'color': 'green', 'text-align': 'center'}),
            html.Br(),
            dcc.Graph(id='indicator_investment_tri', style={'float': 'left', 'width': '60%'}, figure= fig_tri),
            dcc.Graph(id='static_tri', style={'float': 'right', 'width': '40%',}, figure= fig_static_tri),
        ])
    ], #style={'height': '300', 'width': '300', 'position': 'relative'}
    )
],style= {'background-color': 'rgb(17, 17, 17)', 'height': '250vh' })

if __name__== '__main__':
    app.run_server(port= 80, debug= True)
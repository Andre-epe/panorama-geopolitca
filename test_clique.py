import pandas as pd
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
from data import database

st.set_page_config(layout="wide")
st.title("Mapa Mundi Interativo")

# Carregar base de dados dos países
world = database()

def mapa_mundi():
    m = folium.Map(location=[0, 0], zoom_start=2)
    # Adicionar os polígonos dos países sem borda preta ao clicar
    for _, row in world.iterrows():
        folium.GeoJson(
            row['Geometria'],
            tooltip=row['País'],  # Exibir o nome do país ao passar o mouse
            style_function=lambda x: {
                'fillColor': 'blue',
                'color': 'blue',
                'weight': 1,  # Espessura da borda
                'fillOpacity': 0.3,
                'interactive': False  # Desativa a interatividade do clique
            }
        ).add_to(m)  # Removemos a highlight_function
        
    # Adicionar funcionalidade de clique
    m.add_child(folium.LatLngPopup())

    # Exibir o mapa e capturar o clique
    map_data = st_folium(m, width=1000, height=600)
    return map_data 

map_data = mapa_mundi()

def pais_clicado():
    # Verifica se houve clique no mapa
    if map_data and map_data.get("last_clicked"):
        lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        
        # Criar um ponto com as coordenadas clicadas
        clicked_point = Point(lon, lat)
        
        # Verificar em qual país o clique ocorreu
        clicked_country = None
        for _, row in world.iterrows():
            if row['Geometria'].contains(clicked_point):
                clicked_country = row['País']
                break
        
        # if clicked_country:
        #     return st.success(f"Você clicou no país: {clicked_country}")
        # else:
        #     return st.warning("Clique fora de um país detectado.")
        return clicked_country
pais_clicado()
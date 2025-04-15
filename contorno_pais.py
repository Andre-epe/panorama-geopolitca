import folium
import requests

# Criando o mapa
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Baixando o GeoJSON com os limites do Brasil
url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
geojson_data = requests.get(url).json()

# Adicionando a camada GeoJSON
folium.GeoJson(geojson_data, name="Brasil").add_to(m)

# Exibir mapa
m

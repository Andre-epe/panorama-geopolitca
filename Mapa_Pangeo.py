import pandas as pd
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static, st_folium
from shapely.geometry import Point
from data import data_countries, data_publications
import base64
import webbrowser
from streamlit_javascript import st_javascript

    
st.set_page_config(layout="wide")

# screen_size = st_javascript("window.innerWidth + ',' + window.innerHeight")
# if screen_size:
#     width, height = map(int, screen_size.split(','))
#     # st.write(f"Largura: {width}, Altura: {height}")    ##No monitor é 1502


st.markdown(
    """
    <style>
        .block-container {
        
            padding-top: 2.5em;  ############## Botei em 1.8
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #F0F2F6;
}
[data-testid="stHeader"] {
    background-color: #F0F2F6;
}
</style>
""")

col1, col2 = st.columns([6.1,1])


with col1:
    # st.markdown("<h1 style='color: #0C2340;'>Panorama Geopolítico de Óleo, Gás e Biocombustíveis⛽</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #0C2340; font-size: 40px;'>Panorama Geopolítico de Óleo, Gás e Biocombustíveis🌎</h1>", unsafe_allow_html=True) #Fonte 42 no meu notebook; 50 no monitor
    st.markdown(
    """<hr style="height: 2.4px; border: none; background-color: #7a7b7d; margin: -18px 0; width: 95%;">""", #### Na margin eu consegui juntar a linha do titulo
    unsafe_allow_html=True
)

with col2:
    # st.write("")
    # st.write("")
    # st.write("\n")
    st.image('Logo Cinza.png')

# st.markdown(
#     "<h1 style='color: #9ea0a3; font-size: 30px; font-weight: normal;'>Mapa PANGEO</h1>",
#     unsafe_allow_html=True
# )


col1, col2 = st.columns([4,1])


with col2:
    
    col3, col4 = st.columns([1,1])
    with col3:
        # CSS personalizado para o botão
        st.markdown("""
            <style>
            div.st-key-meu_botao_dark_mode {
                display: flex;
                justify-content: center; /* Centraliza o botão dentro do contêiner */
            }

            div.st-key-meu_botao_dark_mode button {
                background-color: transparent !important;
                color: #434445 !important;
                border: 1px solid #7a7b7d !important;
                display: flex;
                align-items: center; /* Centraliza o conteúdo verticalmente */
                justify-content: center; /* Centraliza o texto horizontalmente */
                text-align: center; /* Centraliza o texto dentro do botão */
                width: 100%; /* Garante alinhamento correto */
            }

            div.st-key-meu_botao_dark_mode button p {
                font-size: 12px !important;
                font-weight: bold;
                line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                margin: 0 auto !important; /* Garante centralização */
                text-align: center !important; /* Centraliza o texto dentro do botão */
            }
            </style>
        """, unsafe_allow_html=True)
        
        # st.button('Modo Escuro', key='meu_botao_dark_mode', icon=":material/dark_mode:")

    with col4:

        # CSS personalizado para o botão
        st.markdown("""
            <style>
            div.st-key-meu_botao_baixar_dados {
                display: flex;
                justify-content: center; /* Centraliza o botão dentro do contêiner */
            }

            div.st-key-meu_botao_baixar_dados button {
                background-color: transparent !important;
                color: #434445 !important;
                border: 1px solid #7a7b7d !important;
                display: flex;
                align-items: center; /* Centraliza o conteúdo verticalmente */
                justify-content: center; /* Centraliza o texto horizontalmente */
                text-align: center; /* Centraliza o texto dentro do botão */
                width: 100%; /* Garante alinhamento correto */
            }

            div.st-key-meu_botao_baixar_dados button p {
                font-size: 12px !important;
                font-weight: bold;
                line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                margin: 0 auto !important; /* Garante centralização */
                text-align: center !important; /* Centraliza o texto dentro do botão */
            }
            </style>
        """, unsafe_allow_html=True)
        
        # st.button('Baixar Dados', key='meu_botao_baixar_dados', icon=":material/download:")

with col1:    
    st.markdown(
        """
        <style>
        [kind="pillsActive"][data-testid="stBaseButton-pillsActive"] {
            background: #0C2340;  /* Cor de fundo quando ativo */
            color: white;  /* Cor da fonte quando ativo */
        }
        
        [data-testid="stPillsContainer"] button {
            background: #f0f0f0;  /* Cor de fundo padrão */
            color: black;  /* Cor da fonte padrão */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    

    st.markdown(
    """<h3 style='margin-top: -5px; margin-bottom: -200px; font-size: 16px;'>Publicações disponíveis</h3>""",
    unsafe_allow_html=True
    )


    
    lista_publicacoes = list(data_publications().loc[data_publications()['pais_ou_regiao']=='País', 'tipo'].unique())
    lista_publicacoes.append('Todas as publicações')
    publicacao_clicada = st.pills(
            label = '', 
            options= lista_publicacoes,
            default='Todas as publicações',
            selection_mode='single')

# st.write(publicacao_clicada) ############################################# VER MAIS TARDE ESSE PRINT COM O MULTISELECT ATIVADO PARA ST.PILLS ######################################3

world = data_countries()
regions = world['Região'].unique().tolist()
regions.append('Mundo')


# col1, col2, col3 = st.columns([1,4,1])
with st.sidebar:

    # st.image('Logo-epe-negativa.png')

    st.write("")
    st.write("")

    st.html(
        """
    <style>
    [data-testid="stSidebarContent"] {
        background-color: rgb(12, 35, 64);
        color: white; /* Para melhor contraste com o fundo escuro */
    }

    /* Para alterar também a cor dos elementos de navegação */
    [data-testid="stSidebarNav"] span {
        color: white;
    }
    </style>
    """
    )
    a = "Selecione uma Região 📌"
    cor_hex = "#FFFFFF"  # Exemplo de cor HEX

    # Exibindo a expressão LaTeX com cor HEX
    latex_expression = f'$\large \\textsf{{\\textcolor{{{cor_hex}}}{{{a}}}}}$'

    selected_region = st.radio(latex_expression, 
                            options=regions,
                            index=7,
                            format_func=lambda option: f'$\scriptsize \\textit{{\\textcolor{{{cor_hex}}}{{{option}}}}}$')
    
    
    # ########### Opção de dowload
    # # Adicionar CSS personalizado
    # st.markdown("""
    # <style>
    #     .stDownloadButton button {
    #         background-color: transparent !important;
    #         color: #FFFFFF !important;
    #         border: 0px solid #FFFFFF;
    #     }
        
    #     /* Seletor específico para o texto do botão */
    #     .stDownloadButton button p {
    #         font-size: 13px !important; /* Tamanho da fonte do texto */
    #     }
        
    #     .stDownloadButton button:hover {
    #         background-color: rgba(255, 75, 75, 0.1) !important;
    #         color: #FF4B4B !important;
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    # # Criar um arquivo vazio
    # empty_file = b''

    # # Exibir o botão de download
    # st.download_button(
    #     label="Baixar arquivos do mapa",
    #     data=empty_file,
    #     file_name="arquivo_vazio.txt",
    #     mime="text/plain",
    #     icon=":material/download:"
    # )
    
    st.markdown(
        """
        <style>
        .sidebar-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 250px; /* Ajuste conforme necessário */
            padding: 10px;
            text-align: left;
            background-color: rgba(0, 0, 0, 0); /* Leve transparência */
            color: white;
            font-size: 12px;
        }
        </style>
        <div class="sidebar-footer">
            📌 Superintendência de Derivados de Petróleo e Biocombustíveis/<b>DPG<b> <br>
            📧 Contato: <i>SDB@epe.gov.br</i>
        </div>
        """,
        unsafe_allow_html=True
    )

def zoom_region_map(selected_region=selected_region):
    if selected_region == 'Mundo':
        location = [25,70]
        var_zoom=2
    elif selected_region == 'Ásia':
        location = [37,120]
        var_zoom=2.9
    elif selected_region == 'África':
        location = [5,52]
        var_zoom=3.4
    elif selected_region == 'Europa':
        location = [55,80]
        var_zoom=3.4
    elif selected_region == 'América do Sul e Central':
        location = [-20,-40]
        var_zoom=3.48
    elif selected_region == 'Antártica':
        location = [-50,0]
        var_zoom=2
    elif selected_region == 'Oceania':
        location = [-20,160]
        var_zoom=3.4
    elif 'América do Norte':
        location = [45,-80]
        var_zoom=3.48

    return location, var_zoom
    
location = zoom_region_map()[0]
var_zoom = zoom_region_map()[1]


countries = world['País'].tolist()
# Interface do Streamlit

publicacoes_paises_pintado = data_publications()
publicacoes_paises_pintado_filtrado = publicacoes_paises_pintado.loc[publicacoes_paises_pintado['Região']==selected_region].copy() #Filtrar na região
publicacoes_paises_pintado_filtrado = publicacoes_paises_pintado_filtrado.loc[publicacoes_paises_pintado_filtrado['tipo']==publicacao_clicada].copy() if publicacao_clicada != 'Todas as publicações' else publicacoes_paises_pintado_filtrado #Filtrar no tipo de publicação
selected_country = publicacoes_paises_pintado_filtrado['nome'].unique() if selected_region != 'Mundo' else publicacoes_paises_pintado['nome'].unique() #obter a lista de países depois das filtragens

# color = st.color_picker("Escolha uma cor", "#ff0000")
color = "#ff0000"

def mapa_mundi(location = location, var_zoom=var_zoom):
   
    # Criar o mapa
    m = folium.Map(location, zoom_start=var_zoom, tiles="OpenStreetMap")
    # Adicionar países ao mapa
    for _, row in world.iterrows():
        if row['País Traduzido'] in selected_country:
            folium.GeoJson(
                row['Geometria'],
                tooltip=row['País Traduzido'],  # Exibir o nome do país ao passar o mouse
                style_function=lambda x: {
                    'fillColor': '#0C2340',
                    'color': '#0C2340',
                    'weight': 1.3,  # Espessura da borda
                    'fillOpacity': 0.6,
                    'interactive': False  # Desativa a interatividade do clique
                }
            ).add_to(m)  # Removemos a highlight_function
        else:
            folium.GeoJson(row['Geometria'], 
                    style_function=lambda x: {
                    #'fillColor': 'blue',
                    'color': '##6a6a6b',
                    'weight': 1,  # Espessura da borda
                    'fillOpacity': 0.05,
                    'interactive': False  # Desativa a interatividade do clique
                }
            ).add_to(m)

    # Adicionar funcionalidade de clique
    m.add_child(folium.LatLngPopup())

    # Exibir o mapa e capturar o clique
    map_data = st_folium(m, width=1200, height=700) # Na tela do monitor height = 780

    return map_data


################ MAPA QUE CONSEGUE MUDAR PARCIALMENTE AS CORES ##################33
# def mapa_mundi(location = location, var_zoom=var_zoom, ocean_color="#304878"):
#     # Criar o mapa com o estilo de fundo desejado (exemplo: CartoDB positron)
#     m = folium.Map(location, zoom_start=var_zoom, tiles="CartoDB positron")

#     # Adicionar uma camada customizada para o oceano (pode ser qualquer cor desejada)
#     folium.TileLayer(
#         tiles="CartoDB positron",  # Fundo claro
#         name="Ocean Layer",
#         overlay=True,
#         control=False,
#         attr="Map tiles by CartoDB, under CC BY 3.0."
#     ).add_to(m)

#     # Aqui vamos estilizar o oceano para a cor mais escura (#304878)
#     folium.GeoJson(
#         # GeoJSON de oceanos. Você pode usar seu arquivo ou ajustá-lo.
#         # Para o propósito de exemplo, vou criar uma forma simples para simular
#         # o oceano. Você deve substituir isso pelo seu arquivo de oceanos.
#         {
#             "type": "FeatureCollection",
#             "features": [
#                 {
#                     "type": "Feature",
#                     "properties": {},
#                     "geometry": {
#                         "type": "Polygon",
#                         "coordinates": [
#                             [
#                                 [-180, -90],
#                                 [180, -90],
#                                 [180, 90],
#                                 [-180, 90],
#                                 [-180, -90]
#                             ]
#                         ]
#                     }
#                 }
#             ]
#         },
#         style_function=lambda x: {
#             'fillColor': ocean_color,  # A cor do oceano
#             'color': ocean_color,
#             'weight': 0,
#             'fillOpacity': 0.5  # Controle da opacidade do oceano
#         }
#     ).add_to(m)

#     # Adicionar países ao mapa
#     for _, row in world.iterrows():
#         if row['País Traduzido'] in selected_country:
#             folium.GeoJson(
#                 row['Geometria'],
#                 tooltip=row['País Traduzido'],  # Exibir o nome do país ao passar o mouse
#                 style_function=lambda x: {
#                     'fillColor': '#0C2340',
#                     'color': '#0C2340',
#                     'weight': 1.3,  # Espessura da borda
#                     'fillOpacity': 0.6,
#                     'interactive': False  # Desativa a interatividade do clique
#                 }
#             ).add_to(m)
#         else:
#             folium.GeoJson(
#                 row['Geometria'],
#                 style_function=lambda x: {
#                     'color': '##6a6a6b',
#                     'weight': 1,  # Espessura da borda
#                     'fillOpacity': 0.05,
#                     'interactive': False  # Desativa a interatividade do clique
#                 }
#             ).add_to(m)

#     # Adicionar funcionalidade de clique com LatLngPopup
#     m.add_child(folium.LatLngPopup())

#     # Exibir o mapa e capturar o clique
#     map_data = st_folium(m, width=1200, height=750)

#     return map_data

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
                clicked_country = row['País Traduzido']
                break
        
        # if clicked_country:
        #     return st.success(f"Você clicou no país: {clicked_country}")
        # else:
        #     return st.warning("Clique fora de um país detectado.")
        return clicked_country


def get_image_base64(image_path):
    """Converte a imagem para base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


st.markdown("""
<span style='font-size:16px; font-style:italic; color:#333;'>
<span style='font-style: normal;'>💡</span>
<u>Clique no mapa</u> para selecionar o <b>País de interesse!</b>
</span>
""", unsafe_allow_html=True)
    

col1, col2 = st.columns([2.05,1], vertical_alignment='top')
with col1:
    map_data = mapa_mundi()

# Adição do fundo cinza na coluna lateral direita de cima #e4e6eb
st.markdown(
    """
    <style>
    div.st-key-minha_coluna3 {
        background-color: #e4e6eb;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adição do fundo cinza na coluna lateral direita de baixo #e4e6eb
st.markdown(
    """
    <style>
    div.st-key-minha_coluna4 {
        background-color: #e4e6eb;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



with col2:
    # st.write('')
    # st.write('')
    with st.container(key="minha_coluna3"):

        pais_clicado_mapa = pais_clicado()

        pais_clicado_mapa = 'Brasil' if (pais_clicado_mapa == None and selected_region == 'América do Sul e Central') else pais_clicado_mapa ####################################################### CORRIGIR ISSO BOTANDO POR ORDEM ALFABÉTICA ####################################################
        pais_clicado_mapa = 'Canadá' if (pais_clicado_mapa == None and selected_region == 'América do Norte') else pais_clicado_mapa
        pais_clicado_mapa = 'Irã' if (pais_clicado_mapa == None and selected_region == 'Ásia') else pais_clicado_mapa
        pais_clicado_mapa = 'República do Congo' if (pais_clicado_mapa == None and selected_region == 'África') else pais_clicado_mapa
        pais_clicado_mapa = 'Alemanha' if (pais_clicado_mapa == None and selected_region == 'Europa') else pais_clicado_mapa
        pais_clicado_mapa = 'Antártida' if (pais_clicado_mapa == None and selected_region == 'Antártica') else pais_clicado_mapa
        pais_clicado_mapa = 'Austrália' if (pais_clicado_mapa == None and selected_region == 'Oceania') else pais_clicado_mapa
        pais_clicado_mapa = 'Brasil' if (pais_clicado_mapa == None and selected_region == 'Mundo') else pais_clicado_mapa

        if pais_clicado_mapa != 'Brasil':
            st.write("")
            st.write("")
            st.write("")
    
        st.markdown(
        f"<div style='text-align: center; margin-top: 0;'><p style='font-size: 17px; font-family: \"Source Sans Pro\", sans-serif; font-weight: normal;'><span style='color: #636466;'>Região selecionada:</span> <span style='color: #0C2340; font-weight: bold;'>{selected_region}</span></p></div>",
        unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1,1], vertical_alignment='center')

        with col1:
            
            image_path = fr"Contornos/{selected_region}.png"
            img_base64 = get_image_base64(image_path)

            # Criando HTML para centralizar a imagem
            html_code = f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_base64}" width="150">
            """
            st.markdown(html_code, unsafe_allow_html=True)
        


        with col2:

            #Colocar a data de publicação da publicação acima da imagem
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -35px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 10px;">Publicação: Junho/2013</span>
                </div>
                """, 
                unsafe_allow_html=True)

            # Configurar a Imagem adicionada para representar o estudo

            figurinha_botao = '📖' if not (selected_region == 'Oceania' or selected_region == 'Antártica') else ''
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -40px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 40px;">{figurinha_botao}</span>
                </div>
                """, 
                unsafe_allow_html=True)


            if selected_region not in ['Oceania', 'Antártica']:
                links = {
                    'Ásia': "https://drive.google.com/file/d/1XAZC-u05PBvhP6ZsNvkqV4_sBO4zgHW0/view?usp=sharing",
                    'África': "https://drive.google.com/file/d/1GedlRMVsvymqwFqevZB2emymQN4P76pu/view?usp=sharing",
                    'Europa': "https://drive.google.com/file/d/1SVf2mXHsOCMaNtRbNH-GTaSD7M7JTGLF/view?usp=sharing",
                    'América do Sul e Central': "https://drive.google.com/file/d/1_fREydk0X-dOJ51qYnD3PU-0MVwDbgKA/view?usp=sharing",
                    'América do Norte': "https://drive.google.com/file/d/1gBcl_f6sGOrjvjcIQoYgIXWl5JZbRsp_/view?usp=sharing",
                    'Mundo': "https://drive.google.com/file/d/14Hrt6IB-RvLYkUIurLHtSNpjjhih4OA7/view?usp=sharing"
                }

            url = links.get(selected_region)

            st.markdown(f"""
                <style>
                .custom-button-container {{
                    display: flex;
                    justify-content: center;
                    margin-top: 10px;
                }}

                a.custom-button {{
                    background-color: transparent;
                    color: #434445;
                    border: 0px solid #7a7b7d;
                    font-size: 13px;
                    font-weight: bold;
                    line-height: 1.1;
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                }}

                a.custom-button:hover {{
                    text-decoration: underline;
                }}
                </style>

                <div class="custom-button-container">
                    <a href="{url}" target="_blank" class="custom-button">
                        Estudo do Mercado Internacional de Gás Natural
                    </a>
                </div>
            """, unsafe_allow_html=True)



            if selected_region == 'Mundo':
                st.markdown(
    """<hr style="height: 0.09px; border: none; background-color: #cccccf; margin: -0px 0;">""", #### Na margin eu consegui juntar a linha do titulo #7a7b7d
    unsafe_allow_html=True
            )
                

                #Colocar a data de publicação da publicação acima da imagem
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: -35x;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 10px;">Publicação: Junho/2016</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                    
                # Configurar a Imagem adicionada para representar o estudo
                st.markdown(
                    """
                    <div style="text-align: center; margin-bottom: -40px;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 40px;">📖</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)


                link = {
        'Mundo': "https://drive.google.com/file/d/14Hrt6IB-RvLYkUIurLHtSNpjjhih4OA7/view?usp=sharing"}
                
                url = link.get('Mundo')

                st.markdown(f"""
                        <style>
                        .custom-button-container {{
                            display: flex;
                            justify-content: center;
                            margin-top: 10px;
                        }}

                        .custom-button {{
                            background-color: transparent;
                            color: #434445;
                            border: 0px solid #7a7b7d;
                            font-size: 13px;
                            font-weight: bold;
                            line-height: 1.1;
                            padding: 0.5rem 1rem;
                            cursor: pointer;
                            text-align: center;
                            text-decoration: none;
                        }}

                        .custom-button:hover {{
                            text-decoration: underline;
                        }}
                        </style>

                        <div class="custom-button-container">
                            <a href="{url}" target="_blank" class="custom-button">
                                Estudo do Mercado Internacional de Gás Natural
                            </a>
                        </div>
                    """, unsafe_allow_html=True)


        if pais_clicado_mapa != 'Brasil':
            st.write("")
            st.write("")
            st.write("")
    # st.write("")
    # st.write("")

    with st.container(key="minha_coluna4"):
        
        if (pais_clicado_mapa != 'Brasil') and (pais_clicado_mapa != 'Argentina'):
            st.write("")
            st.write("")
            st.write("")
            # st.write("")

        st.markdown(
        f"<div style='text-align: center; margin-top: 0;'><p style='font-size: 17px; font-family: \"Source Sans Pro\", sans-serif; font-weight: normal;'><span style='color: #636466;'>País selecionado:</span> <span style='color: #0C2340; font-weight: bold;'>{pais_clicado_mapa}</span></p></div>",
        unsafe_allow_html=True
        )

        if (pais_clicado_mapa != 'Brasil') and (pais_clicado_mapa != 'Argentina'):
            st.write("")

    
        col1, col2 = st.columns([1,1], vertical_alignment='center')
        
        with col1:

            image_path = fr"Contornos/{pais_clicado_mapa}.png"
            img_base64 = get_image_base64(image_path)

            # Criando HTML para centralizar a imagem
            html_code = f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_base64}" width="150">
            """

            st.markdown(html_code, unsafe_allow_html=True)
            
            st.write("")
            
        with col2:
            
            publicacoes_paises = data_publications()
            publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['pais_ou_regiao']=='País'].copy()
            publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['nome']==pais_clicado_mapa].copy()
            publicacoes_paises['edicao'] = pd.to_datetime(publicacoes_paises['edicao'], errors='coerce', format = r"%m/%Y")
            publicacoes_paises = publicacoes_paises.sort_values(by='edicao', ascending=True)
            publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['tipo']==publicacao_clicada] if not (publicacao_clicada == 'Todas as publicações') else publicacoes_paises
            publicacoes_paises = publicacoes_paises.reset_index(drop=True)
            lista_paises = publicacoes_paises['nome'].unique()
            
            
            try:
                titulo_botao = publicacoes_paises.loc[publicacoes_paises.index==0, 'nome_publicação'].item()
            except ValueError:
                titulo_botao = ''

            try:
                data_publicacao_botao = publicacoes_paises.loc[publicacoes_paises.index==0, 'data_publicacao'].item()
                # data_publicacao_botao = data_publicacao_botao.strip('Publicação: ')
            except ValueError:
                data_publicacao_botao = ''


            

            #Colocar a data de publicação da publicação acima da imagem
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -20px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 10px;">{data_publicacao_botao}</span>
                </div>
                """, 
                unsafe_allow_html=True)

            # Configurar a Imagem adicionada para representar o estudo
            figurinha_botao = '📑' if pais_clicado_mapa in lista_paises else ''
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -40px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 40px;">{figurinha_botao}</span>
                </div>
                """, 
                unsafe_allow_html=True)
            

            url = publicacoes_paises.loc[publicacoes_paises.index==0, 'url'].item()
            st.markdown(f"""
                    <style>
                    .custom-button-container {{
                        display: flex;
                        justify-content: center;
                        margin-top: 10px;
                    }}

                    a.custom-button {{
                        background-color: transparent;
                        color: #434445 !important;
                        border: 0px solid #7a7b7d;
                        font-size: 13px;
                        font-weight: bold;
                        line-height: 1.1;
                        padding: 0.5rem 1rem;
                        cursor: pointer;
                        text-align: center;
                        text-decoration: none;
                    }}

                    a.custom-button:hover {{
                        text-decoration: underline;
                    }}
                    </style>

                    <div class="custom-button-container">
                        <a href="{url}" target="_blank" class="custom-button">
                            {titulo_botao}
                        </a>
                    </div>
                """, unsafe_allow_html=True)

            
            if publicacoes_paises.shape[0] >= 2:

                def open_page_2(publicacoes_paises=publicacoes_paises):
                    url = publicacoes_paises.loc[publicacoes_paises.index==1, 'url'].item()
                    return webbrowser.open(url)
                
                try:
                    titulo_botao = publicacoes_paises.loc[publicacoes_paises.index==1, 'nome_publicação'].item()
                except ValueError:
                    titulo_botao = ''

                try:
                    data_publicacao_botao = publicacoes_paises.loc[publicacoes_paises.index==1, 'data_publicacao'].item()
                    # data_publicacao_botao = data_publicacao_botao.strip('Publicação: ')
                except ValueError:
                    data_publicacao_botao = ''

                 #Adicionar a linha que separa as publicações
                st.markdown(
                    """<hr style="height: 0.09px; border: none; background-color: #cccccf; margin: -0px 0;">""", 
                    unsafe_allow_html=True
                                        )
                                
                #Colocar a data de publicação da publicação acima da imagem
                st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -20px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 10px;">{data_publicacao_botao}</span>
                </div>
                """, 
                unsafe_allow_html=True)


                #📄📋🧾
                # Configurar a Imagem adicionada para representar o estudo
                figurinha_botao = '📑' if pais_clicado_mapa in lista_paises else ''
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: -40px;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 40px;">{figurinha_botao}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                


                url = publicacoes_paises.loc[publicacoes_paises.index==1, 'url'].item()
                st.markdown(f"""
                        <style>
                        .custom-button-container {{
                            display: flex;
                            justify-content: center;
                            margin-top: 10px;
                        }}

                        a.custom-button {{
                            background-color: transparent;
                            color: #434445 !important;
                            border: 0px solid #7a7b7d;
                            font-size: 13px;
                            font-weight: bold;
                            line-height: 1.1;
                            padding: 0.5rem 1rem;
                            cursor: pointer;
                            text-align: center;
                            text-decoration: none;
                        }}

                        a.custom-button:hover {{
                            text-decoration: underline;
                        }}
                        </style>

                        <div class="custom-button-container">
                            <a href="{url}" target="_blank" class="custom-button">
                                {titulo_botao}
                            </a>
                        </div>
                    """, unsafe_allow_html=True)



            if publicacoes_paises.shape[0] >= 3:

                def open_page_3(publicacoes_paises=publicacoes_paises):
                    url = publicacoes_paises.loc[publicacoes_paises.index==2, 'url'].item()
                    return webbrowser.open(url)
                
                try:
                    titulo_botao = publicacoes_paises.loc[publicacoes_paises.index==2, 'nome_publicação'].item()
                except ValueError:
                    titulo_botao = ''

                try:
                    data_publicacao_botao = publicacoes_paises.loc[publicacoes_paises.index==2, 'data_publicacao'].item()
                    # data_publicacao_botao = data_publicacao_botao.strip('Publicação: ')
                except ValueError:
                    data_publicacao_botao = ''

                #Adicionar a linha que separa as publicações
                st.markdown(
                    """<hr style="height: 0.09px; border: none; background-color: #cccccf; margin: -0px 0;">""",
                    unsafe_allow_html=True
                            )
                

                #Colocar a data de publicação da publicação acima da imagem
                st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -20px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 10px;">{data_publicacao_botao}</span>
                </div>
                """, 
                unsafe_allow_html=True)
            
                #📄📋
                # Configurar a Imagem adicionada para representar o estudo
                figurinha_botao = '📑' if pais_clicado_mapa in lista_paises else ''
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: -40px;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 40px;">{figurinha_botao}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                

                url = publicacoes_paises.loc[publicacoes_paises.index==2, 'url'].item()
                st.markdown(f"""
                        <style>
                        .custom-button-container {{
                            display: flex;
                            justify-content: center;
                            margin-top: 10px;
                        }}

                        a.custom-button {{
                            background-color: transparent;
                            color: #434445 !important;
                            border: 0px solid #7a7b7d;
                            font-size: 13px;
                            font-weight: bold;
                            line-height: 1.1;
                            padding: 0.5rem 1rem;
                            cursor: pointer;
                            text-align: center;
                            text-decoration: none;
                        }}

                        a.custom-button:hover {{
                            text-decoration: underline;
                        }}
                        </style>

                        <div class="custom-button-container">
                            <a href="{url}" target="_blank" class="custom-button">
                                {titulo_botao}
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                
        
        if (pais_clicado_mapa != 'Brasil') and (pais_clicado_mapa != 'Argentina'):
            st.write("")
            st.write("")
            st.write("")
            st.write("")






# # for _, row in world.iterrows():
# lista_aux = []
# for row in world.iterrows():
#     lista_aux.append(row)


# #Parte superior - 1° card
# if selected_country == 'Brasil':
#     st.write("")
# elif selected_country == 'Argentina':
#     pass 
# elif selected_country == 'Bolívia':
#     pass 
# elif selected_country == 'Venezuela':
#     pass 
# elif selected_country == 'Guiana':
#     pass 
# elif selected_country == 'Suriname':
#     pass

# #Parte inferior - 1° card
# if selected_country == 'Brasil':
#     st.write("")

# #Meiuca
# if selected_country == 'Brasil':
#     pass 

# #Parte superior - 2° card
# if selected_country == 'Brasil':
#     pass 

# #Parte inferior - 2° card
# if selected_country == 'Brasil':
#     pass


# # Título da página
# st.markdown(
#     "<div style='text-align: center;'>"
#     "<h1 style='color: #0C2340; font-size: 24px;'>Timeline das Publicações do Panorama Geopolítico</h1>"
#     "</div>",
#     unsafe_allow_html=True
# )

# # Estilos
# st.markdown("""
# <style>
# .timeline-container {
#     position: relative;
#     margin: 50px auto;
#     width: 90%;
#     max-width: 900px;
# }
# .timeline-line {
#     position: absolute;
#     top: 0;
#     left: 50%;
#     transform: translateX(-50%);
#     width: 2px;
#     height: 100%;
#     background: repeating-linear-gradient(
#         to bottom,
#         #7a7b7d,
#         #7a7b7d 10px,
#         transparent 10px,
#         transparent 20px
#     );
#     z-index: 0;
# }
# .timeline-block {
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
#     margin: 40px 0;
#     position: relative;
#     z-index: 1;
# }
# .timeline-date {
#     background: #F0F2F6;
#     border: 2px solid #7a7b7d;
#     color: #7a7b7d;
#     font-weight: normal;
#     border-radius: 50%;
#     width: 80px;
#     height: 80px;
#     line-height: 80px;
#     text-align: center;
#     z-index: 2;
# }
# .timeline-content {
#     width: 40%;
#     background: transparent;
#     padding: 15px;
#     border-radius: 8px;
#     box-shadow: 0 0px 0px rgba(0,0,0,0.1);
# }
# .timeline-img {
#     width: 70%;
#     max-width: 200px;
#     height: auto;
#     border-radius: 8px;
#     display: block;
#     margin: 0 auto;
# }
# .timeline-content.align-bottom-right {
#     display: flex;
#     justify-content: flex-end;
#     align-items: flex-end;
#     text-align: right
# }
# .timeline-title {
#     text-align: center;
#     font-weight: bold;
#     margin-bottom: 8px;
#     font-size: 16px;                /* tamanho */
#     color: #0C2340;                 /* cor */
# }
# </style>
# """, unsafe_allow_html=True)

# def get_base64_image(image_path):
#     with open(image_path, "rb") as img_file:
#         encoded = base64.b64encode(img_file.read()).decode()
#         return f"data:image/png;base64,{encoded}"

# # Imagens da timeline
# image1 = get_base64_image(r'Timeline/África_ESTUDO DO MERCADO INTERNACIONAL DE GÁS NATURAL.png')
# image2 = get_base64_image(r'Timeline/América do Norte_ESTUDO DO MERCADO INTERNACIONAL DE GÁS NATURAL.png')
# image3 = get_base64_image(r'Timeline/América Latina_Estudo do Mercado Internacional - Gás Natural.png')
# image4 = get_base64_image(r'Timeline/Ásia_Estudo do Mercado Internacional - Gás Natural.png')
# image5 = get_base64_image(r'Timeline/Europa_Estudo do Mercado Internacional - Gás Natural.png')
# image6 = get_base64_image(r'Timeline/Mundo_Estudo do Mercado Internacional - Gás Natural.png')
# image7 = get_base64_image(r'Timeline/set-2016_Marco Regulatório Da Indústria Do Petróleo No México.png')
# image8 = get_base64_image(r'Timeline/Mundo_Boletim de Óleo e Gás.png')
# image9 = get_base64_image(r'Timeline/Bolívia_42887_Panorama da Indústria de Gás Natural na Bolívia.png')
# image10 = get_base64_image(r'Timeline/Nigéria_43101_Boletim de Conjuntura da Indústria do Óleo & Gás.png')

# # HTML da timeline


# cor_descricao_texto = '#1b232e'
# tipo_descricao_texto = 'normal'
# estilo_descricao_texto = 'italic'

# # <strong>texto aqui</strong> Tag para ficar em negrito
# # <u>texto aqui</u> Tag para ficar em sublinhado

# st.markdown(f"""
# <div class="timeline-container">
#   <div class="timeline-line"></div>

#   <!-- Bloco 1 -->
#   <div class="timeline-block">
#     <div class="timeline-content align-bottom-right">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#         Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Africano</strong>.
#       </span>
#     </div>
#     <div class="timeline-date">Jun/2013</div>
#     <div class="timeline-content">
#       <div class="timeline-title">Publicação Especial - África</div>
#       <a href="https://drive.google.com/file/d/1GedlRMVsvymqwFqevZB2emymQN4P76pu/view?usp=drive_link" target="_blank">
#         <img src="{image1}" class="timeline-img">
#       </a>
#     </div>
#   </div>

#   <!-- Bloco 2 -->
#   <div class="timeline-block">
#     <div class="timeline-content">
#       <div class="timeline-title">Publicação Especial - América do Norte</div>
#       <a href="https://drive.google.com/file/d/1gBcl_f6sGOrjvjcIQoYgIXWl5JZbRsp_/view?usp=drive_link" target="_blank">
#         <img src="{image2}" class="timeline-img">
#       </a>
#     </div>
#     <div class="timeline-date">Jun/2013</div>
#     <div class="timeline-content">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#       Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Norte Americano</strong>.
#       </span>
#     </div>
#   </div>

#   <!-- Bloco 3 -->
#   <div class="timeline-block">
#     <div class="timeline-content align-bottom-right">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#       Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Latino Americano</strong>.
#       </span>
#     </div>
#     <div class="timeline-date">Jun/2013</div>
#     <div class="timeline-content">
#       <div class="timeline-title">Publicação Especial - América Latina</div>
#       <a href="https://drive.google.com/file/d/1_fREydk0X-dOJ51qYnD3PU-0MVwDbgKA/view?usp=drive_link" target="_blank">
#         <img src="{image3}" class="timeline-img">
#       </a>
#     </div>
#   </div>

#   <!-- Bloco 4 -->
#   <div class="timeline-block">
#     <div class="timeline-content">
#       <div class="timeline-title">Publicação especial - Ásia</div>
#       <a href="https://drive.google.com/file/d/1XAZC-u05PBvhP6ZsNvkqV4_sBO4zgHW0/view?usp=drive_link" target="_blank">
#         <img src="{image4}" class="timeline-img">
#       </a>
#     </div>
#     <div class="timeline-date">Jun/2013</div>
#     <div class="timeline-content">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#       Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Asiático</strong>.
#       </span>
#     </div>
#   </div>

#   <!-- Bloco 5 -->
#   <div class="timeline-block">
#     <div class="timeline-content align-bottom-right">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#       Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Europeu</strong>.
#       </span>
#     </div>
#     <div class="timeline-date">Jun/2013</div>
#     <div class="timeline-content">
#       <div class="timeline-title">Publicação Especial - Europa</div>
#       <a href="https://drive.google.com/file/d/1SVf2mXHsOCMaNtRbNH-GTaSD7M7JTGLF/view?usp=drive_link" target="_blank">
#         <img src="{image5}" class="timeline-img">
#       </a>
#     </div>
#   </div>

#   <!-- Bloco 6 -->
#   <div class="timeline-block">
#     <div class="timeline-content">
#       <div class="timeline-title">Publicação Especial - Mundo</div>
#       <a href="https://drive.google.com/file/d/14Hrt6IB-RvLYkUIurLHtSNpjjhih4OA7/view?usp=drive_link" target="_blank">
#         <img src="{image6}" class="timeline-img">
#       </a>
#     </div>
#     <div class="timeline-date">Jun/2013</div>
#     <div class="timeline-content">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#        Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>Mundo</strong>.
#       </span>
#     </div>
#   </div>


#   <!-- Bloco 7 -->
#   <div class="timeline-block">
#     <div class="timeline-content align-bottom-right">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#       Marco regulatório da indústria do <strong> petróleo no México. </strong>
#       </span>
#     </div>
#     <div class="timeline-date">Set/2016</div>
#     <div class="timeline-content">
#       <div class="timeline-title">Nota Técnica - México</div>
#       <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-250/topico-306/NT_Mexico%202016set%5b1%5d.pdf" target="_blank">
#         <img src="{image7}" class="timeline-img">
#       </a>
#     </div>
#   </div>

#   <!-- Bloco 8 -->
#   <div class="timeline-block">
#     <div class="timeline-content">
#       <div class="timeline-title">Boletim de conjuntura da indústria de petróleo - Mundo</div>
#       <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-338/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo%20-%20n%C2%BA%201.pdf" target="_blank">
#         <img src="{image8}" class="timeline-img">
#       </a>
#     </div>
#     <div class="timeline-date">Dez/2016</div>
#     <div class="timeline-content">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#        Análise da <strong> indústria petrolífera mundial </strong>, retratando a evolução dos principais <u> indicadores econômicos e de produção </u>.
#       </span>
#     </div>
#   </div>

  
#   <!-- Bloco 9 -->
#   <div class="timeline-block">
#     <div class="timeline-content align-bottom-right">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#       Panorama da indústria de <u>gás natural</u> na <strong>Bolívia</strong>.
#       </span>
#     </div>
#     <div class="timeline-date">Jun/2017</div>
#     <div class="timeline-content">
#       <div class="timeline-title">Nota Técnica - Bolívia</div>
#       <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-250/topico-307/EPE%202017%20-%20Panorama%20da%20Ind%C3%BAstria%20de%20G%C3%A1s%20Natural%20na%20Bol%C3%ADvia%2022jun17.pdf" target="_blank">
#         <img src="{image9}" class="timeline-img">
#       </a>
#     </div>
#   </div>

#   <!-- Bloco 10 -->
#   <div class="timeline-block">
#     <div class="timeline-content">
#       <div class="timeline-title">Boletim de conjuntura da indústria de petróleo - Oeste da África</div>
#       <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-336/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo_2sem2017.pdf" target="_blank">
#         <img src="{image10}" class="timeline-img">
#       </a>
#     </div>
#     <div class="timeline-date">Dez/2017</div>
#     <div class="timeline-content">
#       <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
#        Analise do panorama do <strong>Oeste da África</strong>, região que se tornou relevante para o <strong>mercado mundial de petróleo</strong> em função de descobertas offshore em águas profundas, principalmente na <u>Angola e na Nigéria</u>.
#       </span>
#     </div>
#   </div>  

# </div>
# """, unsafe_allow_html=True)
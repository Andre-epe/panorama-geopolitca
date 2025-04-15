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

screen_size = st_javascript("window.innerWidth + ',' + window.innerHeight")
if screen_size:
    width, height = map(int, screen_size.split(','))
    # st.write(f"Largura: {width}, Altura: {height}")    ##No monitor é 1502


st.markdown(
    """
    <style>
        .block-container {
        
            padding-top: 1.5em;  ############## Botei em 1.8
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


# st.markdown("<h1 style='color: #0C2340;'>Panorama Geopolítico de Óleo, Gás e Biocombustíveis⛽</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color: #0C2340; font-size: 50px;'>Panorama Geopolítico de Óleo, Gás e Biocombustíveis⛽</h1>", unsafe_allow_html=True) #Fonte 42 no meu notebook; 50 no monitor


st.markdown(
    """<hr style="height: 2.4px; border: none; background-color: #7a7b7d; margin: -18px 0;">""", #### Na margin eu consegui juntar a linha do titulo
    unsafe_allow_html=True
)

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
        
        st.button('Modo Escuro', key='meu_botao_dark_mode', icon=":material/dark_mode:")

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
        
        st.button('Baixar Dados', key='meu_botao_baixar_dados', icon=":material/download:")

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


    lista_publicacoes = list(data_publications().loc[data_publications()['pais_ou_regiao']=='País', 'tipo'].unique())
    lista_publicacoes.append('Todas as publicações')
    publicacao_clicada = st.pills('Publicações disponíveis', 
            options= lista_publicacoes,
            default='Todas as publicações',
            selection_mode='single')

# st.write(publicacao_clicada) ############################################# VER MAIS TARDE ESSE PRINT COM O MULTISELECT ATIVADO PARA ST.PILLS ######################################3

world = data_countries()
regions = world['Região'].unique().tolist()
regions.append('Mundo')


# col1, col2, col3 = st.columns([1,4,1])
with st.sidebar:

    st.image('Logo-epe-negativa.png')

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
    a = "Selecione uma Região 🌏"
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
        location = [0,0]
        var_zoom=2
    elif selected_region == 'Ásia':
        location = [37,90]
        var_zoom=2.9
    elif selected_region == 'África':
        location = [5,20]
        var_zoom=3.3
    elif selected_region == 'Europa':
        location = [55,30]
        var_zoom=3.4
    elif selected_region == 'América do Sul e Central':
        location = [-20,-62]
        var_zoom=3.48
    elif selected_region == 'Antártica':
        location = [-50,0]
        var_zoom=2
    elif selected_region == 'Oceania':
        location = [-20,130]
        var_zoom=3.4
    elif 'América do Norte':
        location = [40,-90]
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
    map_data = st_folium(m, width=1200, height=780) # Na tela do monitor height = 780

    return map_data


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
    
    with st.container(key="minha_coluna3"):

        st.markdown(
        f"<div style='text-align: center; margin-top: 0;'><p style='font-size: 17px; font-family: \"Source Sans Pro\", sans-serif; font-weight: normal;'><span style='color: #636466;'>Região selecionada:</span> <span style='color: #0C2340; font-weight: bold;'>{selected_region}</span></p></div>",
        unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1,1], vertical_alignment='center')

        with col1:
            
            image_path = fr"Contornos\{selected_region}.png"
            img_base64 = get_image_base64(image_path)

            # Criando HTML para centralizar a imagem
            html_code = f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_base64}" width="150">
            """
            st.markdown(html_code, unsafe_allow_html=True)
        


        with col2:

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
            
            # CSS personalizado para o botão
            st.markdown("""
                <style>
                div.st-key-meu_botao {
                    display: flex;
                    justify-content: center; /* Centraliza o botão dentro do contêiner */
                }

                div.st-key-meu_botao button {
                    background-color: transparent !important;
                    color: #434445 !important;
                    border: 0px solid #7a7b7d !important;
                    display: flex;
                    align-items: center; /* Centraliza o conteúdo verticalmente */
                    justify-content: center; /* Centraliza o texto horizontalmente */
                    text-align: center; /* Centraliza o texto dentro do botão */
                    width: 100%; /* Garante alinhamento correto */
                }

                div.st-key-meu_botao button p {
                    font-size: 13px !important;
                    font-weight: bold;
                    line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                    margin: 0 auto !important; /* Garante centralização */
                    text-align: center !important; /* Centraliza o texto dentro do botão */
                }
                </style>
            """, unsafe_allow_html=True)

            def open_page(selected_region=selected_region):
                
                if selected_region == 'Ásia':
                    url = r"https://epegovbr-my.sharepoint.com/:b:/g/personal/andre_alves_epe_gov_br/EfR87f27gDhFke9zK9XF85IBrvRkTVqBvSupE5kBOVc2hQ?e=yTAder"
                elif selected_region == 'África':
                    url = r"https://epegovbr-my.sharepoint.com/:b:/g/personal/andre_alves_epe_gov_br/Ed5htFGdLOJHp6egflUbhBAB77i_G2iqW95CNFZkB5yQ2w?e=Rdpodk"
                elif selected_region == 'Europa':
                    url = r"https://epegovbr-my.sharepoint.com/:b:/g/personal/andre_alves_epe_gov_br/ETOVVmQ4vrBJkNpF1nL_pnwBotbZMbU__YN5uX7m8SOqRA?e=XuGQWp"
                elif selected_region == 'América do Sul e Central':
                    url = r"https://epegovbr-my.sharepoint.com/:b:/g/personal/andre_alves_epe_gov_br/ERNzfxH2QeJBm-27eusluO0Biq804uc1L7fJCS7zCvh5Ig?e=Ze5wM3"
                elif selected_region == 'América do Norte':
                    url = r"https://epegovbr-my.sharepoint.com/:b:/g/personal/andre_alves_epe_gov_br/EU595Ma4LKFAgAi1GcjI3HUBkfajL3JWFSPfhea3udVBlw?e=0zBnW6"
                elif selected_region == 'Mundo':
                    url = r"https://epegovbr-my.sharepoint.com/:b:/g/personal/andre_alves_epe_gov_br/EaeFtcWswDVAu3ItUKXBQOUBoaC0WbMVe3QJgf66iZUyMg?e=IakvQw"
                elif selected_region == 'Antártica':
                    return None
                elif selected_region == 'Oceania':
                    return None
                
                return webbrowser.open(url)

            titulo_botao = 'Estudo do Mercado Internacional de Gás Natural' if not (selected_region == 'Oceania' or selected_region == 'Antártica') else ''
            # Seu botão com uma key específica
            st.button(titulo_botao, 
                    key="meu_botao",
                    on_click=open_page)


            if selected_region == 'Mundo':
                st.markdown(
    """<hr style="height: 0.09px; border: none; background-color: #cccccf; margin: -0px 0;">""", #### Na margin eu consegui juntar a linha do titulo #7a7b7d
    unsafe_allow_html=True
            )
                    
                # Configurar a Imagem adicionada para representar o estudo
                st.markdown(
                    """
                    <div style="text-align: center; margin-bottom: -40px;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 40px;">📖</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                
                # CSS personalizado para o botão
                st.markdown("""
                    <style>
                    div.st-key-meu_botao2 button {
                        background-color: transparent !important;
                        color: #434445 !important;
                        border: 0px solid #ffffff !important;
                    }
                    
                    div.st-key-meu_botao2 button p {
                        font-size: 13px !important;
                        font-weight: bold;
                        line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                    }
                    </style>
                """, unsafe_allow_html=True)

                def open_page(selected_region=selected_region):
                    url = r'https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-338/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo%20-%20n%C2%BA%201.pdf'
                    return webbrowser.open(url)

                # Seu botão com uma key específica
                st.button('Boletim de Conjutura da Indústria de Petróleo', 
                        key="meu_botao2",
                        on_click=open_page)


    # st.write("")
    # st.write("")

    with st.container(key="minha_coluna4"):
        pais_clicado = pais_clicado()
        
        pais_clicado = 'Brasil' if (pais_clicado == None and selected_region == 'América do Sul e Central') else pais_clicado ####################################################### CORRIGIR ISSO BOTANDO POR ORDEM ALFABÉTICA ####################################################
        pais_clicado = 'Canadá' if (pais_clicado == None and selected_region == 'América do Norte') else pais_clicado
        pais_clicado = 'Irã' if (pais_clicado == None and selected_region == 'Ásia') else pais_clicado
        pais_clicado = 'República do Congo' if (pais_clicado == None and selected_region == 'África') else pais_clicado
        pais_clicado = 'Alemanha' if (pais_clicado == None and selected_region == 'Europa') else pais_clicado
        pais_clicado = 'Antártida' if (pais_clicado == None and selected_region == 'Antártica') else pais_clicado
        pais_clicado = 'Austrália' if (pais_clicado == None and selected_region == 'Oceania') else pais_clicado
        pais_clicado = 'Brasil' if (pais_clicado == None and selected_region == 'Mundo') else pais_clicado
        
        if (pais_clicado != 'Brasil') and (pais_clicado != 'Argentina'):
            st.write("")
            st.write("")
            st.write("")
            st.write("")

        st.markdown(
        f"<div style='text-align: center; margin-top: 0;'><p style='font-size: 17px; font-family: \"Source Sans Pro\", sans-serif; font-weight: normal;'><span style='color: #636466;'>País selecionado:</span> <span style='color: #0C2340; font-weight: bold;'>{pais_clicado}</span></p></div>",
        unsafe_allow_html=True
        )
    
        col1, col2 = st.columns([1,1], vertical_alignment='center')
        
        with col1:

            image_path = fr"Contornos\{pais_clicado}.png"
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
            publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['nome']==pais_clicado].copy()
            publicacoes_paises['edicao'] = pd.to_datetime(publicacoes_paises['edicao'], errors='coerce', format = r"%m/%Y")
            publicacoes_paises = publicacoes_paises.sort_values(by='edicao', ascending=True)
            publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['tipo']==publicacao_clicada] if not (publicacao_clicada == 'Todas as publicações') else publicacoes_paises
            publicacoes_paises = publicacoes_paises.reset_index(drop=True)
            lista_paises = publicacoes_paises['nome'].unique()
            

            def open_page_1(publicacoes_paises=publicacoes_paises):
                url = publicacoes_paises.loc[publicacoes_paises.index==0, 'url'].item()
                return webbrowser.open(url)
            
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
            figurinha_botao = '📑' if pais_clicado in lista_paises else ''
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: -40px;">
                    <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                    <span style="font-size: 40px;">{figurinha_botao}</span>
                </div>
                """, 
                unsafe_allow_html=True)
            

            # CSS personalizado para o botão
            st.markdown("""
                <style>
                div.st-key-meu_botao_pais {
                    display: flex;
                    justify-content: center; /* Centraliza o botão dentro do contêiner */
                }

                div.st-key-meu_botao_pais button {
                    background-color: transparent !important;
                    color: #434445 !important;
                    border: 0px solid #7a7b7d !important;
                    display: flex;
                    align-items: center; /* Centraliza o conteúdo verticalmente */
                    justify-content: center; /* Centraliza o texto horizontalmente */
                    text-align: center; /* Centraliza o texto dentro do botão */
                    width: 100%; /* Garante alinhamento correto */
                }

                div.st-key-meu_botao_pais button p {
                    font-size: 13px !important;
                    font-weight: bold;
                    line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                    margin: 0 auto !important; /* Garante centralização */
                    text-align: center !important; /* Centraliza o texto dentro do botão */
                }
                </style>
            """, unsafe_allow_html=True)


            # Seu botão com uma key específica
            st.button(titulo_botao, 
                    key="meu_botao_pais",
                    on_click=open_page_1)


            
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


                #📄📋
                # Configurar a Imagem adicionada para representar o estudo
                figurinha_botao = '🧾' if pais_clicado in lista_paises else ''
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: -40px;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 40px;">{figurinha_botao}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                

                # CSS personalizado para o botão
                st.markdown("""
                    <style>
                    div.st-key-meu_botao_pais2 {
                        display: flex;
                        justify-content: center; /* Centraliza o botão dentro do contêiner */
                    }

                    div.st-key-meu_botao_pais2 button {
                        background-color: transparent !important;
                        color: #434445 !important;
                        border: 0px solid #7a7b7d !important;
                        display: flex;
                        align-items: center; /* Centraliza o conteúdo verticalmente */
                        justify-content: center; /* Centraliza o texto horizontalmente */
                        text-align: center; /* Centraliza o texto dentro do botão */
                        width: 100%; /* Garante alinhamento correto */
                    }

                    div.st-key-meu_botao_pais2 button p {
                        font-size: 13px !important;
                        font-weight: bold;
                        line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                        margin: 0 auto !important; /* Garante centralização */
                        text-align: center !important; /* Centraliza o texto dentro do botão */
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Seu botão com uma key específica
                st.button(titulo_botao, 
                        key="meu_botao_pais2",
                        on_click=open_page_2)



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
                figurinha_botao = '📄' if pais_clicado in lista_paises else ''
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: -40px;">
                        <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                        <span style="font-size: 40px;">{figurinha_botao}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
                

                # CSS personalizado para o botão
                st.markdown("""
                    <style>
                    div.st-key-meu_botao_pais3 {
                        display: flex;
                        justify-content: center; /* Centraliza o botão dentro do contêiner */
                    }

                    div.st-key-meu_botao_pais3 button {
                        background-color: transparent !important;
                        color: #434445 !important;
                        border: 0px solid #7a7b7d !important;
                        display: flex;
                        align-items: center; /* Centraliza o conteúdo verticalmente */
                        justify-content: center; /* Centraliza o texto horizontalmente */
                        text-align: center; /* Centraliza o texto dentro do botão */
                        width: 100%; /* Garante alinhamento correto */
                    }

                    div.st-key-meu_botao_pais3 button p {
                        font-size: 13px !important;
                        font-weight: bold;
                        line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
                        margin: 0 auto !important; /* Garante centralização */
                        text-align: center !important; /* Centraliza o texto dentro do botão */
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Seu botão com uma key específica
                st.button(titulo_botao, 
                        key="meu_botao_pais3",
                        on_click=open_page_3)
        
        if (pais_clicado != 'Brasil') and (pais_clicado != 'Argentina'):
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





import pandas as pd
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static, st_folium
from shapely.geometry import Point
from data import data_countries, data_publications, data_timeline
import base64
from streamlit_javascript import st_javascript
import streamlit.components.v1 as components
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import streamlit.components.v1 as components
import locale

st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded")

from streamlit_cookies_manager import EncryptedCookieManager

#Variaveis em session state para alterar para dark mode
if not 'background_color' in st.session_state:
    st.session_state["background_color"] = "#EBEBF1"

if not 'title_color' in st.session_state:
    st.session_state["title_color"] = "#0C2340"


# # Detecta se está rodando na Streamlit Cloud
# is_streamlit_cloud = os.getenv('STREAMLIT_CLOUD') == 'true'

# if is_streamlit_cloud:
#     st.markdown("""
#         <style>
#         .appview-container .main {
#             transform: scale(0.75);  /* Ajuste o valor para seu zoom desejado */
#             transform-origin: top left;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    

# screen_size = st_javascript("window.innerWidth + ',' + window.innerHeight")
# if screen_size:
#     width, height = map(int, screen_size.split(','))
#     st.write(f"Largura: {width}, Altura: {height}")    #Monitor Largura: 1880; #Notebook Largura: 1496

#Customização das bordas
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.6em;
            padding-left: 1.0em;
            padding-right: 1.0em;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cor de fundo - #F0F2F6
st.html(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: {st.session_state["background_color"]};
}}
[data-testid="stHeader"] {{
    background-color: {st.session_state["background_color"]};
}}
</style>
""")

col1, col2 = st.columns([2.9,1])


with col1:
    # st.markdown("<h1 style='color: #0C2340;'>Panorama Geopolítico de Óleo, Gás e Biocombustíveis⛽</h1>", unsafe_allow_html=True)

    ###### TAVA 35PX
#     st.markdown(f"""
# <h1 style='color: {st.session_state["title_color"]}; font-size: 42px;'>
#     Panorama Geopolítico de Óleo, Gás e Biocombustíveis🌎
# </h1>
# """, unsafe_allow_html=True)

    st.markdown(f"""
<h1 style='
    color: {st.session_state["title_color"]};
    font-size: 2.1vw;
    line-height: 1.2;
    margin-bottom: 0.5em;
    margin-top: 0.4em;
'>
    Panorama Geopolítico de Óleo, Gás e Biocombustíveis🌎
</h1>
""", unsafe_allow_html=True)
    
#     st.markdown(
#     """<hr style="height: 2.4px; border: none; background-color: #7a7b7d; margin: -18px 0; width: 95%;">""", #### Na margin eu consegui juntar a linha do titulo
#     unsafe_allow_html=True
# )


with col2:
    # st.image('Logo Cinza.png')
    # st.write('')
    # st.write('')

    # st.markdown(
    #     "<div style='color:#0C2340; font-size: 14px; padding-left:30px;'><u><b>Avalie-nos!</b></u></div>",
    #     unsafe_allow_html=True
    # )
    # # sentiment_mapping = ["one", "two", "three", "four", "five"]
    # # feedback_estrelas = st.feedback("stars")


    
    col1_botao, col2_botao = st.columns([1,1])
    
    # ---------- CONFIGURAÇÃO DO COOKIE ----------
    cookies = EncryptedCookieManager(
        prefix="pangeo_",  # prefixo para isolar cookies do seu app
        password=st.secrets["cookie_password"]
    )

    # ⚠️ OBRIGATÓRIO: só continue se os cookies estiverem prontos
    if not cookies.ready():
        st.stop()

    # ---------- CONECTAR PLANILHA ----------
    @st.cache_resource
    def conectar_planilha():
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        return client.open("Feedback Pangeo").sheet1

    # ---------- REGISTRAR ACESSO ----------
    def registrar_acesso():
        try:
            sheet = conectar_planilha()
            registros = sheet.col_values(1)
            proxima_linha = len(registros) + 1

            data = [
                "False",  # Nome
                "False",  # Email
                "False",  # Feedback
                "False",  # Data Feedback
                "True",   # Acesso
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Data Acesso
            ]
            sheet.insert_row(data, index=proxima_linha)
            return proxima_linha
        except Exception as e:
            st.error(f"Erro ao registrar acesso: {e}")
            return None

    # ---------- SALVAR FEEDBACK ----------
    def salvar_feedback(linha, nome, email, feedback):
        if linha is None:
            st.error("Linha inválida para salvar feedback.")
            return
        try:
            sheet = conectar_planilha()
            nome = nome.strip() if nome.strip() else "False"
            email = email.strip() if email.strip() else "False"

            valores = [
                [nome, email, feedback, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            sheet.update(f"A{linha}:D{linha}", valores)
        except Exception as e:
            st.error(f"Erro ao salvar feedback: {e}")

    # ---------- LÓGICA DE ACESSO DIÁRIO POR COOKIE ----------
    hoje = date.today().isoformat()

    if "linha_acesso" not in st.session_state:
        if cookies.get("ultimo_acesso", None) != hoje:
            linha = registrar_acesso()
            if linha is not None:
                cookies["ultimo_acesso"] = hoje
                cookies.save()  # salva no navegador
                st.session_state.linha_acesso = linha
            else:
                st.session_state.linha_acesso = None
        else:
            st.session_state.linha_acesso = None

    with col1_botao:

        # ---------- DIÁLOGO DE FEEDBACK ----------
        @st.dialog("Forneça um feedback detalhado!")
        def feedback_mensagem():
            st.markdown("Envie um feedback detalhado com dúvidas, sugestões ou críticas para continuarmos melhorando o Mapa Pangeo! 👋")
            name = st.text_input("Qual o seu nome (opcional)?")
            email = st.text_input("Qual o seu email (opcional)?")
            feedback_texto = st.text_area("Escreva o seu feedback!")

            if st.button("Enviar"):
                if feedback_texto.strip() == "":
                    st.warning("Por favor, escreva um feedback antes de enviar.")
                else:
                    try:
                        if st.session_state.linha_acesso:
                            salvar_feedback(st.session_state.linha_acesso, name, email, feedback_texto)
                        else:
                            # Usuário já acessou hoje, registra nova linha só para o feedback
                            linha = registrar_acesso()
                            salvar_feedback(linha, name, email, feedback_texto)
                            st.session_state.linha_acesso = linha  # atualiza estado para possíveis próximos feedbacks
                        st.success("Obrigado pelo seu feedback! 💙")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao registrar feedback: {e}. Recarregue a página e tente novamente.")

        # CSS personalizado para o botão de feedback e dark mode
        st.markdown(
            f"""
            <style>
                /* Container dos botões - ajuste fino de posição */
                div.st-key-meu_botao_feedback, 
                div.st-key-botao_dark_mode1 {{
                    display: flex;
                    transform: translateY(20px);  /* Move apenas os botões para baixo */
                    margin-bottom: -20px;        /* Compensa o espaço criado */
                }}

                /* Estilo original dos botões */
                div.st-key-meu_botao_feedback button, 
                div.st-key-botao_dark_mode1 button {{
                    background-color: transparent !important;
                    color: #0C2340 !important;
                    border: 1px solid #0C2340 !important;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    width: 100%;
                    height: 100%;
                    padding: 0 !important;
                    font-family: "Source Sans Pro", sans-serif !important;
                    transition: all 0.3s ease;
                }}

                /* EFEITO HOVER */
                div.st-key-meu_botao_feedback button:hover, 
                div.st-key-botao_dark_mode1 button:hover {{
                    background-color: #0C2340 !important;
                    color: white !important;
                    cursor: pointer;
                }}

                /* Estilo do texto */
                div.st-key-meu_botao_feedback button p, 
                div.st-key-botao_dark_mode1 button p {{
                    font-size: 12px !important;
                    font-weight: bold !important;
                    line-height: 1.1 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    width: 100%;
                    text-align: center !important;
                    font-family: "Source Sans Pro", sans-serif !important;
                }}

                div.st-key-meu_botao_feedback button span, 
                div.st-key-botao_dark_mode1 button span {{
                    flex-grow: 1;
                    text-align: center;
                    display: block;
                    font-family: "Source Sans Pro", sans-serif !important;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )




        if not 'chave_botao_feedback' in st.session_state:
            st.session_state['chave_botao_feedback'] = 'meu_botao_feedback'

        if st.button('💭Forneça um feedback!', key=st.session_state['chave_botao_feedback']):
            feedback_mensagem()

    with col2_botao:

        if not 'botao_dark_mode' in st.session_state:
            st.session_state['botao_dark_mode'] = True
    
        if not 'tiles' in st.session_state:
            st.session_state["tiles"] = "CartoDB Positron"
        if not 'sidebar_color' in st.session_state:
            st.session_state['sidebar_color'] = "#0C2340"
        if not 'title_tabs' in st.session_state:
            st.session_state['title_tabs'] = "#0C2340"
        if not 'title_pills' in st.session_state:
            st.session_state['title_pills'] = "#0C2340"
        if not 'descricao_mapa' in st.session_state:
            st.session_state['descricao_mapa'] = "#333"
        if not 'title_card_regiao_1' in st.session_state:
            st.session_state['title_card_regiao_1'] = "#636466"
        if not 'title_card_regiao_2' in st.session_state:
            st.session_state['title_card_regiao_2'] = "#0C2340"
        if not 'title_card_pais_1' in st.session_state:
            st.session_state['title_card_pais_1'] = "#636466"
        if not 'title_card_pais_2' in st.session_state:
            st.session_state['title_card_pais_2'] = "#0C2340"
        if not 'publicacao_card_regiao_1' in st.session_state:
            st.session_state['publicacao_card_regiao_1'] = "#31333f"
        if not 'publicacao_card_regiao_2' in st.session_state:
            st.session_state['publicacao_card_regiao_2'] =  "#31333f"
        if not 'file_card_regiao_1' in st.session_state: ######### Mudou em todos os nomes das publicações, provavelmente devido ao !important da linha 886
            st.session_state['file_card_regiao_1'] = '#434445'
        if not 'publicacao_card_pais' in st.session_state:
            st.session_state['publicacao_card_pais'] = '#555'
        if not 'color_st_radio' in st.session_state:
            st.session_state['color_st_radio'] =  "#FFFFFF"
        if not 'color_st_pills' in st.session_state:
            st.session_state['color_st_pills'] = "#b8c0d5"
        if not 'color_descricao_SDB' in st.session_state:
            st.session_state['color_descricao_SDB'] = "#FFFFFF"
        if not 'color_title_timeline' in st.session_state:
            st.session_state['color_title_timeline'] = '#0C2340'
        if not 'dark_mode_contornos' in st.session_state:
            st.session_state['dark_mode_contornos'] = ''


        st.markdown(
            f"""
            <style>
                /* Aplica o mesmo estilo para DOIS botões com chaves diferentes */
                div.st-key-meu_botao_feedback_darkmode, 
                div.st-key-botao_clear_mode {{
                    display: flex;
                    transform: translateY(20px);  /* Movimento vertical (ajuste o valor) */
                    margin-bottom: -20px;        /* Compensação do espaço */
                }}

                div.st-key-meu_botao_feedback_darkmode button, 
                div.st-key-botao_clear_mode button {{
                    background-color: transparent !important;
                    color: #CED3D8 !important;
                    border: 1px solid #CED3D8 !important;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    width: 100%;
                    height: 100%;
                    padding: 0 !important;
                    font-family: "Source Sans Pro", sans-serif !important;
                    transition: all 0.3s ease;
                }}

                /* EFEITO HOVER */
                div.st-key-meu_botao_feedback_darkmode button:hover, 
                div.st-key-botao_clear_mode button:hover {{
                    background-color: #0C2340 !important;
                    color: white !important;
                    cursor: pointer;
                }}

                div.st-key-meu_botao_feedback_darkmode button p, 
                div.st-key-botao_clear_mode button p {{
                    font-size: 12px !important;
                    font-weight: bold !important;
                    line-height: 1.1 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    width: 100%;
                    text-align: center !important;
                    font-family: "Source Sans Pro", sans-serif !important;
                }}

                div.st-key-meu_botao_feedback_darkmode button span, 
                div.st-key-botao_clear_mode button span {{
                    flex-grow: 1;
                    text-align: center;
                    display: block;
                    font-family: "Source Sans Pro", sans-serif !important;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
            
        if st.session_state['botao_dark_mode']:
            # st.write("")
            
            botao_dark_mode = st.button('🌙 Modo Escuro', key='botao_dark_mode1')
            if botao_dark_mode:
                st.session_state["tiles"] = "cartodbdark_matter"
                st.session_state["background_color"] = "#181a1f"
                st.session_state["title_color"] = "#CED3D8"
                st.session_state['sidebar_color'] = "#121317ff"
                st.session_state['title_tabs'] = "#CED3D8"
                st.session_state['title_pills'] = "#CED3D8"
                st.session_state['descricao_mapa'] = "#CED3D8"
                st.session_state['title_card_regiao_1'] = "#CED3D8"
                st.session_state['title_card_regiao_2'] = "#CED3D8"
                st.session_state['title_card_pais_1'] = "#CED3D8"
                st.session_state['title_card_pais_2'] = "#CED3D8"
                st.session_state['publicacao_card_regiao_1'] = "#CED3D8"
                st.session_state['publicacao_card_regiao_2'] =  "#CED3D8"
                st.session_state['file_card_regiao_1'] = "#CED3D8"
                st.session_state['publicacao_card_pais'] = "#CED3D8"
                st.session_state['color_st_radio'] = "#CED3D8"
                st.session_state['color_st_pills'] = "#7d808d"
                st.session_state['color_descricao_SDB'] = "#CED3D8"
                st.session_state['color_title_timeline'] = "#CED3D8"
                st.session_state['dark_mode_contornos'] = '_dark_mode'

                st.session_state['botao_dark_mode'] = False
                st.session_state['chave_botao_feedback'] = "meu_botao_feedback_darkmode"
        
        else:
            # st.write('')

            botao_clear_mode = st.button('☀️Modo Claro', 
                                        #  icon=":material/light_mode:",
                                           key='botao_clear_mode')
            if botao_clear_mode:
                st.session_state["tiles"] = "CartoDB Positron"
                st.session_state["background_color"] = "#F0F2F6"
                st.session_state["title_color"] = "#0C2340"
                st.session_state['sidebar_color'] = "#0C2340"
                st.session_state['title_tabs'] = "#0C2340"
                st.session_state['title_pills'] = "#0C2340"
                st.session_state['descricao_mapa'] = "#333"
                st.session_state['title_card_regiao_1'] = "#636466"
                st.session_state['title_card_regiao_2'] = "#0C2340"
                st.session_state['title_card_pais_1'] = "#636466"
                st.session_state['title_card_pais_2'] = "#0C2340"
                st.session_state['publicacao_card_regiao_1'] = "#31333f"
                st.session_state['publicacao_card_regiao_2'] =  "#31333f"
                st.session_state['file_card_regiao_1'] = '#434445'
                st.session_state['publicacao_card_pais'] = '#555'
                st.session_state['color_st_radio'] =  "#FFFFFF"
                st.session_state['color_st_pills'] = "#b8c0d5"
                st.session_state['color_descricao_SDB'] = "#FFFFFF"
                st.session_state['color_title_timeline'] = '#0C2340'
                st.session_state['dark_mode_contornos'] = ''

                st.session_state['botao_dark_mode'] = True
                st.session_state['chave_botao_feedback'] = 'meu_botao_feedback'


# st.markdown(
#     "<h1 style='color: #9ea0a3; font-size: 30px; font-weight: normal;'>Mapa PANGEO</h1>",
#     unsafe_allow_html=True
# )

# Configurar a cor do tab
st.markdown(f"""
    <style>
    .stTabs [role="tab"] * {{
        font-size: {"16px"} !important;
        font-weight: {"bold"} !important;  /* ou bold / 400 / 700 */
        color: {st.session_state['title_tabs']} !important;
    }}
    </style>
""", unsafe_allow_html=True)



tab1, tab2 = st.tabs(["🌐 Mapa PanGeo","📅 Histórico de Publicações"])

with tab1:

    col1, col2 = st.columns([5,1])


    with col2:
        pass

        # col3, col4 = st.columns([1,1])
        # with col3:
        #     # CSS personalizado para o botão
        #     st.markdown("""
        #         <style>
        #         div.st-key-meu_botao_dark_mode {
        #             display: flex;
        #             justify-content: center; /* Centraliza o botão dentro do contêiner */
        #         }

        #         div.st-key-meu_botao_dark_mode button {
        #             background-color: transparent !important;
        #             color: #434445 !important;
        #             border: 1px solid #7a7b7d !important;
        #             display: flex;
        #             align-items: center; /* Centraliza o conteúdo verticalmente */
        #             justify-content: center; /* Centraliza o texto horizontalmente */
        #             text-align: center; /* Centraliza o texto dentro do botão */
        #             width: 100%; /* Garante alinhamento correto */
        #         }

        #         div.st-key-meu_botao_dark_mode button p {
        #             font-size: 12px !important;
        #             font-weight: bold;
        #             line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
        #             margin: 0 auto !important; /* Garante centralização */
        #             text-align: center !important; /* Centraliza o texto dentro do botão */
        #         }
        #         </style>
        #     """, unsafe_allow_html=True)
            
        #     st.button('Modo Escuro', key='meu_botao_dark_mode', icon=":material/dark_mode:")

        # with col4:

        #     # CSS personalizado para o botão
        #     st.markdown("""
        #         <style>
        #         div.st-key-meu_botao_baixar_dados {
        #             display: flex;
        #             justify-content: center; /* Centraliza o botão dentro do contêiner */
        #         }

        #         div.st-key-meu_botao_baixar_dados button {
        #             background-color: transparent !important;
        #             color: #434445 !important;
        #             border: 1px solid #7a7b7d !important;
        #             display: flex;
        #             align-items: center; /* Centraliza o conteúdo verticalmente */
        #             justify-content: center; /* Centraliza o texto horizontalmente */
        #             text-align: center; /* Centraliza o texto dentro do botão */
        #             width: 100%; /* Garante alinhamento correto */
        #         }

        #         div.st-key-meu_botao_baixar_dados button p {
        #             font-size: 12px !important;
        #             font-weight: bold;
        #             line-height: 1.1 !important; /* Reduz o espaçamento entre linhas */
        #             margin: 0 auto !important; /* Garante centralização */
        #             text-align: center !important; /* Centraliza o texto dentro do botão */
        #         }
        #         </style>
        #     """, unsafe_allow_html=True)
            
        #     st.button('Baixar Dados', key='meu_botao_baixar_dados', icon=":material/download:")

    with col1:

        # Configuração das cores do st.pills
        st.markdown(
            f"""
            <style>
            /* Estilo para o botão ativo */
            button[data-testid="stBaseButton-pillsActive"] {{
                background-color: #0C2340 !important;
                color: white !important;
                border: none !important;
                font-weight: normal !important;
            }}

            /* Estilo para os botões inativos */
            button[data-testid="stBaseButton-pills"] {{
                background-color: {st.session_state['color_st_pills']} !important;
                color: black !important;
                border: 2px solid #ccc !important;
                font-weight: bold !important;
            }}

            /* Hover para os inativos */
            button[data-testid="stBaseButton-pills"]:hover {{
                background-color: #e0e0e0 !important;
                color: black !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )




        

        st.markdown(
            f"""<h3 style='margin-top: 5px; margin-bottom: -200px; font-size: 15px; color: {st.session_state['title_pills']};'><u>Publicações disponíveis</u></h3>""",
            unsafe_allow_html=True
        )


        
        lista_publicacoes = list(data_publications().loc[data_publications()['pais_ou_regiao']=='País', 'tipo'].unique())
        lista_publicacoes.append('Todas as publicações')
        publicacao_clicada = st.pills(
                label = '', 
                options= lista_publicacoes,
                default='Todas as publicações',
                selection_mode='single',
                # help='Ajuda'
                )
        
        

    # st.write(publicacao_clicada) ############################################# VER MAIS TARDE ESSE PRINT COM O MULTISELECT ATIVADO PARA ST.PILLS ######################################3

    world = data_countries()
    regions = world['Região'].unique().tolist()
    regions.append('Mundo')


    # col1, col2, col3 = st.columns([1,4,1])
    with st.sidebar:

        # Código para subir o logo EPE
        st.markdown("""
            <style>
            /* Remove todo o padding/margin do container da sidebar */
            section[data-testid="stSidebar"] {
                padding-top: 0px !important;
                margin-top: -60px !important;
            }

            /* Remove o header oculto da sidebar (normalmente reserva altura) */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            /* Remove o padding interno do conteúdo da sidebar */
            [data-testid="stSidebar"] > div {
                padding-top: 0px !important;
            }

            /* Garante que nada desça a imagem com margem */
            [data-testid="stImage"] {
                margin-top: 0px !important;
            }
            </style>
        """, unsafe_allow_html=True)


        st.image('Logo-epe-negativa.png')

        # CSS customizado para mudar a largura da sidebar
        st.markdown(
            """
            <style>
            /* Força a largura menor da sidebar */
            [data-testid="stSidebar"] {
                width: 220px !important;
                min-width: 220px !important;
            }
            [data-testid="stSidebarContent"] {
                width: 220px !important;
                min-width: 220px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")
        st.write("")
        st.write("")

        # Alterar a cor de fundo da st.sidebar
        st.html(f"""
            <style>
            [data-testid="stSidebarContent"] {{
                background-color: {st.session_state['sidebar_color']};
                color: {"white"}; /* Para melhor contraste com o fundo escuro */
            }}

            /* Para alterar também a cor dos elementos de navegação */
            [data-testid="stSidebarNav"] span {{
                color: {"white"};
            }}
            </style>
        """)


        a = "Selecione uma Região 📌"
        cor_hex = st.session_state['color_st_radio']  # Exemplo de cor HEX

        # Exibindo a expressão LaTeX com cor HEX
        latex_expression = fr'$\normalsize' + f' \\textsf{{\\textcolor{{{cor_hex}}}{{{a}}}}}$'

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
        
        # Descrição da SDB
        st.markdown(
            f"""
            <style>
            .sidebar-footer {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 210px; /* Ajuste conforme necessário */
                padding: 10px;
                text-align: left;
                background-color: rgba(0, 0, 0, 0); /* Leve transparência */
                color: {st.session_state['color_descricao_SDB']};
                font-size: 10px;
            }}
            </style>
            <div class="sidebar-footer">
                📌 Superintendência de Derivados de Petróleo e Biocombustíveis/<b>DPG</b><br>
                📧 Contato: <i>SDB@epe.gov.br</i>
            </div>
            """,
            unsafe_allow_html=True
        )


    def zoom_region_map(selected_region=selected_region):
        if selected_region == 'Mundo':
            location = [20,75]
            var_zoom=1.5
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
            location = [-20,-35]
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
    publicacoes_paises_pintado_mundo = publicacoes_paises_pintado if publicacao_clicada=='Todas as publicações' else publicacoes_paises_pintado.loc[publicacoes_paises_pintado['tipo']==publicacao_clicada].copy()
    selected_country = publicacoes_paises_pintado_filtrado['nome'].unique() if selected_region != 'Mundo' else publicacoes_paises_pintado_mundo['nome'].unique() #obter a lista de países depois das filtragens

    # color = st.color_picker("Escolha uma cor", "#ff0000")
    color = "#ff0000"



    def mapa_mundi(location=location, var_zoom=var_zoom):
        # Mantenha seu CSS original aqui
        st.markdown("""
            <style>
            iframe {
                margin-bottom: -20px !important;
                padding-bottom: 20px !important;
                display: block;
                border: none !important;
            }
            .element-container {
                padding-bottom: 0px !important;
                margin-bottom: 0px !important;
            }
            .stDeployButton {
                display: none;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Criar o mapa
        m = folium.Map(location, zoom_start=var_zoom, tiles=st.session_state["tiles"])
        
        # Adicionar camada de países
        for _, row in world.iterrows():
            # Criar feature GeoJSON com propriedades
            feature = {
                "type": "Feature",
                "geometry": row['Geometria'].__geo_interface__,
                "properties": {
                    "pais_traduzido": row['País Traduzido'],
                    "is_selected": row['País Traduzido'] in selected_country
                }
            }
            
            # Determinar estilos baseados na seleção
            style = {
                'fillColor': '#0C2340' if feature['properties']['is_selected'] else None,
                'color': "#91A1B7" if feature['properties']['is_selected'] else "#6a6a6b",
                'weight': 1.3 if feature['properties']['is_selected'] else 1,
                'fillOpacity': 0.9 if feature['properties']['is_selected'] else 0.05,
            }
            
            highlight = {
                'fillColor': "#030817" if feature['properties']['is_selected'] else "#D0D2D7",
                'color': '#ffffff',
                'weight': 2,
                'fillOpacity': 0.9
            }
            
            # Criar o GeoJson
            folium.GeoJson(
                feature,
                name=row['País Traduzido'],
                tooltip=folium.GeoJsonTooltip(
                    fields=['pais_traduzido'],
                    aliases=[''],
                    localize=True
                ),
                style_function=lambda x, style=style: style,
                highlight_function=lambda x, highlight=highlight: highlight
            ).add_to(m)
        
        # Configuração para capturar cliques
        # m.add_child(folium.LatLngPopup())
        
        # Exibir o mapa
        map_data = st_folium(
            m,
            width=1200,
            height=700,
            returned_objects=["last_clicked"],
            key="world_map"
        )
        
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
        if st.session_state.get("world_map") and st.session_state["world_map"].get("last_clicked"):
            click_data = st.session_state["world_map"]["last_clicked"]
            clicked_point = Point(click_data['lng'], click_data['lat'])
            
            # Encontrar o país clicado
            for _, row in world.iterrows():
                if row['Geometria'].contains(clicked_point):
                    return row['País Traduzido']
        return None

    def get_image_base64(image_path):
        """Converte a imagem para base64."""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")


    st.markdown(
        f"""
        <span style='font-size:16px; font-style:italic; color:{st.session_state['descricao_mapa']};'>
            <span style='font-style: normal;'>💡</span>
            <u>Clique no mapa</u> para selecionar o <b>País de interesse!</b>
        </span>
        """,
        unsafe_allow_html=True
    )



    col1, col2 = st.columns([1.8,1], vertical_alignment='top') #antes era 2.05,1


    with col1:

        # Configuração inicial
        if 'world_map' not in st.session_state:
            st.session_state['world_map'] = None


        map_data = mapa_mundi()
        
    # Adição do fundo cinza na coluna lateral direita de cima #e4e6eb
    st.markdown(
        """
        <style>
        div.st-key-minha_coluna3 {
            background-color: transparent;
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
            background-color: transparent;
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


            # if pais_clicado_mapa != 'Brasil':
            #     st.write("")
            #     st.write("")
            #     st.write("")
        
            #Título do cartão da Região Selecionada
            bg_color = "transparent"         # Cor de fundo
            label_color = st.session_state['title_card_regiao_1'] # Cor do texto fixo
            value_color = st.session_state['title_card_regiao_2']  # Cor do valor
            font_size = "clamp(12px, 2.5vw, 16px)"            # Tamanho da fonte
            padding = "10px"              # Espaçamento interno
            border_radius = "8px"         # Arredondamento da borda

            st.markdown(
                f"""
                <div style='
                    text-align: center;
                    margin-top: 0;
                    background-color: {bg_color};
                    padding: {padding};
                    border-radius: {border_radius};
                '>
                    <p style='
                        font-size: {font_size};
                        font-family: "Source Sans Pro", sans-serif;
                        font-weight: normal;
                        margin: 0;
                    '>
                        <span style='color: {label_color};'>Região selecionada:</span>
                        <span style='color: {value_color}; font-weight: bold;'>{selected_region}</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([1,1], vertical_alignment='center')

            with col1:

                image_path = fr"Contornos/{selected_region}{st.session_state['dark_mode_contornos']}.png"
                img_base64 = get_image_base64(image_path)
                
                st.markdown(
                    f"""
                    <div style="
                        padding-top: 0em;
                        padding-left: 0em;
                        padding-right: 0em;
                        border-radius: 10px;
                        text-align: center;
                    ">
                        <img src="data:image/png;base64,{img_base64}" style="max-width: 250px; max-height: 250px; width: auto; height: auto;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    

                # # Criando HTML para centralizar a imagem
                # html_code = f"""
                # <div style="display: flex; justify-content: center;">
                #     <img src="data:image/png;base64,{img_base64}" width="150">
                # """
                # st.markdown(html_code, unsafe_allow_html=True)
            


            with col2:

                #Colocar a data de publicação da publicação acima da imagem
                if selected_region not in ['Oceania', 'Antártica']:
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: -35px;">
                            <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                            <span style="font-size: 10px; color: {st.session_state['publicacao_card_regiao_1']};">
                                Publicação: Junho/2013
                            </span>
                        </div>
                    """, unsafe_allow_html=True)

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
                        'Ásia': "https://1drv.ms/b/c/c11d7baa08fee88d/EfTkxOhi7SBMl90KsV7KU3cByIhrqf-Nieh33c0sApUYWw?e=yVTIkO",
                        'África': "https://1drv.ms/b/c/c11d7baa08fee88d/EfkwWRmAL6dHt4P4foEaZBwBtqP6UpEXRLrBCY7q4p0fcw?e=F7GsQx",
                        'Europa': "https://1drv.ms/b/c/c11d7baa08fee88d/EaN0cIWgU3JJvvrVoEMHdoYBZxTSPgQVLo5qt-0w0uYMBA?e=En49sW",
                        'América do Sul e Central': "https://1drv.ms/b/c/c11d7baa08fee88d/EUK59r0ulptLt6e_qsKxitUBPvZrL10l5xak38R8xcKTDQ?e=ODazQY",
                        'América do Norte': "https://1drv.ms/b/c/c11d7baa08fee88d/EVQMLIhjOhhPqTgzYxY5JaQBJ1imzXSBho3zGB1R_bEH7g?e=dDyG9D",
                        'Mundo': "https://1drv.ms/b/c/c11d7baa08fee88d/ESJW-oJ7UXlIj50IfH_3k6UB8fPUhmS0-emQEiDQOI_5vA?e=XBze86"
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
                            color: {st.session_state['file_card_regiao_1']}!important;
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
        """<hr style="height: 0.09px; border: none; background-color: #cccccf; width: 70%; margin-left: auto; margin-right: auto; margin-top: 0; margin-bottom: 0;">""", #### Na margin eu consegui juntar a linha do titulo #7a7b7d
        unsafe_allow_html=True
                )
                    

                    #Colocar a data de publicação da publicação acima da imagem
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: -35px;">
                            <!-- IMPORTANTE: Aproximei a imagem unicode do texto abaixo botando margem negativa acima -->
                            <span style="font-size: 10px; color: {st.session_state['publicacao_card_regiao_2']};">
                                Publicação: Junho/2016
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                        
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
            'Mundo': "https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-338/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo%20-%20n%C2%BA%201.pdf"}
                    
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
                                    Boletim de Conjuntura da Indústria de Petróleo
                                </a>
                            </div>
                        """, unsafe_allow_html=True)


            if (selected_region == 'Ásia') or (selected_region=='Europa') or (selected_region=='Antártica') or (selected_region=='Oceania') or (selected_region=='América do Norte'):
                st.write("")
                st.write("")
                st.write("")
                st.write("")
            elif (selected_region == 'Mundo') and (pais_clicado_mapa == 'Brasil'):
                pass
            elif (selected_region == 'Mundo'):
                st.write("")
        

        # st.write("")
        # st.write("")

        # Linha entre as colunas 7a7b7d
        st.markdown(
        """<hr style="height: 2.4px; border: none; background-color: #818b99; margin: 0px 0; width: 95%;">""", #### Na margin eu consegui juntar a linha do titulo
        unsafe_allow_html=True)

        with st.container(key="minha_coluna4"):
            
            if (selected_region == 'Ásia') or (selected_region=='Europa') or (selected_region=='Antártica') or (selected_region=='Oceania') or (selected_region=='América do Norte'):
                st.write("")
                st.write("")
                # st.write("")
            elif (selected_region == 'Mundo') and (pais_clicado_mapa == 'Brasil'):
                pass
            elif (selected_region == 'Mundo'):
                st.write("")

            #Título do cartão do País selecionado
            bg_color = "transparent"          # Cor de fundo
            label_color = st.session_state['title_card_pais_1'] # Cor do texto fixo
            value_color = st.session_state['title_card_pais_2'] # Cor do valor
            font_size = "clamp(12px, 2.5vw, 16px)"   # Tamanho da fonte
            padding = "10px"              # Espaçamento interno
            border_radius = "8px"         # Arredondamento da borda

            st.markdown(
                f"""
                <div style='
                    text-align: center;
                    margin-top: 0;
                    background-color: {bg_color};
                    padding: {padding};
                    border-radius: {border_radius};
                '>
                    <p style='
                        font-size: {font_size};
                        font-family: "Source Sans Pro", sans-serif;
                        font-weight: normal;
                        margin: 0;
                    '>
                        <span style='color: {label_color};'>País selecionado:</span>
                        <span style='color: {value_color}; font-weight: bold;'>{pais_clicado_mapa}</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if (pais_clicado_mapa != 'Brasil') and (pais_clicado_mapa != 'Argentina'):
                st.write("")

        
            col1, col2 = st.columns([1,1], vertical_alignment='center')
            
            with col1:

                image_path = fr"Contornos/{pais_clicado_mapa}{st.session_state['dark_mode_contornos']}.png"
                img_base64 = get_image_base64(image_path)

                st.markdown(
                    f"""
                    <div style="
                        padding-top: 0em;
                        padding-left: 0em;
                        padding-right: 0em;
                        border-radius: 10px;
                        text-align: center;
                    ">
                        <img src="data:image/png;base64,{img_base64}" style="max-width: 250px; max-height: 200px; width: auto; height: auto;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # # Criando HTML para centralizar a imagem
                # html_code = f"""
                # <div style="display: flex; justify-content: center;">
                #     <img src="data:image/png;base64,{img_base64}" width="150">
                # """

                # st.markdown(html_code, unsafe_allow_html=True)
                
                st.write("")
                
            with col2:

                publicacoes_paises = data_publications()
                publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['pais_ou_regiao']=='País'].copy()
                publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['nome']==pais_clicado_mapa].copy()
                publicacoes_paises['data'] = pd.to_datetime(publicacoes_paises['data'], errors='coerce', format = "%d/%m/%Y")
                publicacoes_paises = publicacoes_paises.sort_values(by='data', ascending=False)
                publicacoes_paises = publicacoes_paises.loc[publicacoes_paises['tipo']==publicacao_clicada] if not (publicacao_clicada == 'Todas as publicações') else publicacoes_paises
                publicacoes_paises = publicacoes_paises.reset_index(drop=True)
                lista_paises = publicacoes_paises['nome'].unique()
                

                ##########
                #  1° publicação #############
                
                try:
                    titulo_botao = publicacoes_paises.loc[publicacoes_paises.index==0, 'nome_publicação'].item()
                except ValueError:
                    titulo_botao = ''

                try:
                    data_publicacao_botao = publicacoes_paises.loc[publicacoes_paises.index==0, 'data_publicacao'].item()
                    # data_publicacao_botao = data_publicacao_botao.strip('Publicação: ')
                except ValueError:
                    data_publicacao_botao = ''

                # HTML dinâmico para colocar as publicações por país
                html_content = f"""
                            <style>
                            .two-columns {{
                            display: flex;
                            gap: 0px;  /* Tiramos o gap, vamos controlar o espaço via bordas */
                            margin-bottom: 0px;
                            border-bottom: 1px solid #ccc;  /* Linha horizontal entre fileiras */
                            }}

                            .two-columns:last-child {{
                            border-bottom: none;  /* Remove a linha horizontal após o último grupo */
                            }}

                            .column {{
                            flex: 1;
                            padding: 6px;
                            background-color: transparent;
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                            border-left: 1px solid #ccc;
                            border-right: 1px solid #ccc;
                            border-top: 0px solid #ccc;
                            }}

                            .column:first-child {{
                            border-left: none;  /* Remove a borda esquerda da primeira coluna */
                            }}

                            .column:last-child {{
                            border-right: none;  /* Remove a borda direita da última coluna */
                            }}

                            .two-columns:first-child .column {{
                            border-top: none !important;  /* Remove a borda superior da primeira linha */
                            }}

                            .column p {{
                            margin: 2px 0;
                            padding: 0;
                            }}

                            .custom-button {{
                            background-color: transparent;
                            color: #434445 !important;
                            border: 0px solid #7a7b7d;
                            font-size: 12px !important;
                            font-weight: bold;
                            line-height: 1.1;
                            padding: 0.3rem 0.6rem;
                            cursor: pointer;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            }}

                            .custom-button:hover {{
                            text-decoration: underline;
                            }}

                            .button-container {{
                            display: flex;
                            justify-content: center;
                            margin-top: 3px;
                            margin-bottom: 0px;
                            }}

                            .data-publicacao {{
                            font-size: 10px !important;
                            text-align: center;
                            color: {st.session_state['publicacao_card_pais']};
                            margin-bottom: 3px;
                            }}

                            .figurinha {{
                            font-size: 30px !important;
                            text-align: center;
                            color: #FF5733;
                            margin-bottom: 3px;
                            }}
                            </style>
                            """

                # Montar os blocos em pares de duas colunas
                for i in range(0, len(publicacoes_paises), 2):
                    html_content += '<div class="two-columns">'

                    for j in range(2):
                        index = i + j
                        if index < len(publicacoes_paises):
                            row = publicacoes_paises.iloc[index]
                            data_publicacao_botao = row['data_publicacao']
                            figurinha_botao = "📑"
                            url = row['url']
                            titulo_botao = row['nome_publicação']

                            html_content += f"""
                            <div class="column">
                                <p class="data-publicacao">{data_publicacao_botao}</p>
                                <p class="figurinha">{figurinha_botao}</p>
                                <div class="button-container">
                                    <a href="{url}" target="_blank" class="custom-button">{titulo_botao}</a>
                                </div>
                            </div>
                            """

                    html_content += '</div>'

                st.markdown(html_content, unsafe_allow_html=True)

                    
            
            # if (pais_clicado_mapa != 'Brasil') and (pais_clicado_mapa != 'Argentina'):
            #     st.write("")
            #     st.write("")
            #     st.write("")
            #     st.write("")





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




with tab2:

    # Título da página
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <h1 style='color: {st.session_state['color_title_timeline']}; font-size: 23px; font-weight: bold;'>
                Histórico de Publicações do Panorama Geopolítico
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )


    dados_timeline = data_timeline()
    dados_timeline = dados_timeline.loc[(dados_timeline['descricao'].isna()==False) & (dados_timeline['imagem'].isna()==False)].copy()
    dados_timeline = dados_timeline.loc[dados_timeline.duplicated(subset='url')==False].copy()
    
    # ---------- Função para converter imagem em base64 ----------
    def get_base64_image(image_path):
        with open(image_path.strip().strip('"'), "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"

    # ---------- HTML + CSS atualizado ----------
    timeline_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    html, body {
        overflow-x: hidden;
        margin: 0;
        padding: 0;
        font-family: "Segoe UI", "Helvetica Neue", sans-serif;
        background: transparent;
        color: #1b232e;
        scroll-behavior: smooth;
    }

    .timeline-container {
        position: relative;
        margin: 50px auto;
        width: 95%;
        max-width: 1000px;
        padding: 30px 10px;
    }

    .timeline-line {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 1px;
        height: 100%;
        background: repeating-linear-gradient(
            to bottom,
            #ccc,
            #ccc 8px,
            transparent 8px,
            transparent 16px
        );
        z-index: 0;
    }

    .timeline-block {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 60px 0;
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.6s ease both;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .timeline-date {
        background: white;
        border: 2px solid #304878;
        color: #304878;
        font-weight: bold;
        font-size: 14px;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        line-height: 80px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }

    .timeline-date:hover {
        transform: scale(1.05);
        background: #f2f4f8;
    }

    .timeline-content {
        width: 40%;
        background: rgba(255, 255, 255, 0.88);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }

    .timeline-content:hover {
        transform: translateY(-4px);
    }

    .timeline-image-box {
        width: 40%;
        padding: 20px;
        background: transparent;
        border-radius: 12px;
    }

    .timeline-img {
        width: 100%;
        max-width: 220px;
        height: auto;
        border-radius: 8px;
        display: block;
        margin: 0 auto;
        transition: transform 0.3s ease;
    }

    .timeline-img:hover {
        transform: scale(1.03);
    }

    .timeline-content.align-bottom-right {
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        text-align: right;
    }

    .timeline-title {
        text-align: center;
        font-weight: bold;
        margin-bottom: 12px;
        font-size: 17px;
        color: #0C2340;
    }

    /* RESPONSIVO */
    @media (max-width: 768px) {
        .timeline-block {
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .timeline-content, .timeline-image-box {
            width: 90%;
            margin-bottom: 20px;
        }

        .timeline-date {
            margin: 20px 0;
        }

        .timeline-content.align-bottom-right {
            justify-content: center;
            align-items: center;
            text-align: center;
        }
    }

    /* BOTÃO VOLTAR AO TOPO */
    #top-button {
        position: fixed;
        bottom: 20px;
        right: 30px;
        z-index: 99;
        background-color: #304878;
        color: white;
        border: none;
        border-radius: 40px;
        padding: 12px 18px;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    #top-button.show {
        opacity: 1;
    }
    #top-button:hover {
        background-color: #1d2f4a;
    }
    </style>
    </head>
    <body>
    <div id="top"></div>
    <div class="timeline-container">
        <div class="timeline-line"></div>
    """
    

    # ---------- Definir o locale para português brasileiro ----------
    locales_to_try = ['pt_BR.UTF-8', 'pt_BR', 'Portuguese_Brazil.1252']
    for loc in locales_to_try:
        try:
            locale.setlocale(locale.LC_TIME, loc)
            break
        except locale.Error:
            continue

    # ---------- Dicionário com meses abreviados em português ----------
    meses_abreviados = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }

    # ---------- Formatar a data usando o mapeamento manual ----------
    dados_timeline['data'] = pd.to_datetime(dados_timeline['data'])
    dados_timeline['data'] = dados_timeline['data'].apply(lambda x: f"{meses_abreviados[x.month]}/{x.year}")

    # ---------- Loop usando o DataFrame ----------
    for i, row in dados_timeline.iterrows():
        direita = (i % 2 == 0)
        alinhamento_classe = "align-bottom-right" if direita else ""

        imagem_base64 = get_base64_image(row['imagem'])

        descricao_html = f"""
        <div class="timeline-content {alinhamento_classe}">
            <span style="font-weight: normal; font-style: italic; color: #1b232e;">
                {row['descricao']}
            </span>
        </div>
        """

        imagem_html = f"""
        <div class="timeline-content">
            <div class="timeline-title">{row['tipo']}</div>
            <a href="{row['url']}" target="_blank">
                <img src="{imagem_base64}" class="timeline-img">
            </a>
        </div>
        """

        timeline_html += f"""
        <div class="timeline-block">
            {descricao_html if direita else imagem_html}
            <div class="timeline-date">{row['data']}</div>
            {imagem_html if direita else descricao_html}
        </div>
        """

    timeline_html += """
    </div>

    </body>
    </html>
    """

    # ---------- Renderização no Streamlit ----------
    components.html(timeline_html, height=9500, scrolling=False)
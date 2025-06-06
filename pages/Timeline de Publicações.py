import streamlit as st
import base64
from streamlit_javascript import st_javascript
from data import data_countries

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
    st.image('Logo Cinza.png')




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




# Título da página
st.markdown(
    "<div style='text-align: center;'>"
    "<h1 style='color: #434345; font-size: 23px; font-weight: bold;'>Timeline das Publicações do Panorama Geopolítico</h1>"
    "</div>",
    unsafe_allow_html=True
)

# Estilos
st.markdown("""
<style>
.timeline-container {
    position: relative;
    margin: 50px auto;
    width: 90%;
    max-width: 900px;
}
.timeline-line {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    height: 100%;
    background: repeating-linear-gradient(
        to bottom,
        #7a7b7d,
        #7a7b7d 10px,
        transparent 10px,
        transparent 20px
    );
    z-index: 0;
}
.timeline-block {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 40px 0;
    position: relative;
    z-index: 1;
}
.timeline-date {
    background: #F0F2F6;
    border: 2px solid #7a7b7d;
    color: #7a7b7d;
    font-weight: normal;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    line-height: 80px;
    text-align: center;
    z-index: 2;
}
.timeline-content {
    width: 40%;
    background: transparent;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 0px 0px rgba(0,0,0,0.1);
}
.timeline-img {
    width: 70%;
    max-width: 200px;
    height: auto;
    border-radius: 8px;
    display: block;
    margin: 0 auto;
}
.timeline-content.align-bottom-right {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    text-align: right
}
.timeline-title {
    text-align: center;
    font-weight: bold;
    margin-bottom: 8px;
    font-size: 16px;                /* tamanho */
    color: #0C2340;                 /* cor */
}
</style>
""", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{encoded}"

# Imagens da timeline
image1 = get_base64_image(r'Timeline/África_ESTUDO DO MERCADO INTERNACIONAL DE GÁS NATURAL.png')
image2 = get_base64_image(r'Timeline/América do Norte_ESTUDO DO MERCADO INTERNACIONAL DE GÁS NATURAL.png')
image3 = get_base64_image(r'Timeline/América Latina_Estudo do Mercado Internacional - Gás Natural.png')
image4 = get_base64_image(r'Timeline/Ásia_Estudo do Mercado Internacional - Gás Natural.png')
image5 = get_base64_image(r'Timeline/Europa_Estudo do Mercado Internacional - Gás Natural.png')
image6 = get_base64_image(r'Timeline/Mundo_Estudo do Mercado Internacional - Gás Natural.png')
image7 = get_base64_image(r'Timeline/set-2016_Marco Regulatório Da Indústria Do Petróleo No México.png')
image8 = get_base64_image(r'Timeline/Mundo_Boletim de Óleo e Gás.png')
image9 = get_base64_image(r'Timeline/Bolívia_42887_Panorama da Indústria de Gás Natural na Bolívia.png')
image10 = get_base64_image(r'Timeline/Nigéria_43101_Boletim de Conjuntura da Indústria do Óleo & Gás.png')
image11 = get_base64_image(r'Timeline/Rússia_43282_Boletim de Conjuntura da Indústria do Óleo & Gás.png')
image12 = get_base64_image(r'Timeline/Brasil_43405_Recent Developments In The Brazilian Oil Industry.png')
image13 = get_base64_image(r'Timeline/Venezuela_43466_Boletim de Conjuntura da Indústria do Óleo & Gás.png')
image14 = get_base64_image(r'Timeline/Argentina_43647_Boletim de Conjuntura da Indústria do Óleo & Gás.png')
image15 = get_base64_image(r'Timeline/Brasil_43800_Brazilian Oil & Gas Report 2019-2020.png')
image16 = get_base64_image(r'Timeline/Argentina_43983_A Indústria de Gás Natural na Argentina.png')

# HTML da timeline


cor_descricao_texto = '#1b232e'
tipo_descricao_texto = 'normal'
estilo_descricao_texto = 'italic'

# <strong>texto aqui</strong> Tag para ficar em negrito
# <u>texto aqui</u> Tag para ficar em sublinhado

st.markdown(f"""
<div class="timeline-container">
  <div class="timeline-line"></div>

  <!-- Bloco 1 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
        Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Africano</strong>.
      </span>
    </div>
    <div class="timeline-date">Jun/2013</div>
    <div class="timeline-content">
      <div class="timeline-title">Publicação Especial - África</div>
      <a href="https://drive.google.com/file/d/1GedlRMVsvymqwFqevZB2emymQN4P76pu/view?usp=drive_link" target="_blank">
        <img src="{image1}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 2 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Publicação Especial - América do Norte</div>
      <a href="https://drive.google.com/file/d/1gBcl_f6sGOrjvjcIQoYgIXWl5JZbRsp_/view?usp=drive_link" target="_blank">
        <img src="{image2}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Jun/2013</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Norte Americano</strong>.
      </span>
    </div>
  </div>

  <!-- Bloco 3 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Latino Americano</strong>.
      </span>
    </div>
    <div class="timeline-date">Jun/2013</div>
    <div class="timeline-content">
      <div class="timeline-title">Publicação Especial - América Latina</div>
      <a href="https://drive.google.com/file/d/1_fREydk0X-dOJ51qYnD3PU-0MVwDbgKA/view?usp=drive_link" target="_blank">
        <img src="{image3}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 4 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Publicação especial - Ásia</div>
      <a href="https://drive.google.com/file/d/1XAZC-u05PBvhP6ZsNvkqV4_sBO4zgHW0/view?usp=drive_link" target="_blank">
        <img src="{image4}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Jun/2013</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Asiático</strong>.
      </span>
    </div>
  </div>

  <!-- Bloco 5 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>continente Europeu</strong>.
      </span>
    </div>
    <div class="timeline-date">Jun/2013</div>
    <div class="timeline-content">
      <div class="timeline-title">Publicação Especial - Europa</div>
      <a href="https://drive.google.com/file/d/1SVf2mXHsOCMaNtRbNH-GTaSD7M7JTGLF/view?usp=drive_link" target="_blank">
        <img src="{image5}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 6 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Publicação Especial - Mundo</div>
      <a href="https://drive.google.com/file/d/14Hrt6IB-RvLYkUIurLHtSNpjjhih4OA7/view?usp=drive_link" target="_blank">
        <img src="{image6}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Jun/2013</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
       Diagnóstico sobre o balanço de oferta e demanda de <u>gás natural</u> para o <strong>Mundo</strong>.
      </span>
    </div>
  </div>


  <!-- Bloco 7 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Marco regulatório da indústria do <strong> petróleo no México. </strong>
      </span>
    </div>
    <div class="timeline-date">Set/2016</div>
    <div class="timeline-content">
      <div class="timeline-title">Nota Técnica - México</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-250/topico-306/NT_Mexico%202016set%5b1%5d.pdf" target="_blank">
        <img src="{image7}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 8 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Boletim de conjuntura da indústria de petróleo - Mundo</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-338/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo%20-%20n%C2%BA%201.pdf" target="_blank">
        <img src="{image8}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Dez/2016</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
       Análise da <strong> indústria petrolífera mundial </strong>, retratando a evolução dos principais <u> indicadores econômicos e de produção </u>.
      </span>
    </div>
  </div>

  
  <!-- Bloco 9 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Panorama da indústria de <u>gás natural</u> na <strong>Bolívia</strong>.
      </span>
    </div>
    <div class="timeline-date">Jun/2017</div>
    <div class="timeline-content">
      <div class="timeline-title">Nota Técnica - Bolívia</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-250/topico-307/EPE%202017%20-%20Panorama%20da%20Ind%C3%BAstria%20de%20G%C3%A1s%20Natural%20na%20Bol%C3%ADvia%2022jun17.pdf" target="_blank">
        <img src="{image9}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 10 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Boletim de conjuntura da indústria de petróleo - Oeste da África</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-336/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo_2sem2017.pdf" target="_blank">
        <img src="{image10}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Dez/2017</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
       Analise do panorama do <strong>Oeste da África</strong>, região que se tornou relevante para o <strong>mercado mundial de petróleo</strong> em função de descobertas offshore em águas profundas, principalmente na <u>Angola e na Nigéria</u>.
      </span>
    </div>
  </div>  

  
  <!-- Bloco 11 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Análise do <strong>Panorama da Rússia</strong>, <u>maior exportador mundial de petróleo e de gás natural</u>, e detentor da <u>maior reserva global de gás natural e da sexta maior de petróleo</u>.
      </span>
    </div>
    <div class="timeline-date">Jun/2018</div>
    <div class="timeline-content">
      <div class="timeline-title">Boletim de Conjuntura da Indústria do Óleo & Gás - Rússia</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-399/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo_1sem2018_07_04.pdf" target="_blank">
        <img src="{image11}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 12 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Recent developments in the Brazilian oil industry - Brasil</div>
      <a href="https://www.epe.gov.br/sites-en/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-189/English%20ROG_v%20final_2018.11.01.pdf" target="_blank">
        <img src="{image12}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Nov/2018</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
       Publicação anual para apresentar as <strong>tendências e os desenvolvimentos do setor nos últimos meses no Brasil</strong>. O relatório esclarece as causas das <u>flutuações nos preços</u>, <u>na produção</u>, <u>no comércio</u> e <u>na demanda</u>.
      </span>
    </div>
  </div>

  
  <!-- Bloco 13 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Análise do <strong>panorama da Venezuela</strong>. Detentor da maior reserva global de petróleo, este país enfrentou uma <u>expressiva queda da produção devido às dificuldades enfrentadas pela indústria</u>. A instabilidade político-econômica é um desafio a ser solucionado.
      </span>
    </div>
    <div class="timeline-date">Dez/2018</div>
    <div class="timeline-content">
      <div class="timeline-title">Boletim de Conjuntura da Indústria do Óleo & Gás - Venezuela</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-450/Boletim%20de%20Conjuntura%20da%20Ind%C3%BAstria%20do%20Petr%C3%B3leo_2019_01_04.pdf" target="_blank">
        <img src="{image13}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 14 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">Boletim de Conjuntura da Indústria do Óleo & Gás - Argentina</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-226/topico-471/Boletim%20de%20Conjuntura%20da%20Indu%CC%81stria%20do%20Petro%CC%81leo_1S19_2019_07_04_final.pdf" target="_blank">
        <img src="{image14}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Jun/2019</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
        A <strong>Argentina</strong> foi o destaque da seção Panorama. As <u>descobertas de reservas não convencionais de elevado potencial</u>, a <u>demanda regional de hidrocarbonetos</u> e a <u>movimentação de leilões de blocos exploratórios</u> representam perspectivas promissoras para a indústria petrolífera.
      </span>
    </div>
  </div>


  <!-- Bloco 15 -->
  <div class="timeline-block">
    <div class="timeline-content align-bottom-right">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
      Apesar de um ambiente desafiador no mercado internacional, a <strong> indústria de petróleo e gás do Brasil </strong> continua no caminho para alcançar seu potencial de se tornar um <u>importante player global</u>.
      </span>
    </div>
    <div class="timeline-date">Dez/2020</div>
    <div class="timeline-content">
      <div class="timeline-title">Brazilian oil & gas report - Brasil</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-448/topico-565/EPE_Brazilian%20Oil%20and%20Gas%20Report%202019-2020.pdf" target="_blank">
        <img src="{image15}" class="timeline-img">
      </a>
    </div>
  </div>

  <!-- Bloco 16 -->
  <div class="timeline-block">
    <div class="timeline-content">
      <div class="timeline-title">A indústria de gás natural na Argentina</div>
      <a href="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-492/Nota%20Tecnica%20A%20Industria%20Gas%20Natural%20na%20Argentina_Panorama%20perspectivas%20e%20oportunidades%20para%20o%20Brasil_DPG_SPG.pdf" target="_blank">
        <img src="{image16}" class="timeline-img">
      </a>
    </div>
    <div class="timeline-date">Jul/2020</div>
    <div class="timeline-content">
      <span style="font-weight: {tipo_descricao_texto}; font-style: {estilo_descricao_texto}; color: {cor_descricao_texto};">
        Panorama, perspectivas e oportunidades para o <strong>Brasil</strong>.
      </span>
    </div>
  </div>

  
</div>
""", unsafe_allow_html=True)
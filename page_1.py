import streamlit as st
import base64

def app():
    # Título da página
    st.markdown(
        "<div style='text-align: center;'>"
        "<h1 style='color: #0C2340; font-size: 24px;'>Timeline das Publicações do Panorama Geopolítico</h1>"
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
        font-size: 18px;                /* tamanho */
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

    </div>
    """, unsafe_allow_html=True)

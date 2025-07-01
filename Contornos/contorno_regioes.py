import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

world = gpd.read_file("dados_paises.geojson")


def gerar_contorno_regiao(region, world = world, salvar=False, nome_arquivo="contorno.png"):    
    
    regiao = world.loc[world['Região']==region]
    # regiao=world #Para gerar o contorno do Mundo
    if regiao.empty:
        print("País não encontrado! Verifique o nome.")
        return

    fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')

    
    regiao.plot(ax=ax, color="#1E569B", edgecolor='none')
    # #0C2340 cor azul padrão
    # '#1E569B' cor usada no clear mode
    # "#337EDB" cor usada no dark mode

    # Remover eixos para parecer uma imagem isolada
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor('none')  # Fundo do gráfico transparente

    if salvar:
        plt.savefig(nome_arquivo, dpi=300, transparent=True, bbox_inches='tight')  # Salvar com fundo transparente
        print(f"Imagem salva como {nome_arquivo}")
    plt.show()




gerar_contorno_regiao(region='Oceania', salvar=True, nome_arquivo="Oceania.png")

# gerar_contorno_regiao(region='América do Sul e Central', salvar=True, nome_arquivo="Mundo_dark_mode.png")

regioes = world['Região'].unique()
for regiao in regioes:
    gerar_contorno_regiao(regiao, salvar=True, nome_arquivo=f"{regiao}{'_dark_mode'}.png")
    





# Converter arquivo PGN para png


import os

def converter_extensao_para_minuscula(caminho_arquivo):
    # Separa o diretório, nome e extensão
    pasta, nome_arquivo = os.path.split(caminho_arquivo)
    nome_base, extensao = os.path.splitext(nome_arquivo)

    # Verifica se a extensão está em maiúscula
    if extensao.isupper():
        nova_extensao = extensao.lower()
        novo_nome = nome_base + nova_extensao
        novo_caminho = os.path.join(pasta, novo_nome)

        # Renomeia o arquivo
        os.rename(caminho_arquivo, novo_caminho)
        print(f"Arquivo renomeado para: {novo_caminho}")
        return novo_caminho
    else:
        print("A extensão já está em minúscula. Nenhuma ação necessária.")
        return caminho_arquivo


converter_extensao_para_minuscula(r'C:\Users\andre.alves\OneDrive - epe.gov.br\Área de Trabalho\Mapa PANGEO\Mapa PANGEO\Contornos\Oceania.PNG')
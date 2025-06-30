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

    
    regiao.plot(ax=ax, color="#337EDB", edgecolor='none')
    # #0C2340 cor azul padrão
    # '#1E569B' cor usada no clear mode
    # '#265dab' cor usada no dark mode

    # Remover eixos para parecer uma imagem isolada
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor('none')  # Fundo do gráfico transparente

    if salvar:
        plt.savefig(nome_arquivo, dpi=300, transparent=True, bbox_inches='tight')  # Salvar com fundo transparente
        print(f"Imagem salva como {nome_arquivo}")
    plt.show()




gerar_contorno_regiao(region='América do Sul e Central', salvar=False, nome_arquivo="brasil_contorno.png")

# gerar_contorno_regiao(region='América do Sul e Central', salvar=True, nome_arquivo="Mundo_dark_mode.png")

regioes = world['Região'].unique()
for regiao in regioes:
    gerar_contorno_regiao(regiao, salvar=True, nome_arquivo=f"{regiao}{'_dark_mode'}.png")
    




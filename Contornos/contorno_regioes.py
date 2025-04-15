import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

world = gpd.read_file("dados_paises.geojson")


def gerar_contorno_regiao(region, world = world, salvar=False, nome_arquivo="contorno.png"):    
    
    regiao = world.loc[world['Região']==region]
    
    if regiao.empty:
        print("País não encontrado! Verifique o nome.")
        return

    fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')

    
    regiao.plot(ax=ax, color='#FF8200', edgecolor='none')
    # #0C2340
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


regioes = world['Região'].unique()
for regiao in regioes:
    gerar_contorno_regiao(regiao, salvar=True, nome_arquivo=f"{regiao}.png")
    



df = pd.DataFrame({1:['a'], 2:['b']})

df.to_csv()

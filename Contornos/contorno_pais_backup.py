import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

def gerar_contorno_pais(nome_pais, salvar=False, nome_arquivo="contorno.png"):
    # Baixar os dados dos países
    world = gpd.read_file(r"dados_paises.geojson")

    # Filtrar o país desejado
    pais = world[world['País Traduzido'] == nome_pais]

    
    if pais.empty:
        print("País não encontrado! Verifique o nome.")
        return
    
    # Criar a figura com fundo transparente
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')

    # Plotar o país preenchido e sem bordas
    pais.plot(ax=ax, color='#FFB81C', edgecolor='none')
    # #515152
    # Remover eixos para parecer uma imagem isolada
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor('none')  # Fundo do gráfico transparente

    if salvar:
        plt.savefig(nome_arquivo, dpi=300, transparent=True, bbox_inches='tight')  # Salvar com fundo transparente
        print(f"Imagem salva como {nome_arquivo}")

    # Mostrar a imagem
    plt.show()
    

# Exemplo: Gerar o contorno do Brasil com fundo transparente
gerar_contorno_pais("Finlândia", salvar=False, nome_arquivo="brasil_contorno.png")


world = gpd.read_file(r"dados_paises.geojson")

paises = world['País Traduzido'].to_list()

for pais in paises:
    gerar_contorno_pais(pais, salvar=True, nome_arquivo=f"{pais}.png")

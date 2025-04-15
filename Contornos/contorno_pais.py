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
    
    # Definir DPI e altura fixa
    dpi = 300
    altura_pixels = 1446
    altura_inches = altura_pixels / dpi
    
    # Calcular a largura dinamicamente para manter a proporção
    bounds = pais.total_bounds
    largura_geografica = bounds[2] - bounds[0]
    altura_geografica = bounds[3] - bounds[1]
    proporcao = largura_geografica / altura_geografica
    largura_inches = altura_inches * proporcao
    
    # Criar figura com altura fixa e largura variável
    fig, ax = plt.subplots(figsize=(largura_inches, altura_inches), dpi=dpi, facecolor='none')

    # Ajustar limites do eixo para ocupar toda a altura
    ax.set_ylim(bounds[1], bounds[3])
    
    # Calcular margens laterais para centralizar o país horizontalmente
    centro_x = (bounds[0] + bounds[2]) / 2
    largura_alvo = altura_geografica * proporcao  # Largura ajustada para manter proporção
    ax.set_xlim(centro_x - largura_alvo / 2, centro_x + largura_alvo / 2)
    
    # Plotar o país preenchido e sem bordas
    pais.plot(ax=ax, color='#FFB81C', edgecolor='none')
    
    # Remover eixos para parecer uma imagem isolada
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor('none')  # Fundo do gráfico transparente

    if salvar:
        plt.savefig(nome_arquivo, dpi=dpi, transparent=True, pad_inches=0, bbox_inches='tight')  # Garantir que a imagem ocupe todo o espaço
        print(f"Imagem salva como {nome_arquivo}")

    # Mostrar a imagem
    plt.show()

# Exemplo: Gerar o contorno do Brasil com fundo transparente
gerar_contorno_pais("Finlândia", salvar=False, nome_arquivo="brasil_contorno.png")


world = gpd.read_file(r"dados_paises.geojson")

paises = world['País Traduzido'].to_list()

for pais in paises:
    gerar_contorno_pais(pais, salvar=True, nome_arquivo=f"{pais}.png")

    
    
    
    
    
    
    
    

from PIL import Image
import os

# Caminho da pasta com as imagens
pasta_imagens = r'C:\Users\andre.alves\Desktop\Mapa PANGEO\Contornos'

# Largura desejada para todas as imagens
largura_padrao = 800

# Iterar sobre todas as imagens na pasta
for arquivo in os.listdir(pasta_imagens):
    if arquivo.endswith('.png'):
        # Caminho completo da imagem
        caminho_imagem = os.path.join(pasta_imagens, arquivo)
        
        # Abrir a imagem
        try:
            imagem = Image.open(caminho_imagem)
            
            # Obter a altura original
            altura_original = imagem.height
            
            # Redimensionar a imagem, esticando apenas a largura
            imagem_redimensionada = imagem.resize((largura_padrao, altura_original))
            
            # Salvar a imagem redimensionada com o mesmo nome
            imagem_redimensionada.save(caminho_imagem)
        except Exception as e:
            print(f"Erro ao processar a imagem {arquivo}: {e}")

print("Redimensionamento concluído!")
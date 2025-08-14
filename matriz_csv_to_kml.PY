import pandas as pd

# Importando funções dos módulos organizados
from calculo_geografico import distance, angle, polar, distance_ptos, angulo_deflexao
from processamento_vertices import get_loose_gap, dividir_tramo, intercalar_vertices
from abaco_mosaico import mtz_abaco, point_in_polygon, mosaico
from exportacao import exportar_para_kml, salvar_csv
from kml import criar_kml_quadrados_bissetriz
from colocar_encabecamento_rede import colocar_encabecamento_rede
from colocar_poste_estrutura import colocar_poste_estrutura
from marcar_vertices_angulo_deflexao import marcar_vertices_angulo_deflexao

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste", "estrutura_mt", "estrutura_mt_nv2", "estrutura_mt_nv3", "estrutura_bt", "estrutura_bt_nv2", "poste", "base_reforcada", "base", "rotacao_poste"])
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)

    new_vertices = dividir_tramo(new_vertices, section_size)

    # Aplica marcação SIM baseada no ângulo de deflexão
    new_vertices = marcar_vertices_angulo_deflexao(new_vertices, gap_size, module_name)

    # Aplica encabeçamento automático baseado na distância
    new_vertices = colocar_encabecamento_rede(new_vertices, section_size)

    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)

    # Carrega o arquivo matriz_teste.csv
    matriz_teste = pd.read_csv("matriz_teste.csv", sep=";", decimal=",")
    
    # Filtra apenas as linhas com status "Implantar" e prepara os dados para a função KML
    matriz_teste_filtrada = matriz_teste[matriz_teste['status'] == 'Implantar'].copy()
    
    # Renomeia as colunas para o formato esperado pela função KML
    matriz_teste_filtrada = matriz_teste_filtrada.rename(columns={
        'lat': 'lat',
        'long': 'long',
        'num_poste': 'numero_poste',
        'tipo_poste': 'poste',  # tipo_poste vai para o campo poste
        'estru_mt_nv1': 'estrutura_mt',
        'estru_mt_nv2': 'estrutura_mt_nv2',
        'estru_mt_nv3': 'estrutura_mt_nv3',
        'est_bt_nv1': 'estrutura_bt',
        'est_bt_nv2': 'estrutura_bt_nv2',
        'base_reforcada': 'base_reforcada',  # mantém o nome original
        'base_concreto': 'base',
        'rotacao_poste': 'rotacao_poste'  # adiciona o campo de rotação
    })
    
    # Garante que todas as colunas necessárias existem
    colunas_necessarias = ['lat', 'long', 'numero_poste', 'poste', 'estrutura_mt', 'estrutura_mt_nv2', 'estrutura_mt_nv3', 'estrutura_bt', 'estrutura_bt_nv2', 'base_reforcada', 'base', 'rotacao_poste']
    for coluna in colunas_necessarias:
        if coluna not in matriz_teste_filtrada.columns:
            matriz_teste_filtrada[coluna] = ''

    #pontos_matriz = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)

    # Nota: criar_kml_quadrados_bissetriz será chamada na função main
    
    # Adiciona os dados da matriz de pontos ao DataFrame
    for i, vertex in enumerate(new_vertices):
        # Busca dados correspondentes na matriz_teste_filtrada baseado na sequência
        dados_ponto = {}
        if i < len(matriz_teste_filtrada):
            row = matriz_teste_filtrada.iloc[i]
            dados_ponto = {
                "estrutura_mt": str(row.get("estrutura_mt", "")),
                "estrutura_mt_nv2": str(row.get("estrutura_mt_nv2", "")),
                "estrutura_mt_nv3": str(row.get("estrutura_mt_nv3", "")),
                "estrutura_bt": str(row.get("estrutura_bt", "")),
                "estrutura_bt_nv2": str(row.get("estrutura_bt_nv2", "")),
                "poste": str(row.get("poste", "")),
                "base_reforcada": str(row.get("base_reforcada", "")),
                "base": str(row.get("base", "")),
                "rotacao_poste": str(row.get("rotacao_poste", ""))
            }
        
        new_row = {
            "trecho": trecho,
            "sequencia": i,
            "lat": f"{vertex[0]:.9f}".replace(".", ","),
            "long": f"{vertex[1]:.9f}".replace(".", ","),
            "numero_poste": num_poste_inicial if i == 0 else "",
            "tipo_poste": tipo_poste if i == 0 else "",
            "estrutura_mt": dados_ponto.get("estrutura_mt", ""),
            "estrutura_mt_nv2": dados_ponto.get("estrutura_mt_nv2", ""),
            "estrutura_mt_nv3": dados_ponto.get("estrutura_mt_nv3", ""),
            "estrutura_bt": dados_ponto.get("estrutura_bt", ""),
            "estrutura_bt_nv2": dados_ponto.get("estrutura_bt_nv2", ""),
            "poste": dados_ponto.get("poste", ""),
            "base_reforcada": dados_ponto.get("base_reforcada", ""),
            "base": dados_ponto.get("base", ""),
            "rotacao_poste": dados_ponto.get("rotacao_poste", "")
        }
        matriz.loc[len(matriz)] = new_row
    return matriz

##################################################################################################################################
def main():
    trecho = "T1"
    module_name = "MT7"
    module_data = ["MT10", 100, "SIM"]
    loose_gap = "SIM"
    section_size = 500
    gap_size = 80
    num_poste_inicial = "2255555"
    tipo_poste = "EXISTENTE"
    lista_nao_intercalar = [2, 4] 

    vertices = [
        (-17.041935, -49.224541, 1, ""), #0
        (-17.045514, -49.217512, 2, ""), #2
        (-17.047802, -49.214406, 3, ""), #3
        (-17.047725, -49.213698, 4, ""), #4
        (-17.046803, -49.213231, 5, ""), #5
        (-17.045692, -49.212772, 6, ""), #6
        (-17.043834, -49.213044, 7, ""), #7
        (-17.042247, -49.213750, 8, ""), #8
        (-17.037641, -49.214581, 9, ""), #9
        (-17.036451, -49.217405, 10, "") #10

        #lat, lon,sequencia original vertice, encabecamento, 
    ]                          
    matriz = gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar)

    # Salva o arquivo CSV na pasta resultados
    salvar_csv(matriz, "matriz_resultado.csv")
    
    # Exporta os pontos para KML na pasta resultados
    print("\n=== Exportando para KML ===")
    exportar_para_kml(matriz, "pontos_matriz.kml")
    
    # Cria KML com quadrados na bissetriz
    print("\n=== Criando KML com quadrados na bissetriz ===")
    criar_kml_quadrados_bissetriz(matriz, "quadrados_bissetriz.kml")

if __name__ == "__main__":
    main()
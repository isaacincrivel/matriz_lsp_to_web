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
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste", "estrutura_mt", "estrutura_bt", "poste", "base"])
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)

    new_vertices = dividir_tramo(new_vertices, section_size)

    # Aplica marcação SIM baseada no ângulo de deflexão
    new_vertices = marcar_vertices_angulo_deflexao(new_vertices, gap_size, module_name)

    # Aplica encabeçamento automático baseado na distância
    new_vertices = colocar_encabecamento_rede(new_vertices, section_size)

    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)

    #pontos_matriz = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)

    



    criar_kml_quadrados_bissetriz(pontos_matriz)
    
    # Adiciona os dados da matriz de pontos ao DataFrame
    for i, vertex in enumerate(new_vertices):
        dados_ponto = pontos_matriz.get(vertex, {})
        new_row = {
            "trecho": trecho,
            "sequencia": i,
            "lat": f"{vertex[0]:.9f}".replace(".", ","),
            "long": f"{vertex[1]:.9f}".replace(".", ","),
            "numero_poste": num_poste_inicial if i == 0 else "",
            "tipo_poste": tipo_poste if i == 0 else "",
            "estrutura_mt": dados_ponto.get("estrutura_mt", ""),
            "estrutura_bt": dados_ponto.get("estrutura_bt", ""),
            "poste": dados_ponto.get("poste", ""),
            "base": dados_ponto.get("base", "")
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
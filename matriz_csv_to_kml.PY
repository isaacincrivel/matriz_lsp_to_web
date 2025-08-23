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
    # Carrega o arquivo matriz_teste.csv para obter todas as colunas
    matriz_teste = pd.read_csv("matriz_teste.csv", sep=";", decimal=",")
    
    # Cria DataFrame com todas as colunas do CSV original + colunas adicionais necessárias
    # Remove colunas duplicadas que já existem no CSV
    colunas_base = ["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste"]
    colunas_csv = list(matriz_teste.columns)  # Todas as colunas do CSV original
    
    # Remove colunas duplicadas
    colunas_finais = colunas_base.copy()
    for coluna in colunas_csv:
        if coluna not in colunas_base:
            colunas_finais.append(coluna)
    
    matriz = pd.DataFrame(columns=colunas_finais)
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)

    new_vertices = dividir_tramo(new_vertices, section_size)

    # Aplica marcação SIM baseada no ângulo de deflexão
    new_vertices = marcar_vertices_angulo_deflexao(new_vertices, gap_size, module_name)

    # Aplica encabeçamento automático baseado na distância
    new_vertices = colocar_encabecamento_rede(new_vertices, section_size)

    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)

    # Filtra apenas as linhas com status "Implantar" e preserva TODAS as colunas do CSV
    matriz_teste_filtrada = matriz_teste[matriz_teste['status'] == 'Implantar'].copy()
    
    # Preserva todas as colunas originais do CSV sem renomear
    # Não renomeia mais as colunas para preservar os dados originais

    #pontos_matriz = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)

    # Nota: criar_kml_quadrados_bissetriz será chamada na função main
    
    # Adiciona os dados da matriz de pontos ao DataFrame
    for i, vertex in enumerate(new_vertices):
        # Busca dados correspondentes na matriz_teste_filtrada baseado na sequência
        dados_csv = {}
        if i < len(matriz_teste_filtrada):
            row = matriz_teste_filtrada.iloc[i]
            # Copia TODAS as colunas do CSV original
            for coluna in matriz_teste.columns:
                dados_csv[coluna] = str(row.get(coluna, ""))
        
        # Cria nova linha com todas as colunas
        new_row = {
            "trecho": trecho,
            "sequencia": i,
            "lat": f"{vertex[0]:.9f}".replace(".", ","),
            "long": f"{vertex[1]:.9f}".replace(".", ","),
            "numero_poste": num_poste_inicial if i == 0 else "",
            "tipo_poste": tipo_poste if i == 0 else ""
        }
        
        # Adiciona todas as colunas do CSV original
        for coluna in matriz_teste.columns:
            new_row[coluna] = dados_csv.get(coluna, "")
        
        matriz.loc[len(matriz)] = new_row
    return matriz

##################################################################################################################################
def main():
    trecho = "T1"
    module_naGIme = "MT7"
    module_data = ["MT10", 100, "SIM"]
    loose_gap = "SIM"
    section_size = 500
    gap_size = 100
    num_poste_inicial = "2255555"
    tipo_poste = "EXISTENTE"
    lista_nao_intercalar = [2, 4] 


    ##variaveis do modulo
    





    vertices = [
        (-17.041935, -49.224541, 0, ""), #0
        (-17.04206183, -49.22429193, 1, ""), #1
        (-17.04234952, -49.22372695, 2, ""), #2
        (-17.0426372, -49.22316196, 3, ""), #3
        (-17.04292489, -49.22259697, 4, ""), #4
        (-17.04321258, -49.22203198, 5, ""), #5
        (-17.04350026, -49.22146699, 6, ""), #6
        (-17.04378794, -49.220902, 7, ""), #7
        (-17.04407562, -49.220337, 8, ""), #8
        (-17.0443633, -49.21977201, 9, ""), #9
        (-17.04465098, -49.21920701, 10, ""), #10
        (-17.04493865, -49.21864201, 11, ""), #11
        (-17.04522633, -49.218077, 12, ""), #12
        (-17.045514, -49.217512, 13, ""), #13
        (-17.047802, -49.214406, 14, ""), #14
        (-17.047725, -49.213698, 15, ""), #15
        (-17.046803, -49.213231, 16, ""), #16
        (-17.0462475, -49.2130015, 17, ""), #17
        (-17.045692, -49.212772, 18, ""), #18
        (-17.04507267, -49.21286267, 19, ""), #19
        (-17.04445333, -49.21295333, 20, ""), #20
        (-17.043834, -49.213044, 21, ""), #21
        (-17.043305, -49.21327934, 22, ""), #22
        (-17.042776, -49.21351467, 23, ""), #23
        (-17.042247, -49.21375, 24, ""), #24
        (-17.04167125, -49.21385388, 25, ""), #25
        (-17.0410955, -49.21395775, 26, ""), #26
        (-17.04051975, -49.21406163, 27, ""), #27
        (-17.039944, -49.21416551, 28, ""), #28
        (-17.03936825, -49.21426938, 29, ""), #29
        (-17.0387925, -49.21437325, 30, ""), #30
        (-17.03821675, -49.21447713, 31, ""), #31
        (-17.037641, -49.214581, 32, ""), #32
        (-17.037403, -49.2151458, 33, ""), #33
        (-17.03716501, -49.2157106, 34, ""), #34
        (-17.03692701, -49.2162754, 35, ""), #35
        (-17.036689, -49.2168402, 36, ""), #36
        (-17.036451, -49.217405, 37, "") #37

        #lat, lon, sequencia original vertice, encabecamento, 
    ]                          
    matriz = gerar_matriz(trecho, module_naGIme, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar)

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
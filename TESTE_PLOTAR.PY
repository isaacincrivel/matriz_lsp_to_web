import pandas as pd

# Importando funções dos módulos organizados
from calculo_geografico import distance, angle, polar, distance_ptos
from processamento_vertices import get_loose_gap, dividir_tramo, intercalar_vertices
from abaco_mosaico import mtz_abaco, point_in_polygon, mosaico
from exportacao import exportar_para_kml, salvar_csv

##################################################################################################################################
def gravar_pontos_matriz(new_vertices, sequencia, estrutura_mt, estrutura_bt, poste, base):
    """
    Função que grava os pontos da matriz com seus dados associados.
    
    Args:
        new_vertices: Lista de vértices (pontos) no formato [(lat, lon), ...]
        sequencia: Índice do ponto na lista (0, 1, 2, ...)
        estrutura_mt: Dados da estrutura MT (ex: "D1")
        estrutura_bt: Dados da estrutura BT (ex: "D2")
        poste: Dados do poste (ex: "P23")
        base: Dados da base (ex: "B1")
    
    Returns:
        dict: Dicionário com os pontos e seus dados associados
    """
    pontos_matriz = {}
    
    # Verifica se a sequência é válida
    if sequencia < 0 or sequencia >= len(new_vertices):
        print(f"Erro: Sequência {sequencia} inválida. Deve estar entre 0 e {len(new_vertices)-1}")
        return pontos_matriz
    
    # Adiciona todos os pontos de new_vertices ao dicionário
    for i, ponto in enumerate(new_vertices):
        pontos_matriz[ponto] = {}
    
    # Adiciona os dados específicos no ponto indicado pela sequência
    ponto_especifico = new_vertices[sequencia]
    pontos_matriz[ponto_especifico] = {
        "estrutura_mt": estrutura_mt,
        "estrutura_bt": estrutura_bt,
        "poste": poste,
        "base": base
    }
    
    return pontos_matriz

##################################################################################################################################
def poste_derivacao( new_vertices, loose_gap, tipo_poste, module_name):   
    pto1 = new_vertices[0]
    pto2 = new_vertices[1]
  
    # se poste não for existente colocar poste
    if tipo_poste == "EXISTENTE":

        ### Se poste existente e instalou vão frouxo, colocar estrutura de derivação existente       
            resultado = mosaico ( 115, distance_ptos (pto1 , pto2),  module_name)      
            if resultado is None:
                 def_estrutura, def_estruturabt, def_poste, def_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
            else:
                def_estrutura, def_estruturabt, def_poste, def_base = resultado[0], resultado[1], resultado[2], resultado[3]

    ## Se poste intercalado                    
    else:
        if loose_gap == "SIM":
            resultado = mosaico ( 105, distance_ptos (pto1 , pto2),  module_name)
            if resultado is None:
                def_estrutura, def_estruturabt, def_poste, def_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
            else:
                def_estrutura, def_estruturabt, def_poste, def_base = resultado[0], resultado[1], resultado[2], resultado[3]
        else:
            ## Se poste intercalado e não instalou vão frouxo, usar mesma regra de fim de linha
            resultado = mosaico ( 95, distance_ptos (pto1 , pto2),  module_name)
            if resultado is None:
                def_estrutura, def_estruturabt, def_poste, def_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
            else:
                def_estrutura, def_estruturabt, def_poste, def_base = resultado[0], resultado[1], resultado[2], resultado[3]
    return def_estrutura, def_estruturabt, def_poste, def_base

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste", "estrutura_mt", "estrutura_bt", "poste", "base"])
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)
    new_vertices = dividir_tramo(new_vertices, section_size)
    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)




    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = poste_derivacao (new_vertices, loose_gap, tipo_poste, module_name)
    pontos_matriz = gravar_pontos_matriz(new_vertices, 0, mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base)

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
    lista_nao_intercalar = [0, 3] 

    vertices = [
        (-17.041935, -49.224541), #0
        (-17.045514, -49.217512), #2
        (-17.047802, -49.214406), #3
        (-17.047725, -49.213698), #4
        (-17.046803, -49.213231)
    ]                          
    matriz = gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar)

#, lista_nao_intercalar


    # Salva o arquivo CSV na pasta resultados
    salvar_csv(matriz, "matriz_resultado.csv")
    
    # Exporta os pontos para KML na pasta resultados
    print("\n=== Exportando para KML ===")
    exportar_para_kml(matriz, "pontos_matriz.kml")

if __name__ == "__main__":
    main()



import pandas as pd

# Importando funções dos módulos organizados
from calculo_geografico import distance, angle, polar, distance_ptos, angulo_deflexao
from processamento_vertices import get_loose_gap, dividir_tramo, intercalar_vertices
from abaco_mosaico import mtz_abaco, point_in_polygon, mosaico
from exportacao import exportar_para_kml, salvar_csv

##################################################################################################################################
def gravar_pontos_matriz(pontos_matriz, sequencia, estrutura_mt, estrutura_bt, poste, base):
    """
    Função que adiciona dados de um ponto específico ao dicionário pontos_matriz.
    
    Args:
        pontos_matriz: Dicionário existente com os pontos
        sequencia: Índice do ponto na lista (0, 1, 2, ...)
        estrutura_mt: Dados da estrutura MT (ex: "D1")
        estrutura_bt: Dados da estrutura BT (ex: "D2")
        poste: Dados do poste (ex: "P23")
        base: Dados da base (ex: "B1")
    
    Returns:
        dict: Dicionário atualizado com os dados do ponto
    """
    # Obtém a lista de vértices das chaves do dicionário
    new_vertices = list(pontos_matriz.keys())
    
    # Verifica se a sequência é válida
    if sequencia < 0 or sequencia >= len(new_vertices):
        print(f"Erro: Sequência {sequencia} inválida. Deve estar entre 0 e {len(new_vertices)-1}")
        return pontos_matriz
    
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
    """
    Função que processa todos os pontos de new_vertices para determinar estruturas e postes.
    
    Args:
        new_vertices: Lista de vértices [(lat, lon), ...]
        loose_gap: "SIM" ou "NÃO" para aplicar regra de vão frouxo
        tipo_poste: "EXISTENTE" ou outro tipo
        module_name: Nome do módulo para consulta no ábaco
    
    Returns:
        dict: Dicionário com todos os pontos e seus dados associados
    """
    # Cria um dicionário pontos_matriz vazio para todos os vértices de new_vertices
    pontos_matriz = {}
    for ponto in new_vertices:
        pontos_matriz[ponto] = {}
    
    # Itera sobre todos os pontos de new_vertices
    for i in range(len(new_vertices)):
        pt2 = new_vertices[i]  # Ponto atual (referência)
        pt1 = new_vertices[i - 1] if i > 0 else None  # Ponto anterior
        pt3 = new_vertices[i + 1] if i < len(new_vertices) - 1 else None  # Ponto posterior

        # Calcula a distância maior apenas se existir pt1 e pt3
        if pt1 is not None and pt3 is not None:
            dist1 = distance_ptos(pt1, pt2)
            dist2 = distance_ptos(pt2, pt3)
            distancia_maior = max(dist1, dist2)
            angulo_def = angulo_deflexao(pt1, pt2, pt3) 
        
                # Se é o primeiro ponto (i == 0)
        if i == 0:
            # Determina o tipo de poste e aplica a lógica correspondente
            if tipo_poste == "EXISTENTE":
                # Se poste existente e instalou vão frouxo, colocar estrutura de derivação existente       
                resultado = mosaico(115, distance_ptos(pt2, pt3), module_name)      
                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 115°, distância: {distance_ptos(pt2, pt3):.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = resultado[0], resultado[1], resultado[2], resultado[3]
            # Se poste intercalado                    
            else:
                if loose_gap == "SIM":
                    resultado = mosaico(105, distance_ptos(pt2, pt3), module_name)
                    if resultado is None:
                        print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 105°, distância: {distance_ptos(pt2, pt3):.2f}m")
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
                    else:
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = resultado[0], resultado[1], resultado[2], resultado[3]
                else:
                    # Se poste intercalado e não instalou vão frouxo, usar mesma regra de fim de linha
                    resultado = mosaico(95, distance_ptos(pt2, pt3), module_name)
                    if resultado is None:
                        print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt2, pt3):.2f}m")
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
                    else:
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = resultado[0], resultado[1], resultado[2], resultado[3]
        
        # Para pontos intermediários (i > 0)
        else:
            if pt3 is not None:
                # Lógica para pontos intermediários
                resultado = mosaico(angulo_def, distancia_maior, module_name) 
                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: {angulo_def:.2f}°, distância: {distancia_maior:.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = resultado[0], resultado[1], resultado[2], resultado[3]
            else:
                resultado = mosaico(95, distance_ptos(pt1, pt2), module_name) 
                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt1, pt2):.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = resultado[0], resultado[1], resultado[2], resultado[3]
        pontos_matriz = gravar_pontos_matriz(pontos_matriz, i, mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base)

    # Retorna o resultado do primeiro ponto (mantendo compatibilidade)
    return     pontos_matriz 





##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste", "estrutura_mt", "estrutura_bt", "poste", "base"])
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)
    new_vertices = dividir_tramo(new_vertices, section_size)
    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)





    #mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = poste_derivacao (new_vertices, loose_gap, tipo_poste, module_name)
    #pontos_matriz = gravar_pontos_matriz(new_vertices, 0, mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base)

    pontos_matriz = poste_derivacao (new_vertices, loose_gap, tipo_poste, module_name)
    #print (pontos_matriz)




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
        (-17.041935, -49.224541, 1), #0
        (-17.045514, -49.217512, 2), #2
        (-17.047802, -49.214406, 2), #3
        (-17.047725, -49.213698, 4), #4
        (-17.046803, -49.213231, 5)
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




 
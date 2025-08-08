import pandas as pd

# Importando funções dos módulos organizados
from calculo_geografico import distance, angle, polar, distance_ptos, angulo_deflexao
from processamento_vertices import get_loose_gap, dividir_tramo, intercalar_vertices
from abaco_mosaico import mtz_abaco, point_in_polygon, mosaico
from exportacao import exportar_para_kml, salvar_csv
from kml import criar_kml_quadrados_bissetriz

##################################################################################################################################
def gravar_pontos_matriz(pontos_matriz, sequencia, estrutura_mt, estrutura_bt, poste, base, posicao_poste):
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
def colocar_poste_estrutura( new_vertices, loose_gap, tipo_poste, module_name):  
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
        
        # Extrai o elemento na posição 3 do pt2 (índice 3)
        possui_encabecamento = pt2[3] if len(pt2) > 3 else ""
        
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
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]
            # Se poste intercalado                    
            else:
                if loose_gap == "SIM":
                    resultado = mosaico(105, distance_ptos(pt2, pt3), module_name)
                    if resultado is None:
                        print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 105°, distância: {distance_ptos(pt2, pt3):.2f}m")
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                    else:
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]
                else:
                    # Se poste intercalado e não instalou vão frouxo, usar mesma regra de fim de linha
                    resultado = mosaico(95, distance_ptos(pt2, pt3), module_name)
                    if resultado is None:
                        print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt2, pt3):.2f}m")
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                    else:
                        mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]
        
        # Para pontos intermediários (i > 0)
        else:
            if pt3 is not None:
                # Lógica para pontos intermediários
                resultado = mosaico(angulo_def, distancia_maior, module_name) 
                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: {angulo_def:.2f}°, distância: {distancia_maior:.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]
            else:
                ############################################# implementar lógica para encabecamento automático
                #if possui_encabecamento == "SIM_AUTOMATICO" or possui_encabecamento == "SIM":
                    
                #    resultado = mosaico(95, distance_ptos(pt1, pt2), module_name) 


                #else:
                resultado = mosaico(95, distance_ptos(pt1, pt2), module_name) 




                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt1, pt2):.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]



        pontos_matriz = gravar_pontos_matriz(pontos_matriz, i, mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste)

    # Retorna o resultado do primeiro ponto (mantendo compatibilidade)
    return pontos_matriz 

##################################################################################################################################
def marcar_vertices_angulo_deflexao(vertices):
    """
    Marca vértices com "SIM" no quarto elemento se o ângulo de deflexão for maior que 30°.
    
    Args:
        vertices: Lista de vértices [(lat, lon, id, status), ...]
    
    Returns:
        list: Lista de vértices com marcações "SIM" atualizadas
    """
    new_vertices = []
    
    for i in range(len(vertices)):
        vertex = vertices[i]
        
        # Garante que o vértice tenha pelo menos 4 elementos
        if len(vertex) < 4:
            # Se não tem quarto elemento, adiciona ""
            vertex = (vertex[0], vertex[1], vertex[2] if len(vertex) > 2 else "", "")
        
        # Se já possui "SIM" no quarto elemento, mantém como está
        if len(vertex) >= 4 and vertex[3] == "SIM":
            new_vertices.append(vertex)
            continue
        
        # Para pontos intermediários (não primeiro nem último)
        if i > 0 and i < len(vertices) - 1:
            pt1 = vertices[i - 1]  # Ponto anterior
            pt2 = vertex           # Ponto atual
            pt3 = vertices[i + 1]  # Ponto posterior
            
            # Calcula o ângulo de deflexão
            angulo_def = angulo_deflexao(pt1, pt2, pt3)
            
            # Se ângulo maior que 30°, marca com "SIM"
            if angulo_def > 30:
                vertex = (vertex[0], vertex[1], vertex[2], "SIM")
            else:
                # Mantém o quarto elemento como estava ou coloca ""
                vertex = (vertex[0], vertex[1], vertex[2], vertex[3] if len(vertex) >= 4 else "")
        else:
            # Para primeiro e último ponto, mantém como está
            vertex = (vertex[0], vertex[1], vertex[2], vertex[3] if len(vertex) >= 4 else "")
        
        new_vertices.append(vertex)
    
    return new_vertices

##################################################################################################################################
def colocar_encabecamento_rede(new_vertices, section_size):
    """
    Efetua loop em todos os vértices, acumulando distâncias e marcando encabeçamentos automáticos.
    
    Args:
        new_vertices: Lista de vértices [(lat, lon, id, status), ...]
        section_size: Tamanho da seção em metros
    
    Returns:
        list: Lista de vértices com encabeçamentos automáticos marcados
    """
    from calculo_geografico import distance_ptos
    
    if len(new_vertices) < 2:
        return new_vertices
    
    vertices_resultado = []
    distancia_acumulada = 0.0
    inicio_tramo = 0
    
    for i in range(len(new_vertices)):
        vertex = new_vertices[i]
        
        # Garante que o vértice tenha pelo menos 4 elementos
        if len(vertex) < 4:
            vertex = (vertex[0], vertex[1], vertex[2] if len(vertex) > 2 else "", "")
        
        # Se é o primeiro vértice, apenas adiciona
        if i == 0:
            vertices_resultado.append(vertex)
            continue
        
        # Calcula a distância entre o vértice atual e o anterior
        vertice_anterior = new_vertices[i - 1]
        distancia_atual = distance_ptos(vertice_anterior, vertex)
        distancia_acumulada += distancia_atual
        
        # Verifica se o vértice atual tem "SIM" no quarto elemento
        if len(vertex) >= 4 and vertex[3] == "SIM":
            # Encontrou um "SIM", paralisa a contagem
            # Verifica se precisa dividir o tramo
            if distancia_acumulada > section_size:
                # Precisa dividir o tramo em seções menores
                # Encontra o vértice mais próximo do meio do tramo
                distancia_meio = distancia_acumulada / 2
                distancia_temp = 0.0
                vertice_escolhido = inicio_tramo
                
                for j in range(inicio_tramo + 1, i):
                    if j > inicio_tramo:
                        dist_anterior = distance_ptos(new_vertices[j - 1], new_vertices[j])
                        distancia_temp += dist_anterior
                    
                    if abs(distancia_temp - distancia_meio) < abs(distancia_temp - distancia_meio + dist_anterior):
                        vertice_escolhido = j
                        break
                
                # Marca o vértice escolhido com "SIM_AUTOMATICO"
                if vertice_escolhido < len(vertices_resultado):
                    vertice_escolhido_atual = vertices_resultado[vertice_escolhido]
                    vertices_resultado[vertice_escolhido] = (
                        vertice_escolhido_atual[0],
                        vertice_escolhido_atual[1],
                        vertice_escolhido_atual[2],
                        "SIM_AUTOMATICO"
                    )
            
            # Adiciona o vértice atual e reinicia a contagem
            vertices_resultado.append(vertex)
            distancia_acumulada = 0.0
            inicio_tramo = i
        else:
            # Verifica se a distância acumulada ultrapassou o section_size
            if distancia_acumulada >= section_size:
                # Precisa dividir o tramo
                # Encontra o vértice mais próximo do meio do tramo
                distancia_meio = distancia_acumulada / 2
                distancia_temp = 0.0
                vertice_escolhido = inicio_tramo
                
                for j in range(inicio_tramo + 1, i):
                    if j > inicio_tramo:
                        dist_anterior = distance_ptos(new_vertices[j - 1], new_vertices[j])
                        distancia_temp += dist_anterior
                    
                    if abs(distancia_temp - distancia_meio) < abs(distancia_temp - distancia_meio + dist_anterior):
                        vertice_escolhido = j
                        break
                
                # Marca o vértice escolhido com "SIM_AUTOMATICO"
                if vertice_escolhido < len(vertices_resultado):
                    vertice_escolhido_atual = vertices_resultado[vertice_escolhido]
                    vertices_resultado[vertice_escolhido] = (
                        vertice_escolhido_atual[0],
                        vertice_escolhido_atual[1],
                        vertice_escolhido_atual[2],
                        "SIM_AUTOMATICO"
                    )
                
                # Reinicia a contagem a partir do vértice atual
                distancia_acumulada = 0.0
                inicio_tramo = i
            
            # Adiciona o vértice atual
            vertices_resultado.append(vertex)
    
    return vertices_resultado

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste", "estrutura_mt", "estrutura_bt", "poste", "base"])
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)

    new_vertices = dividir_tramo(new_vertices, section_size)

    # Aplica marcação SIM baseada no ângulo de deflexão
    new_vertices = marcar_vertices_angulo_deflexao(new_vertices)

    # Aplica encabeçamento automático baseado na distância
    new_vertices = colocar_encabecamento_rede(new_vertices, section_size)

    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)



    

    pontos_matriz = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)


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
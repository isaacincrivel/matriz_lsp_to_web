"""
Módulo para colocar encabeçamento automático na rede baseado em distâncias.
"""

from calculo_geografico import distance_ptos


def colocar_encabecamento_rede(new_vertices, section_size):
    """
    Efetua loop em todos os vértices, acumulando distâncias e marcando encabeçamentos automáticos.
    
    Args:
        new_vertices: Lista de vértices [(lat, lon, id, status), ...]
        section_size: Tamanho da seção em metros
    
    Returns:
        list: Lista de vértices com encabeçamentos automáticos marcados
    """
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

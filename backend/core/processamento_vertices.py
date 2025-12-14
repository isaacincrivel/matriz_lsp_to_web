import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.core.calculo_geografico import distance, angle, polar

##################################################################################################################################
# FUNÇÕES DE PROCESSAMENTO DE VÉRTICES
##################################################################################################################################

def get_loose_gap(loose_gap, vertices):
    """
    Adiciona um ponto intermediário se a distância entre os dois primeiros pontos for maior que 60m.
    
    Args:
        loose_gap: "SIM" ou "NÃO" para aplicar a regra - VÃO FROUXO
        vertices: Lista de vértices [(lat, lon), ...]
    
    Returns:
        tuple: (nova_lista_vertices, status_loose_gap)
    """
    if loose_gap != "SIM":
        return vertices, "NÃO"
    
    else:
        first_point = vertices[0]
        second_point = vertices[1]
        distance_between = distance(first_point[0], first_point[1], second_point[0], second_point[1])

        if distance_between > 60:
            angle_between = angle(first_point[0], first_point[1], second_point[0], second_point[1])
            new_point_coords = polar(first_point[0], first_point[1], 30, angle_between)
            new_point = (new_point_coords[0], new_point_coords[1], "", "SIM")  # Adiciona terceiro elemento vazio
            return [first_point, new_point, second_point] + vertices[2:], "SIM"
        return vertices, "NÃO"

##################################################################################################################################

def dividir_tramo(vertices, section_size):
    """
    Divide os tramos em seções menores baseado no tamanho da seção.
    
    Args:
        vertices: Lista de vértices [(lat, lon), ...]
        section_size: Tamanho máximo da seção em metros
    
    Returns:
        list: Nova lista de vértices com pontos intermediários

        GUSTAVO: SEMPRE QUE ADICIONAR UM PONTO, CLASSIFICALO COMO ENCABEÇAMENTO - vertice_encabec
    """
    new_vertices = []
    for i in range(len(vertices) - 1):
        pto1 = vertices[i]
        pto2 = vertices[i + 1]
        new_vertices.append(pto1)
        dst1 = distance(pto1[0], pto1[1], pto2[0], pto2[1])
        if dst1 > section_size:
            num_divisoes = int(dst1 // section_size)
            distancia_por_tramo = dst1 / (num_divisoes + 1)
            ang = angle(pto1[0], pto1[1], pto2[0], pto2[1])
            for j in range(1, num_divisoes + 1):
                novo_pto = polar(pto1[0], pto1[1], distancia_por_tramo * j, ang)

                new_point = (novo_pto[0], novo_pto[1], "", "SIM") 

                new_vertices.append(new_point)
    new_vertices.append(vertices[-1])
    return new_vertices


##################################################################################################################################

def intercalar_vertices(vertices, lista_nao_intercalar, gap_size):
    """
    Intercala pontos intermediários nos tramos, exceto nos pontos cujo terceiro elemento está na lista_nao_intercalar.
    
    Args:
        vertices: Lista de vértices [(lat, lon, id), ...]
        lista_nao_intercalar: Lista de IDs onde não intercalar
        gap_size: Tamanho máximo do gap em metros
    
    Returns:
        list: Nova lista de vértices com pontos intercalados
    """
    new_vertices = []
    for i in range(len(vertices) - 1):
        pto1 = vertices[i]
        pto2 = vertices[i + 1]
        new_vertices.append(pto1)
        
        # Verifica se o terceiro elemento da tupla está na lista_nao_intercalar
        terceiro_elemento_pto1 = None
        if len(pto1) >= 3:
            terceiro_elemento_pto1 = pto1[2]
        
        if terceiro_elemento_pto1 in lista_nao_intercalar:
            continue
        
        dst = distance(pto1[0], pto1[1], pto2[0], pto2[1])
        if dst > gap_size:
            num_divisoes = int(dst // gap_size)
            if num_divisoes > 0:
                distancia_por_tramo = dst / (num_divisoes + 1)
                ang = angle(pto1[0], pto1[1], pto2[0], pto2[1])
                for j in range(1, num_divisoes + 1):
                    novo_pto_coords = polar(pto1[0], pto1[1], distancia_por_tramo * j, ang)
                    novo_pto = (novo_pto_coords[0], novo_pto_coords[1], "", "")
                    new_vertices.append(novo_pto)

    new_vertices.append(vertices[-1])
    return new_vertices 
"""
Módulo para marcar vértices com base no ângulo de deflexão.
"""

from abaco_mosaico import mosaico
from calculo_geografico import angulo_deflexao, distance_ptos


def marcar_vertices_angulo_deflexao(vertices, gap_size, module_name):
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

            vao_anterior_tem_poste = pt1[2]
            vao_posterior_tem_poste = pt3[2]

            if  vao_anterior_tem_poste == '':                
                distancia1 = gap_size
            else:
                distancia1 = distance_ptos(pt1, pt2)
                

            if  vao_posterior_tem_poste == '':                
                distancia2 = gap_size
            else:
                distancia2 = distance_ptos(pt2, pt3)
                
            
                       
            
            # Calcula o ângulo de deflexão
            angulo_def = angulo_deflexao(pt1, pt2, pt3)

            if distancia1 > distancia2:
                distancia_maior = distancia1
            else:
                distancia_maior = distancia2
                

            resultado = mosaico(angulo_def, distancia_maior,  module_name)

            encabecamento_sim_nao = resultado[5]

            if encabecamento_sim_nao == "ENC":
                vertex = (vertex[0], vertex[1], vertex[2], "SIM")
            else:
                vertex = (vertex[0], vertex[1], vertex[2], vertex[3] if len(vertex) >= 4 else "")



            
            # Se ângulo maior que 30°, marca com "SIM"
            #if angulo_def > 30:
            #    vertex = (vertex[0], vertex[1], vertex[2], "SIM")
            #else:
                # Mantém o quarto elemento como estava ou coloca ""
            #    vertex = (vertex[0], vertex[1], vertex[2], vertex[3] if len(vertex) >= 4 else "")




        else:
            # Para primeiro e último ponto, mantém como está
            vertex = (vertex[0], vertex[1], vertex[2], vertex[3] if len(vertex) >= 4 else "")
        
        new_vertices.append(vertex)
    
    return new_vertices

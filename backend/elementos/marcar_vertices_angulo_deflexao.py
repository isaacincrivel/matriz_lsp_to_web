"""
Módulo para marcar vértices com base no ângulo de deflexão.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.abacos.abaco_mosaico import mosaico
from backend.core.calculo_geografico import angulo_deflexao, distance_ptos


def marcar_vertices_angulo_deflexao(vertices, gap_size, module_name, lista_nao_intercalar):
    """
    Marca vértices com "SIM" no quarto elemento se o ângulo de deflexão e distania, atraves de consulta ao abao
    der estrutura de encabeçamento.
    
    Returns:
        list: Lista de vértices com marcações "SIM" atualizadas
    """
    new_vertices = []
    distancia2_anterior = None  # Armazena distancia2 do vértice anterior
    # seleciona cada vertice da lista de vertice para ser analisado
    for i in range(len(vertices)):
        vertex = vertices[i]


        
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



            # Calcula distancia1: se existe distancia2_anterior, usa ela; senão verifica lista_nao_intercalar
            if distancia2_anterior is not None:
                # Se existe distancia2_anterior do vértice anterior, usa esse valor
                distancia1 = distancia2_anterior
            else:
                # Se não existe distancia2_anterior, verifica se o vértice anterior está na lista_nao_intercalar
                vertice_anterior_na_lista = False
                sequencia_anterior = pt1[2]  # Sequência do vértice anterior
                if lista_nao_intercalar:
                    try:
                        # Converte sequencia_anterior para int para comparação
                        if isinstance(sequencia_anterior, (int, float)):
                            seq_int = int(sequencia_anterior)
                        elif isinstance(sequencia_anterior, str) and sequencia_anterior.strip() != "":
                            seq_int = int(float(sequencia_anterior))
                        else:
                            seq_int = None
                        
                        # Compara diretamente o valor da sequência com os valores na lista
                        if seq_int is not None and seq_int in lista_nao_intercalar:
                            vertice_anterior_na_lista = True
                    except (ValueError, TypeError):
                        pass
                
                if vertice_anterior_na_lista:
                    # Se o vértice anterior está na lista: usa distância real
                    distancia1 = distance_ptos(pt1, pt2)
                else:
                    # Se não está na lista: usa gap_size
                    distancia1 = gap_size


                

            # PREMISSAS:
            # toda vez que for ponto vazio, vamos utilizar como distancia2 gap_size    
            
            # Verifica se o vértice atual está na lista_nao_intercalar
            # Compara diretamente a sequência original (terceiro elemento) com os valores da lista
            vertice_na_lista = False
            sequencia_atual = pt2[2]  # Sequência original do vértice atual (terceiro elemento)
            if lista_nao_intercalar:
                try:
                    # Converte sequencia_atual para int para comparação
                    if isinstance(sequencia_atual, (int, float)):
                        seq_int = int(sequencia_atual)
                    elif isinstance(sequencia_atual, str) and sequencia_atual.strip() != "":
                        seq_int = int(float(sequencia_atual))
                    else:
                        seq_int = None
                    
                    # Compara diretamente o valor da sequência com os valores na lista
                    if seq_int is not None and seq_int in lista_nao_intercalar:
                        vertice_na_lista = True
                except (ValueError, TypeError):
                    pass
            
            # Calcula distancia2 baseado se o vértice está ou não na lista_nao_intercalar
            if vertice_na_lista:
                # Se está na lista: usa distância real
                distancia2 = distance_ptos(pt2, pt3)
            else:
                # Se não está na lista: usa gap_size
                distancia2 = gap_size
            
            # Armazena o valor atual de distancia2 em distancia2_anterior
            distancia2_anterior = distancia2
                
            #verificar o tramo maior que tem. e se existir tramo  maior que o maximo do abaco intercalar potes mas avisar na tela
            #resultado = mosaico(10, distancia_maior,  module_name)           
            
            # Calcula o ângulo de deflexão
            angulo_def = angulo_deflexao(pt1, pt2, pt3)


            if distancia1 > distancia2:
                distancia_maior = distancia1
            else:
                distancia_maior = distancia2
                

            resultado = mosaico(angulo_def, distancia_maior,  module_name)

            # resultado agora é um dicionário dinâmico, busca o campo de encabecamento
            # Pode ser "tang_ou_enc", "encabecamento", ou outro nome dependendo do módulo
            encabecamento_sim_nao = resultado.get("tang_ou_enc") or resultado.get("encabecamento") or ""

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

"""
Módulo para colocar postes e estruturas na rede baseado em ábacos e regras de negócio.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.core.calculo_geografico import distance_ptos, angulo_deflexao
from backend.abacos.abaco_mosaico import mosaico


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
        posicao_poste: Posição do poste (ex: "TOPOMAIOR")
    
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
        "base": base,
        "num_poste": "8989899889",
        "tipo_poste": "EXISTENTE",
        "estru_mt_nv1": "ESTRUTURA_MT",
        "estru_mt_nv2": "ESTRUTURA_MT",
        "estru_mt_nv3": "ESTRUTURA_MT",
        "est_bt_nv1": "ESTRUTURA_BT",
        "est_bt_nv2": "ESTRUTURA_BT",
        "estai_ancora": "ESTRUTURA_BT",
        "base_reforcada": "BASE_REFORCADA",
        "base_concreto": "BASE_CONCRETO",
        "aterr_neutro": "SIM",
        "chave": "SIM",
        "trafo": "SIM",
        "equipamento": "SIM",
        "faixa": "SIM",
        "cort_arvores_isol": "SIM",
        "adiconal_1": "SIM",
        "qdt_adic_1": "SIM",
        "adiconal_2": "SIM",
        "qdt_adic_2": "SIM",
        "adiconal_3": "SIM",
        "qdt_adic_3": "SIM",
        "adiconal_4": "SIM",
        "qdt_adic_4": "SIM",
        "adiconal_5": "SIM",    	


    }
    
    return pontos_matriz


def colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name):
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
                # se tiver pt3, usar ábaco de pontos intermediários
                # Lógica para pontos intermediários
                ############################################# implementar lógica para encabecamento automático
                
                resultado = mosaico(angulo_def, distancia_maior, module_name) 

                if (possui_encabecamento == "SIM_AUTOMATICO" or possui_encabecamento == "SIM") and (resultado[5] != "ENC"):
                    resultado = mosaico(135, distancia_maior, module_name) 
                

                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: {angulo_def:.2f}°, distância: {distancia_maior:.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]
            else:
                ## se não tiver pt3, usar ábaco de fim de linha
                resultado = mosaico(95, distance_ptos(pt1, pt2), module_name) 

                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt1, pt2):.2f}m")
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO", "TOPOMAIOR"
                else:
                    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste = resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]

        pontos_matriz = gravar_pontos_matriz(pontos_matriz, i, mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base, posicao_poste)

    # Retorna o resultado do primeiro ponto (mantendo compatibilidade)
    return pontos_matriz

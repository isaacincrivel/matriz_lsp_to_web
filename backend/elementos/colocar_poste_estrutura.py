"""
Módulo para colocar postes e estruturas na rede baseado em ábacos e regras de negócio.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.core.calculo_geografico import distance_ptos, angulo_deflexao
from backend.abacos.abaco_mosaico import mosaico


def gravar_pontos_matriz(pontos_matriz, sequencia, resultado_abaco=None, sequencia_poste=None):
    """
    Função que adiciona dados de um ponto específico ao dicionário pontos_matriz.
    Os campos do resultado_abaco (dicionário dinâmico do módulo) são mesclados com os campos fixos.
    O tipo_poste virá do resultado_abaco se existir lá.
    
    Args:
        pontos_matriz: Dicionário existente com os pontos
        sequencia: Índice do ponto na lista (0, 1, 2, ...)
        resultado_abaco: Dicionário com campos dinâmicos do ábaco do módulo (todos os campos que vieram do resultado)
        sequencia_poste: Sequência do poste para ser salva no CSV (inicia em 0 se EXISTENTE, 1 caso contrário)
    
    Returns:
        dict: Dicionário atualizado com os dados do ponto
    """
    # Obtém a lista de vértices das chaves do dicionário
    new_vertices = list(pontos_matriz.keys())
    
    # Verifica se a sequência é válida
    if sequencia < 0 or sequencia >= len(new_vertices):
        print(f"Erro: Sequência {sequencia} inválida. Deve estar entre 0 e {len(new_vertices)-1}")
        return pontos_matriz
    



    # Dicionário base com valores padrão para todos os campos possíveis
    dados_base = {
        "sequencia": "",
        "num_poste": "",
        "tipo_poste": "",
        "estru_mt_nv1": "",
        "estru_mt_nv2": "",
        "estru_mt_nv3": "",
        "est_bt_nv1": "",
        "est_bt_nv2": "",
        "estai_ancora": "",
        "base_reforcada": "",
        "base_concreto": "",
        "aterr_neutro": "",
        "chave": "",
        "trafo": "",
        "equipamento": "",
        "faixa": "",
        "cort_arvores_isol": "",
        "adiconal_1": "",
        "qdt_adic_1": "",
        "adiconal_2": "",
        "qdt_adic_2": "",
        "adiconal_3": "",
        "qdt_adic_3": "",
        "adiconal_4": "",
        "qdt_adic_4": "",
        "adiconal_5": "",
        "qdt_adic_5": "",
        "adiconal_6": "",
        "qdt_adic_6": "",
        "adiconal_7": "",
        "qdt_adic_7": "",               
        "rotacao_poste": "",
        "tang_ou_enc": ""
    }
    
    # Se houver resultado do ábaco, mescla todos os campos dinâmicos do módulo
    # Isso sobrescreve os valores padrão com os valores do ábaco e adiciona campos novos
    # O tipo_poste virá do resultado_abaco se existir lá
    if resultado_abaco and isinstance(resultado_abaco, dict):
        dados_base.update(resultado_abaco)
    
    # Define o campo "sequencia" com o valor de sequencia_poste se foi fornecido
    if sequencia_poste is not None:
        dados_base["sequencia"] = sequencia_poste
    
    # tipo_poste vem do resultado_abaco (já foi mesclado pelo update acima)
    # Se não existir no resultado, mantém o valor padrão vazio
    
    # Adiciona os dados específicos no ponto indicado pela sequência
    ponto_especifico = new_vertices[sequencia]
    pontos_matriz[ponto_especifico] = dados_base
    
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
    
    # Inicializa sequencia_poste baseado no tipo_poste
    # Se EXISTENTE, começa em 0; caso contrário, começa em 1
    tipo_poste_upper = str(tipo_poste).upper() if tipo_poste else ""
    if tipo_poste_upper == "EXISTENTE":
        sequencia_poste = 0
    else:
        sequencia_poste = 1
    
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
            # Aceita "EXISTENTE" ou "Existente" (case-insensitive)
            tipo_poste_upper = str(tipo_poste).upper() if tipo_poste else ""
            if tipo_poste_upper == "EXISTENTE":
                # Se poste existente e instalou vão frouxo, colocar estrutura de derivação existente       
                resultado = mosaico(115, distance_ptos(pt2, pt3), module_name)      
                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 115°, distância: {distance_ptos(pt2, pt3):.2f}m")
                    resultado = None  # Passa None para usar valores padrão
                # resultado já é um dicionário completo com todos os campos do módulo
            # Se poste intercalado                    
            else:
                if loose_gap == "SIM":
                    resultado = mosaico(105, distance_ptos(pt2, pt3), module_name)
                    if resultado is None:
                        print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 105°, distância: {distance_ptos(pt2, pt3):.2f}m")
                        resultado = None  # Passa None para usar valores padrão
                    # resultado já é um dicionário completo com todos os campos do módulo
                else:
                    # Se poste intercalado e não instalou vão frouxo, usar mesma regra de fim de linha
                    resultado = mosaico(95, distance_ptos(pt2, pt3), module_name)
                    if resultado is None:
                        print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt2, pt3):.2f}m")
                        resultado = None  # Passa None para usar valores padrão
                    # resultado já é um dicionário completo com todos os campos do módulo
        
        # Para pontos intermediários (i > 0)
        else:
            if pt3 is not None:
                # se tiver pt3, usar ábaco de pontos intermediários
                # Lógica para pontos intermediários
                ############################################# implementar lógica para encabecamento automático
                
                resultado = mosaico(angulo_def, distancia_maior, module_name) 

                # Verifica encabecamento (pode ser "tang_ou_enc" ou "encabecamento" dependendo do módulo)
                encabecamento_atual = resultado.get("tang_ou_enc") or resultado.get("encabecamento") or "" if resultado else ""
                if (possui_encabecamento == "SIM_AUTOMATICO" or possui_encabecamento == "SIM") and (encabecamento_atual != "ENC"):
                    resultado = mosaico(135, distancia_maior, module_name) 
                

                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: {angulo_def:.2f}°, distância: {distancia_maior:.2f}m")
                    resultado = None  # Passa None para usar valores padrão
                # resultado já é um dicionário completo com todos os campos do módulo
            else:
                ## se não tiver pt3, usar ábaco de fim de linha
                resultado = mosaico(95, distance_ptos(pt1, pt2), module_name) 

                if resultado is None:
                    print(f"ALERTA: Verificar ábaco para ponto {i} - ângulo: 95°, distância: {distance_ptos(pt1, pt2):.2f}m")
                    resultado = None  # Passa None para usar valores padrão
                # resultado já é um dicionário completo com todos os campos do módulo

        # Passa o resultado completo (dicionário com todos os campos dinâmicos do módulo) e sequencia_poste para gravar_pontos_matriz
        # O tipo_poste virá do resultado (resultado_abaco) se existir lá
        pontos_matriz = gravar_pontos_matriz(pontos_matriz, i, resultado, sequencia_poste)
        
        # Incrementa sequencia_poste para o próximo ponto
        sequencia_poste += 1


    #resultado temos: indice 1 trata-se de estrutura mt, indice 2 trata-se de estrutura bt, 
    # indice 3 trata-se de poste, indice 4 trata-se de base, indice 5 trata-se de posição do poste

    # Retorna o resultado do primeiro ponto (mantendo compatibilidade)
    return pontos_matriz

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.core.calculo_geografico import distance_ptos

##################################################################################################################################
# FUNÇÕES DE ÁBACO E MOSAICO
##################################################################################################################################

def mtz_abaco(str1):
    """
    Retorna o ábaco correspondente ao módulo especificado.
    
    Args:
        str1: Nome do módulo (ex: "MT7", "MT8")
    
    Returns:
        list: Lista de entradas do ábaco
    """

    
    # cria o dicionario de abacos
    abacos = {}    
    abacos["10105"] = [
        {"estru_mt_nv1": "UP1", "tipo_poste": "PDT10/300", "rotacao_poste": "BICETRIZ", "tang_ou_enc": "TAN", "polygon": [(-1.0, 0.0), (-1.0, 217.143), (160.0, 217.143), (160.0, 0.0), (-1.0, 0.0)], "id": "ms1"},
        {"estru_mt_nv1": "UP1", "tipo_poste": "PDT10/300", "base_concreto": "BC", "rotacao_poste": "BICETRIZ", "tang_ou_enc": "TAN", "polygon": [(160.0, 0.0), (160.0, 217.143), (350.0, 0.0), (160.0, 0.0)], "id": "ms2"},
        {"estru_mt_nv1": "UP4", "tipo_poste": "PDT10/600", "base_concreto": "BC", "rotacao_poste": "ZIRTECIB", "tang_ou_enc": "ENC", "polygon": [(160.0, 217.143), (160.0, 300.0), (600.0, 100.0), (600.0, 0.0), (350.0, 0.0), (160.0, 217.143)], "id": "ms3"},
        {"estru_mt_nv1": "UP4", "tipo_poste": "PDT10/600", "base_concreto": "BC", "rotacao_poste": "ZIRTECIB", "tang_ou_enc": "ENC", "polygon": [(-1.0, 217.143), (-1.0, 401.143), (160.0, 217.143), (-1.0, 217.143)], "id": "ms4"},
        {"estru_mt_nv1": "UP4", "tipo_poste": "PDT10/1000", "base_concreto": "BC", "rotacao_poste": "ZIRTECIB", "tang_ou_enc": "ENC", "polygon": [(-1.0, 401.143), (-1.0, 500.0), (600.0, 500.0), (600.0, 100.0), (160.0, 300.0), (160.0, 217.143), (-1.0, 401.143)], "id": "ms5"},
        {"estru_mt_nv1": "U3U3", "tipo_poste": "PDT10/1500", "base_concreto": "BC", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(600.0, 220.0), (600.0, 500.0), (900.0, 500.0), (900.0, 220.0), (600.0, 220.0)], "id": "ms6"},
        {"estru_mt_nv1": "U3", "tipo_poste": "PDT10/1000", "estai_ancora": "ES", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(600.0, 0.0), (600.0, 220.0), (900.0, 220.0), (900.0, 0.0), (600.0, 0.0)], "id": "ms7"},
        {"estru_mt_nv1": "U3", "tipo_poste": "PDT10/600", "base_concreto": "BC", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(900.0, 220.0), (1000.0, 220.0), (1000.0, 1.39955e-12), (900.0, 9.09495e-13), (900.0, 220.0)], "id": "ms8"},
        {"estru_mt_nv1": "U3", "tipo_poste": "PDT10/1000", "base_concreto": "BC", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(900.0, 220.0), (900.0, 500.0), (1000.0, 500.0), (1000.0, 220.0), (900.0, 220.0)], "id": "ms9"},
        {"estru_mt_nv1": "U3", "tipo_poste": "PDT11/300", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(1000.0, 35.0), (1100.0, 35.0), (1100.0, 9.09495e-13), (1000.0, 1.39266e-12), (1000.0, 35.0)], "id": "ms10"},
        {"estru_mt_nv1": "U3", "tipo_poste": "PDT11/1000", "base_concreto": "BC", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(1000.0, 220.0), (1100.0, 220.0), (1100.0, 35.0), (1000.0, 35.0), (1000.0, 220.0)], "id": "ms11"},
        {"estru_mt_nv1": "U3", "tipo_poste": "EXIST", "base_concreto": "BC", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(1100.0, 35.0), (1200.0, 35.0), (1200.0, 9.09495e-13), (1100.0, 1.39266e-12), (1100.0, 35.0)], "id": "ms12"},
        {"estru_mt_nv1": "U3", "tipo_poste": "EXIST", "estai_ancora": "ES", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(1100.0, 220.0), (1200.0, 220.0), (1200.0, 35.0), (1100.0, 35.0), (1100.0, 220.0)], "id": "ms13"},
        {"estru_mt_nv1": "UP4", "tipo_poste": "PDT10/600", "base_concreto": "BC", "rotacao_poste": "ZIRTECIB", "tang_ou_enc": "ENC", "polygon": [(1300.0, 1.81899e-12), (1300.0, 180.0), (1400.0, 180.0), (1400.0, 2.72671e-12), (1300.0, 1.81899e-12)], "id": "ms14"}
    ]  
    abacos["10106"] = [
        {"estru_mt_nv1": "UP1", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "TAN", "polygon": [(-1.0, 0.0), (160.0, 0.0), (160.0, 217.143), (-1.0, 217.143), (-1.0, 0.0)]},
        {"estru_mt_nv1": "UP1", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ES", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "TAN", "polygon": [(160.0, 217.143), (160.0, 0.0), (350.0, 0.0), (160.0, 217.143)]},
        {"estru_mt_nv1": "UP4", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ED", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(-1.0, 217.143), (-1.0, 500.0), (160.0, 500.0), (160.0, 300.0), (600.0, 180.0), (600.0, 0.0), (350.0, 0.0), (160.0, 217.143), (-1.0, 217.143)]},
        {"estru_mt_nv1": "U3", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ED", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(600.0, 220.0), (600.0, 0.0), (900.0, 0.0), (900.0, 220.0), (600.0, 220.0)]},
        {"estru_mt_nv1": "UP4", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ET", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(160.0, 300.0), (160.0, 500.0), (600.0, 500.0), (600.0, 180.0), (160.0, 300.0)]},
        {"estru_mt_nv1": "U3U3", "estrutura_bt": "A1", "tipo_poste": "PDT10/600", "estai_ancora": "ET", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(600.0, 220.0), (600.0, 500.0), (900.0, 500.0), (900.0, 220.0), (600.0, 220.0)]},
        {"estru_mt_nv1": "U3", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ET", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(900.0, 220.0), (900.0, 500.0), (1100.0, 500.0), (1100.0, 220.0), (900.0, 220.0)]},
        {"estru_mt_nv1": "U3", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ES", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(900.0, 0.0), (900.0, 220.0), (1100.0, 220.0), (1100.0, 0.0), (900.0, 0.0)]},
        {"estru_mt_nv1": "UP4", "estrutura_bt": "A1", "tipo_poste": "PDT10/300", "estai_ancora": "ED", "rotacao_poste": "TOPOMAIOR", "tang_ou_enc": "ENC", "polygon": [(1100.0, 217.143), (1300.0, 217.143), (1300.0, 0.0), (1100.0, 0.0), (1100.0, 217.143)]}
    ]
    return abacos.get(str1, [])

##################################################################################################################################

def point_in_polygon(polygon, point):
    """
    Verifica se um ponto está dentro de um polígono usando o algoritmo ray casting.
    
    Args:
        polygon: Lista de pontos do polígono [(x, y), ...]
        point: Ponto a verificar (x, y)
    
    Returns:
        bool: True se o ponto está dentro do polígono
    """
    x, y = point
    odd = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi < y and yj >= y) or (yj < y and yi >= y)):
            if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                odd = not odd
        j = i
    return odd

##################################################################################################################################

def mosaico(ang1, dist1, str1):
    """
    Encontra a correspondência no ábaco baseado no ângulo e distância.
    
    Args:
        ang1: Ângulo multiplicado por 10
        dist1: Distância em metros
        str1: Nome do módulo
    
    Returns:
        dict: Dicionário com todos os campos do ábaco encontrado (exceto 'polygon' e 'id'), 
              ou None se não encontrar
    """
    ang1 = ang1 * 10
    abaco = mtz_abaco(str1)
    ptx = (ang1, dist1)

    for entry in abaco:
        # Entradas agora são dicionários com chaves nomeadas
        polygon = entry.get("polygon", [])
        if point_in_polygon(polygon, ptx):
            # Retorna uma cópia do dicionário sem os campos internos (polygon e id)
            resultado = {k: v for k, v in entry.items() if k not in ["polygon", "id"]}
            return resultado

    ## se não der nada tem que retornar algo padrão
    print(f"ERRO: Não foi possível encontrar correspondência no ábaco para:")
    print(f"  - Ângulo: {ang1}")
    print(f"  - Distância: {dist1}")
    print(f"  - Módulo: {str1}")
    print(f"  - Ponto: {ptx}")
    print(f"  - Ábaco disponível: {len(abaco)} entradas")
    return None 
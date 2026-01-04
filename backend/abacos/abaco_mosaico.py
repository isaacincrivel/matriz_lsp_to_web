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
    abacos["10104"] = [
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
    abacos["10105"] = [
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

    abacos["10101"] = [
        {"estru_mt_nv1": "N4", "tipo_poste": "PDT11/1000", "base_concreto": "BC", "polygon": [(1100, 0), (1100, 180), (1300, 180), (1300, 0), (1100, 0)], "id": "ms1"},
        {"estru_mt_nv1": "N3", "tipo_poste": "PDT11/1000", "base_concreto": "BC", "polygon": [(900, 0), (900, 140), (1100, 140), (1100, 0), (900, 0)], "id": "ms2"},
        {"estru_mt_nv1": "N3N3", "tipo_poste": "PDT11/2000", "base_concreto": "BC", "polygon": [(600, 0), (600, 140), (900, 140), (900, 0), (600, 0)], "id": "ms3"},
        {"estru_mt_nv1": "HT", "tipo_poste": "2XPDT11/1500", "base_concreto": "BC", "polygon": [(460, 500), (600, 500), (600, 140), (460, 500)], "id": "ms4"},
        {"estru_mt_nv1": "TE", "tipo_poste": "PDT11/2000", "base_concreto": "BC", "polygon": [(-1, 400), (-1, 500), (460, 500), (584.444, 180), (420, 180), (323.063, 400), (-1, 400)], "id": "ms5"},
        {"estru_mt_nv1": "TE", "tipo_poste": "PDT11/1500", "base_concreto": "BC", "polygon": [(59, 300), (59, 400), (323.063, 400), (420, 180), (250, 180), (212.125, 300), (59, 300)], "id": "ms6"},
        {"estru_mt_nv1": "TE", "tipo_poste": "PDT11/1000", "base_concreto": "BC", "polygon": [(59, 180), (59, 300), (212.125, 300), (250, 180), (59, 180)], "id": "ms7"},
        {"estru_mt_nv1": "TE", "tipo_poste": "PDT11/1000", "base_concreto": "BC", "polygon": [(-1, 400), (59, 400), (59, 180), (-1, 180), (-1, 400)], "id": "ms8"},
        {"estru_mt_nv1": "N4", "tipo_poste": "PDT11/2000", "base_concreto": "BC", "polygon": [(150, 180), (600, 60), (600, 140), (584.444, 180), (150, 180)], "id": "ms9"},
        {"estru_mt_nv1": "N4", "tipo_poste": "PDT11/1500", "base_concreto": "BC", "polygon": [(150, 180), (220, 0), (600, 0), (600, 60), (150, 180)], "id": "ms10"},
        {"estru_mt_nv1": "N2", "tipo_poste": "PDT11/600", "base_concreto": "BC", "polygon": [(150, 180), (150, 0), (220, 0), (150, 180)], "id": "ms11"},
        {"estru_mt_nv1": "N1", "tipo_poste": "PDT11/600", "base_concreto": "BC", "polygon": [(-1, 100), (-1, 180), (150, 180), (150, 0), (60, 0), (-1, 100)], "id": "ms12"},
        {"estru_mt_nv1": "N1", "tipo_poste": "PDT11/300", "polygon": [(-1, 0), (-1, 100), (60, 0), (-1, 0)], "id": "ms13"},        
    ]


    abacos["10102"] = [
    {"estru_mt_nv1": "UP3", "tipo_poste": "DT10/300", "rotacao_poste": "TOPO2", "tang_ou_enc": "ENC", "polygon": [(1100, 35), (1000, 35), (1000, 0), (1100, 0), (1100, 35)], "id": "ms10"},
    {"estru_mt_nv1": "UP3", "tipo_poste": "EXIST", "rotacao_poste": "TOPO2", "tang_ou_enc": "ENC", "polygon": [(1200, 35), (1100, 35), (1100, 0), (1200, 0), (1200, 35)], "id": "ms11"},
    {"estru_mt_nv1": "UP3", "tipo_poste": "EXIST", "estai_ancora": "1ES", "rotacao_poste": "TOPO2", "tang_ou_enc": "ENC", "polygon": [(1200, 110), (1100, 110), (1100, 35), (1200, 35), (1200, 110)], "id": "ms12"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/1000", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "BISS2", "tang_ou_enc": "ENC", "polygon": [(1400, 500), (1300, 500), (1300, 240), (1400, 240), (1400, 500)], "id": "ms16"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/600", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "BISS2", "tang_ou_enc": "ENC", "polygon": [(1400, 240), (1300, 240), (1300, 220), (1300, 0), (1400, 0), (1400, 240)], "id": "ms15"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/1000", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "TOPO2", "tang_ou_enc": "ENC", "polygon": [(1300, 500), (1200, 500), (1200, 240), (1300, 240), (1300, 500)], "id": "ms14"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/600", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "TOPO2", "tang_ou_enc": "ENC", "polygon": [(1300, 240), (1200, 240), (1200, 220), (1200, 0), (1300, 0), (1300, 240)], "id": "ms13"},
    {"estru_mt_nv1": "UP3", "tipo_poste": "DT10/1000", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "TOPO1", "tang_ou_enc": "ENC", "polygon": [(1000, 500), (900, 500), (900, 240), (1000, 240), (1000, 500)], "id": "ms09"},
    {"estru_mt_nv1": "UP3", "tipo_poste": "DT10/600", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "TOPO1", "tang_ou_enc": "ENC", "polygon": [(1000, 240), (900, 240), (900, 220), (900, 0), (1000, 0), (1000, 240)], "id": "ms08"},
    {"estru_mt_nv1": "UP3UP3", "tipo_poste": "DT10/1000", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "TOPO1", "tang_ou_enc": "ENC", "polygon": [(900, 220), (600, 220), (600, 100), (600, 0), (900, 0), (900, 220)], "id": "ms07"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/600", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "BISS2", "tang_ou_enc": "ENC", "polygon": [(160, 300), (160, 220), (345, 0), (600, 0), (600, 100), (160, 300)], "id": "ms06"},
    {"estru_mt_nv1": "UP1", "tipo_poste": "DT10/600", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "BISS1", "tang_ou_enc": "TAN", "polygon": [(160, 220), (160, 0), (345, 0), (160, 220)], "id": "ms05"},
    {"estru_mt_nv1": "UP1", "tipo_poste": "DT10/300", "rotacao_poste": "BISS1", "tang_ou_enc": "TAN", "polygon": [(160, 220), (-1, 220), (-1, 0), (160, 0), (160, 220)], "id": "ms04"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/600", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "BISS2", "tang_ou_enc": "ENC", "polygon": [(160, 500), (-1, 500), (-1, 220), (160, 220), (160, 500)], "id": "ms01"},
    {"estru_mt_nv1": "UP3UP3", "tipo_poste": "DT11/1500", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "TOPO1", "tang_ou_enc": "ENC", "polygon": [(900, 500), (600, 500), (600, 220), (900, 220), (900, 500)], "id": "ms03"},
    {"estru_mt_nv1": "UP4", "tipo_poste": "DT10/1000", "base_concreto": "BC", "base_reforcada": "BC", "rotacao_poste": "BISS2", "tang_ou_enc": "ENC", "polygon": [(600, 500), (160, 500), (160, 300), (600, 100), (600, 500)], "id": "ms02"},     
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
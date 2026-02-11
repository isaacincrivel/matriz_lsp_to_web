"""
MÓDULO DE CATALOGAÇÃO DE MATERIAIS POR ESTRUTURA
================================================

Este módulo permite catalogar materiais e suas posições relativas dentro de estruturas
de rede de distribuição elétrica, facilitando a geração de listas para CAD.

USO:
    from backend.elementos.estrutura_materiais import (
        catalogar_material_estrutura,
        obter_materiais_estrutura,
        exportar_lista_cad
    )
    
    # Catalogar materiais de uma estrutura
    materiais = catalogar_material_estrutura("B3CE-PR", {
        "F-30": {"tipo": "Ferramenta", "posicao": (0, 0, 150), "quantidade": 1},
        "A-02": {"tipo": "Acessório", "posicao": (500, 0, 800), "quantidade": 1}
    })
    
    # Obter lista de materiais
    lista = obter_materiais_estrutura("B3CE-PR")
    
    # Exportar para CAD
    exportar_lista_cad("B3CE-PR", "lista_materiais.csv", coordenadas_base=(lat, lon))
"""

import sys
import os
import json
import csv
from typing import Dict, List, Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Dicionário global para armazenar catálogos de estruturas
CATALOGO_ESTRUTURAS = {}

# Estrutura padrão para armazenar materiais
ESTRUTURA_MATERIAL = {
    "codigo": "",           # Código do material (ex: "F-30", "A-02")
    "descricao": "",        # Descrição do material
    "tipo": "",             # Tipo: "Ferramenta", "Acessório", "Isolador", "Condutor", etc.
    "posicao_x": 0.0,       # Posição X relativa ao poste (mm)
    "posicao_y": 0.0,       # Posição Y relativa ao poste (mm)
    "posicao_z": 0.0,       # Posição Z (altura) relativa ao solo (mm)
    "quantidade": 1,        # Quantidade do material
    "unidade": "UN",        # Unidade de medida
    "angulo": 0.0,          # Ângulo de rotação (graus)
    "observacoes": ""       # Observações adicionais
}


def catalogar_material_estrutura(
    codigo_estrutura: str,
    materiais: Dict[str, Dict],
    descricao_estrutura: str = ""
) -> bool:
    """
    Catalogar materiais de uma estrutura específica.
    
    Args:
        codigo_estrutura: Código da estrutura (ex: "B3CE-PR", "UP1", "UP4")
        materiais: Dicionário com materiais no formato:
                  {
                      "F-30": {
                          "descricao": "Ferramenta tipo 30",
                          "tipo": "Ferramenta",
                          "posicao": (x, y, z),  # em mm
                          "quantidade": 1,
                          "angulo": 0.0,
                          "observacoes": ""
                      },
                      ...
                  }
        descricao_estrutura: Descrição opcional da estrutura
    
    Returns:
        bool: True se catalogou com sucesso
    """
    try:
        if codigo_estrutura not in CATALOGO_ESTRUTURAS:
            CATALOGO_ESTRUTURAS[codigo_estrutura] = {
                "codigo": codigo_estrutura,
                "descricao": descricao_estrutura,
                "materiais": []
            }
        
        estrutura = CATALOGO_ESTRUTURAS[codigo_estrutura]
        
        # Adiciona ou atualiza materiais
        for codigo_material, dados in materiais.items():
            # Verifica se o material já existe
            material_existente = None
            for mat in estrutura["materiais"]:
                if mat["codigo"] == codigo_material:
                    material_existente = mat
                    break
            
            # Prepara dados do material
            posicao = dados.get("posicao", (0, 0, 0))
            if isinstance(posicao, tuple) and len(posicao) >= 3:
                x, y, z = posicao[0], posicao[1], posicao[2]
            else:
                x, y, z = 0, 0, 0
            
            material_data = {
                "codigo": codigo_material,
                "descricao": dados.get("descricao", ""),
                "tipo": dados.get("tipo", ""),
                "posicao_x": float(x),
                "posicao_y": float(y),
                "posicao_z": float(z),
                "quantidade": int(dados.get("quantidade", 1)),
                "unidade": dados.get("unidade", "UN"),
                "angulo": float(dados.get("angulo", 0.0)),
                "observacoes": dados.get("observacoes", "")
            }
            
            if material_existente:
                # Atualiza material existente
                material_existente.update(material_data)
            else:
                # Adiciona novo material
                estrutura["materiais"].append(material_data)
        
        return True
    except Exception as e:
        print(f"Erro ao catalogar materiais: {e}")
        return False


def obter_materiais_estrutura(codigo_estrutura: str) -> List[Dict]:
    """
    Obter lista de materiais de uma estrutura.
    
    Args:
        codigo_estrutura: Código da estrutura
    
    Returns:
        List[Dict]: Lista de materiais catalogados
    """
    if codigo_estrutura in CATALOGO_ESTRUTURAS:
        return CATALOGO_ESTRUTURAS[codigo_estrutura]["materiais"].copy()
    return []


def obter_todas_estruturas() -> Dict[str, Dict]:
    """
    Obter catálogo completo de todas as estruturas.
    
    Returns:
        Dict: Dicionário com todas as estruturas catalogadas
    """
    return CATALOGO_ESTRUTURAS.copy()


def exportar_lista_cad(
    codigo_estrutura: str,
    nome_arquivo: str,
    coordenadas_base: Optional[Tuple[float, float]] = None,
    formato: str = "CSV"
) -> bool:
    """
    Exportar lista de materiais para formato CAD.
    
    Args:
        codigo_estrutura: Código da estrutura
        nome_arquivo: Nome do arquivo de saída
        coordenadas_base: Tupla (lat, lon) para converter coordenadas relativas em absolutas
        formato: Formato de exportação ("CSV" ou "DXF")
    
    Returns:
        bool: True se exportou com sucesso
    """
    try:
        if codigo_estrutura not in CATALOGO_ESTRUTURAS:
            print(f"Estrutura '{codigo_estrutura}' não encontrada no catálogo")
            return False
        
        estrutura = CATALOGO_ESTRUTURAS[codigo_estrutura]
        materiais = estrutura["materiais"]
        
        if formato.upper() == "CSV":
            return _exportar_csv(materiais, nome_arquivo, coordenadas_base)
        elif formato.upper() == "DXF":
            return _exportar_dxf(materiais, nome_arquivo, coordenadas_base)
        else:
            print(f"Formato '{formato}' não suportado. Use 'CSV' ou 'DXF'")
            return False
    
    except Exception as e:
        print(f"Erro ao exportar lista CAD: {e}")
        return False


def _exportar_csv(
    materiais: List[Dict],
    nome_arquivo: str,
    coordenadas_base: Optional[Tuple[float, float]] = None
) -> bool:
    """
    Exportar materiais para CSV.
    
    Args:
        materiais: Lista de materiais
        nome_arquivo: Nome do arquivo
        coordenadas_base: Coordenadas base (lat, lon)
    """
    try:
        # Cria pasta resultados se não existir
        pasta_resultados = "resultados"
        if not os.path.exists(pasta_resultados):
            os.makedirs(pasta_resultados)
        
        caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
        
        with open(caminho_completo, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            
            # Cabeçalho
            writer.writerow([
                "Código",
                "Descrição",
                "Tipo",
                "Posição X (mm)",
                "Posição Y (mm)",
                "Posição Z (mm)",
                "Quantidade",
                "Unidade",
                "Ângulo (°)",
                "Observações"
            ])
            
            # Dados
            for mat in materiais:
                writer.writerow([
                    mat.get("codigo", ""),
                    mat.get("descricao", ""),
                    mat.get("tipo", ""),
                    f"{mat.get('posicao_x', 0):.2f}".replace('.', ','),
                    f"{mat.get('posicao_y', 0):.2f}".replace('.', ','),
                    f"{mat.get('posicao_z', 0):.2f}".replace('.', ','),
                    mat.get("quantidade", 1),
                    mat.get("unidade", "UN"),
                    f"{mat.get('angulo', 0):.2f}".replace('.', ','),
                    mat.get("observacoes", "")
                ])
        
        print(f"✅ Lista de materiais exportada: {os.path.abspath(caminho_completo)}")
        return True
    
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")
        return False


def _exportar_dxf(
    materiais: List[Dict],
    nome_arquivo: str,
    coordenadas_base: Optional[Tuple[float, float]] = None
) -> bool:
    """
    Exportar materiais para DXF (formato simplificado).
    
    Args:
        materiais: Lista de materiais
        nome_arquivo: Nome do arquivo
        coordenadas_base: Coordenadas base (lat, lon)
    """
    try:
        # Cria pasta resultados se não existir
        pasta_resultados = "resultados"
        if not os.path.exists(pasta_resultados):
            os.makedirs(pasta_resultados)
        
        caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
        
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            # Cabeçalho DXF básico
            f.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n")
            f.write("0\nSECTION\n2\nTABLES\n0\nENDSEC\n")
            f.write("0\nSECTION\n2\nBLOCKS\n0\nENDSEC\n")
            f.write("0\nSECTION\n2\nENTITIES\n")
            
            # Adiciona pontos para cada material
            for mat in materiais:
                x = mat.get('posicao_x', 0) / 1000.0  # Converte mm para metros
                y = mat.get('posicao_y', 0) / 1000.0
                z = mat.get('posicao_z', 0) / 1000.0
                
                # Cria um ponto no DXF
                f.write(f"0\nPOINT\n")
                f.write(f"8\n0\n")  # Layer
                f.write(f"10\n{x:.6f}\n")  # X
                f.write(f"20\n{y:.6f}\n")  # Y
                f.write(f"30\n{z:.6f}\n")  # Z
                
                # Adiciona texto com código do material
                f.write(f"0\nTEXT\n")
                f.write(f"8\n0\n")  # Layer
                f.write(f"10\n{x:.6f}\n")  # X
                f.write(f"20\n{y:.6f}\n")  # Y
                f.write(f"30\n{z:.6f}\n")  # Z
                f.write(f"40\n0.5\n")  # Altura do texto
                f.write(f"1\n{mat.get('codigo', '')}\n")  # Texto
            
            f.write("0\nENDSEC\n")
            f.write("0\nEOF\n")
        
        print(f"✅ Arquivo DXF exportado: {os.path.abspath(caminho_completo)}")
        return True
    
    except Exception as e:
        print(f"Erro ao exportar DXF: {e}")
        return False


def salvar_catalogo_arquivo(nome_arquivo: str = "catalogo_estruturas.json") -> bool:
    """
    Salvar catálogo completo em arquivo JSON.
    
    Args:
        nome_arquivo: Nome do arquivo JSON
    
    Returns:
        bool: True se salvou com sucesso
    """
    try:
        pasta_resultados = "resultados"
        if not os.path.exists(pasta_resultados):
            os.makedirs(pasta_resultados)
        
        caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
        
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            json.dump(CATALOGO_ESTRUTURAS, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Catálogo salvo: {os.path.abspath(caminho_completo)}")
        return True
    
    except Exception as e:
        print(f"Erro ao salvar catálogo: {e}")
        return False


def carregar_catalogo_arquivo(nome_arquivo: str = "catalogo_estruturas.json") -> bool:
    """
    Carregar catálogo de arquivo JSON.
    
    Args:
        nome_arquivo: Nome do arquivo JSON
    
    Returns:
        bool: True se carregou com sucesso
    """
    try:
        pasta_resultados = "resultados"
        caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
        
        if not os.path.exists(caminho_completo):
            print(f"Arquivo não encontrado: {caminho_completo}")
            return False
        
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            global CATALOGO_ESTRUTURAS
            CATALOGO_ESTRUTURAS = json.load(f)
        
        print(f"✅ Catálogo carregado: {os.path.abspath(caminho_completo)}")
        return True
    
    except Exception as e:
        print(f"Erro ao carregar catálogo: {e}")
        return False

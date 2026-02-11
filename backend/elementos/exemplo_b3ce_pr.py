"""
EXEMPLO: Estrutura B3CE-PR - Catalogação de Materiais
======================================================

Este script demonstra como catalogar materiais da estrutura B3CE-PR
(baseado no desenho técnico fornecido).

A estrutura B3CE-PR é uma estrutura de transição entre rede convencional
e rede compacta, com dois postes e múltiplos componentes.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.elementos.estrutura_materiais import (
    catalogar_material_estrutura,
    exportar_lista_cad,
    salvar_catalogo_arquivo
)


def catalogar_b3ce_pr():
    """
    Catalogar materiais da estrutura B3CE-PR.
    
    Baseado no desenho técnico:
    - Estrutura de transição rede convencional com rede compacta
    - Dois postes verticais
    - Múltiplos componentes com códigos alfanuméricos
    """
    
    # POSTE ESQUERDO (Rede Convencional)
    materiais_poste_esquerdo = {
        # Componentes do nível 1 (800-13,8kV)
        "F-30": {
            "descricao": "Ferramenta tipo 30",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 800),  # X, Y, Z em mm (altura 800mm = 0,8m)
            "quantidade": 1,
            "observacoes": "Nível 1 - 13,8kV"
        },
        "A-02": {
            "descricao": "Acessório tipo 02",
            "tipo": "Acessório",
            "posicao": (500, 0, 800),
            "quantidade": 1,
            "observacoes": "Nível 1"
        },
        "0-02": {
            "descricao": "Componente 0-02",
            "tipo": "Acessório",
            "posicao": (450, 0, 800),
            "quantidade": 1
        },
        
        # Componentes do nível 2 (1000-23,1kV)
        "F-42": {
            "descricao": "Ferramenta tipo 42",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 1000),
            "quantidade": 1,
            "observacoes": "Nível 2 - 23,1kV"
        },
        
        # Componentes do nível 3 (1000-34,5kV)
        "C-01": {
            "descricao": "Componente C-01",
            "tipo": "Acessório",
            "posicao": (0, 0, 1000),
            "quantidade": 1,
            "observacoes": "Nível 3 - 34,5kV"
        },
        
        # Aterramento
        "MALHA_ATER": {
            "descricao": "Malha de aterramento",
            "tipo": "Aterramento",
            "posicao": (0, -500, 0),  # Abaixo do solo
            "quantidade": 1,
            "observacoes": "P/ malha de aterramento"
        }
    }
    
    # POSTE DIREITO (Rede Compacta)
    materiais_poste_direito = {
        # Componentes diversos
        "0-01": {
            "descricao": "Componente 0-01",
            "tipo": "Acessório",
            "posicao": (0, 0, 150),  # Altura 150mm
            "quantidade": 1
        },
        "A-16": {
            "descricao": "Acessório tipo 16",
            "tipo": "Acessório",
            "posicao": (0, 0, 150),
            "quantidade": 1
        },
        "M-04": {
            "descricao": "Material M-04",
            "tipo": "Acessório",
            "posicao": (0, 0, 200),
            "quantidade": 1
        },
        "F-40": {
            "descricao": "Ferramenta tipo 40",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 300),
            "quantidade": 1
        },
        "F-13": {
            "descricao": "Ferramenta tipo 13",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 400),
            "quantidade": 1
        },
        "M-09": {
            "descricao": "Material M-09",
            "tipo": "Acessório",
            "posicao": (0, 0, 500),
            "quantidade": 1
        },
        "F-34": {
            "descricao": "Ferramenta tipo 34",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 600),
            "quantidade": 1
        },
        "A-02": {
            "descricao": "Acessório tipo 02",
            "tipo": "Acessório",
            "posicao": (0, 0, 600),
            "quantidade": 1
        },
        "I-06": {
            "descricao": "Isolador tipo 06",
            "tipo": "Isolador",
            "posicao": (0, 0, 700),
            "quantidade": 1
        },
        "F-22": {
            "descricao": "Ferramenta tipo 22",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 700),
            "quantidade": 1
        },
        "F-30": {
            "descricao": "Ferramenta tipo 30",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 800),
            "quantidade": 1
        },
        "A-02": {
            "descricao": "Acessório tipo 02",
            "tipo": "Acessório",
            "posicao": (0, 0, 800),
            "quantidade": 1
        },
        "C-11": {
            "descricao": "Componente C-11",
            "tipo": "Acessório",
            "posicao": (0, 0, 900),
            "quantidade": 1
        },
        "I-07": {
            "descricao": "Isolador tipo 07",
            "tipo": "Isolador",
            "posicao": (0, 0, 1000),
            "quantidade": 1
        },
        "E-29": {
            "descricao": "Equipamento E-29",
            "tipo": "Equipamento",
            "posicao": (0, 0, 1100),
            "quantidade": 1
        },
        "F-35": {
            "descricao": "Ferramenta tipo 35",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 1200),
            "quantidade": 1
        },
        "F-31": {
            "descricao": "Ferramenta tipo 31",
            "tipo": "Ferramenta",
            "posicao": (0, 0, 1300),
            "quantidade": 1
        },
        "A-02": {
            "descricao": "Acessório tipo 02",
            "tipo": "Acessório",
            "posicao": (0, 0, 1300),
            "quantidade": 1
        }
    }
    
    # Catalogar estrutura completa (combinando ambos os postes)
    materiais_completos = {**materiais_poste_esquerdo, **materiais_poste_direito}
    
    # Adiciona prefixo para diferenciar postes
    materiais_finais = {}
    for codigo, dados in materiais_poste_esquerdo.items():
        materiais_finais[f"POSTE1_{codigo}"] = dados.copy()
        materiais_finais[f"POSTE1_{codigo}"]["observacoes"] = f"Poste Esquerdo - {dados.get('observacoes', '')}"
    
    for codigo, dados in materiais_poste_direito.items():
        # Ajusta posição X para o poste direito (assumindo 5m de distância)
        dados_ajustados = dados.copy()
        pos_original = dados.get("posicao", (0, 0, 0))
        dados_ajustados["posicao"] = (pos_original[0] + 5000, pos_original[1], pos_original[2])
        materiais_finais[f"POSTE2_{codigo}"] = dados_ajustados
        materiais_finais[f"POSTE2_{codigo}"]["observacoes"] = f"Poste Direito - {dados.get('observacoes', '')}"
    
    # Catalogar
    sucesso = catalogar_material_estrutura(
        codigo_estrutura="B3CE-PR",
        materiais=materiais_finais,
        descricao_estrutura="Estrutura de transição rede convencional com rede compacta"
    )
    
    if sucesso:
        print("✅ Estrutura B3CE-PR catalogada com sucesso!")
        print(f"   Total de materiais: {len(materiais_finais)}")
        
        # Exportar para CAD
        exportar_lista_cad(
            codigo_estrutura="B3CE-PR",
            nome_arquivo="lista_materiais_B3CE-PR.csv",
            formato="CSV"
        )
        
        # Salvar catálogo completo
        salvar_catalogo_arquivo("catalogo_estruturas.json")
        
        return True
    else:
        print("❌ Erro ao catalogar estrutura B3CE-PR")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("CATALOGAÇÃO DE MATERIAIS - ESTRUTURA B3CE-PR")
    print("=" * 80)
    print()
    
    catalogar_b3ce_pr()
    
    print()
    print("=" * 80)
    print("✅ Processo concluído!")
    print("=" * 80)
    print()
    print("Arquivos gerados:")
    print("  - resultados/lista_materiais_B3CE-PR.csv")
    print("  - resultados/catalogo_estruturas.json")
    print()
    print("Próximos passos:")
    print("  1. Abra o CSV no Excel ou CAD")
    print("  2. Use as coordenadas X, Y, Z para posicionar materiais no desenho")
    print("  3. As coordenadas estão em milímetros (mm)")
    print("  4. Posição X, Y é relativa ao centro do poste")
    print("  5. Posição Z é a altura relativa ao solo")

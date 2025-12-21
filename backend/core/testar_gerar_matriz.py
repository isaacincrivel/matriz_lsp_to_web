#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar e depurar a função gerar_matriz diretamente.
Execute este arquivo para depurar sem precisar do frontend ou arquivo JSON.

Uso:
    python backend/core/testar_gerar_matriz.py
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.matriz_csv_to_kml import testar_gerar_matriz

if __name__ == "__main__":
    print("Iniciando teste de gerar_matriz...")
    print("(Certifique-se de que o breakpoint está ativado em matriz_csv_to_kml.py se quiser depurar)")
    print()
    
    try:
        matriz = testar_gerar_matriz()
        print("\n✅ Teste concluído com sucesso!")
    except Exception as e:
        print(f"\nErro durante o teste: {e}")
        sys.exit(1)


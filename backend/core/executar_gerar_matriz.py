#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para executar gerar_matriz diretamente a partir de dados JSON
Pode ser chamado do JavaScript para depuração
"""
import sys
import os
import json

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.matriz_csv_to_kml import gerar_matriz

def main():
    """Função principal que lê JSON do stdin ou arquivo"""
    try:
        # Tenta ler do stdin primeiro (para pipe)
        if not sys.stdin.isatty():
            data = json.load(sys.stdin)
        else:
            # Se não há stdin, tenta ler de arquivo passado como argumento
            if len(sys.argv) > 1:
                with open(sys.argv[1], 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                print("Erro: Nenhum dado fornecido. Use stdin ou passe um arquivo JSON como argumento.")
                print("Exemplo: python executar_gerar_matriz.py dados.json")
                sys.exit(1)
        
        # Extrai os parâmetros
        trecho = data.get("trecho", "T001")
        module_name = data.get("module_name")
        module_data = data.get("module_data", {})
        loose_gap = data.get("loose_gap", "NÃO")
        section_size = data.get("section_size", 80)
        gap_size = data.get("gap_size", 800)
        num_poste_inicial = data.get("num_poste_inicial", "00000000")
        tipo_poste = data.get("tipo_poste", "")
        lista_nao_intercalar = data.get("lista_nao_intercalar", [])
        vertices = data.get("vertices")
        
        # Validações
        if not module_name:
            raise ValueError("module_name é obrigatório")
        if vertices is None:
            raise ValueError("vertices é obrigatório")
        
        print("Executando gerar_matriz com:")
        print(f"  - trecho: {trecho}")
        print(f"  - module_name: {module_name}")
        print(f"  - loose_gap: {loose_gap}")
        print(f"  - section_size: {section_size}")
        print(f"  - gap_size: {gap_size}")
        print(f"  - num_poste_inicial: {num_poste_inicial}")
        print(f"  - tipo_poste: {tipo_poste}")
        print(f"  - lista_nao_intercalar: {lista_nao_intercalar}")
        print(f"  - vertices: {len(vertices)} vertices")
        print()
        print(">>>>> O codigo vai PAUSAR no pdb.set_trace() agora <<<<<")
        print(">>>>> Use os comandos do PDB para depurar (n, s, c, q) <<<<<")
        print()
        
        # Chama a função gerar_matriz
        # O pdb.set_trace() dentro da função vai pausar aqui se estiver ativado
        matriz = gerar_matriz(
            trecho=trecho,
            module_name=module_name,
            module_data=module_data,
            loose_gap=loose_gap,
            section_size=section_size,
            gap_size=gap_size,
            num_poste_inicial=num_poste_inicial,
            tipo_poste=tipo_poste,
            lista_nao_intercalar=lista_nao_intercalar,
            vertices_kml=vertices  # Usa vertices_kml como parâmetro
        )
        
        print(f"\nMatriz gerada com sucesso!")
        print(f"Total de registros: {len(matriz)}")
        
        # Salva o resultado em JSON para o JavaScript ler
        resultado = {
            'success': True,
            'data': matriz.to_dict('records'),
            'total_records': len(matriz)
        }
        
        # Salva em arquivo temporário
        output_file = 'temp_matriz_resultado.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"Resultado salvo em: {output_file}")
        
        # Também imprime no stdout para caso seja usado via pipe
        print(json.dumps(resultado, ensure_ascii=False, default=str))
        
    except Exception as e:
        import traceback
        error_info = {
            'success': False,
            'message': str(e),
            'traceback': traceback.format_exc()
        }
        print(json.dumps(error_info, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()


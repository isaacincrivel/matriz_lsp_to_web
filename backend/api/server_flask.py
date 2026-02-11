#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Servidor Flask para API REST do Sistema Matriz
Expõe endpoints para gerar matriz CSV/KML
"""
import sys
import os
import base64
import io
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.matriz_csv_to_kml import gerar_matriz
from backend.exportacao.exportacao import salvar_csv
from backend.exportacao.kml import criar_kml_quadrados_bissetriz
import pandas as pd

app = Flask(__name__)

## trecho incluido para resolver erro de CORS
from flask import make_response

# Configuração de CORS
# Em produção, restrinja aos domínios permitidos
# Em desenvolvimento, permite todos
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*')

if allowed_origins == '*':
    # Desenvolvimento: permite todos
    CORS(app)
    print("[CORS] Modo desenvolvimento: Permitindo todas as origens")
else:
    # Produção: lista específica de domínios
    origins = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, resources={
        r"/api/*": {
            "origins": origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    print(f"[CORS] Modo produção: Permitindo origens: {origins}")

# Configuração para servir frontend na raiz
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend', 'desktop_app')

@app.route('/api/test/', methods=['GET'])
def test():
    """Endpoint de teste para verificar se o servidor está rodando"""
    return jsonify({
        'status': 'ok',
        'message': 'Servidor Flask está funcionando',
        'version': '1.0'
    })

@app.route('/api/gerar-matriz/', methods=['POST', 'OPTIONS'])
def gerar_matriz_api():
    """
    Endpoint principal para gerar matriz CSV/KML
    
    Parâmetros esperados no JSON:
    - trecho: string
    - module_name: string (ex: "10105")
    - module_data: objeto (dados do módulo da tabela)
    - loose_gap: string ("SIM" ou "NÃO")
    - section_size: number (vao_medio)
    - gap_size: number (tramo_max)
    - num_poste_inicial: string (ex: "00000000")
    - tipo_poste: string ("Implantar" ou "Existente")
    - lista_nao_intercalar: array de números
    - vertices: array de arrays [[lat, lon, sequencia], ...]
    """

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.get_json(silent=True)
        # linha para depurar codigo (evita erro em requisições sem JSON)
        print("\nCHEGOU NA API →\n", data)
        if not data:
            return jsonify({
                'success': False,
                'message': 'JSON inválido ou vazio'
            }), 400
        
        # Extrai parâmetros
        trecho = data.get("trecho", "T001")
        module_name = data.get("module_name")
        module_data = data.get("module_data", {})
        loose_gap = data.get("loose_gap", "NÃO")
        section_size = data.get("section_size", 80)
        gap_size = data.get("gap_size", 700)
        num_poste_inicial = data.get("num_poste_inicial", "00000000")
        tipo_poste = data.get("tipo_poste", "Existente")
        lista_nao_intercalar = data.get("lista_nao_intercalar", [])
        vertices = data.get("vertices", [])
        
        # Validações
        if not module_name:
            return jsonify({
                'success': False,
                'message': 'module_name é obrigatório'
            }), 400
        
        if not vertices or len(vertices) == 0:
            return jsonify({
                'success': False,
                'message': 'vertices é obrigatório e não pode estar vazio'
            }), 400
        
        # Garante que tipo_poste tem valor padrão
        if not tipo_poste or tipo_poste.strip() == '':
            tipo_poste = "Existente"
        
        print(f"[API] Gerando matriz para trecho: {trecho}, módulo: {module_name}")
        print(f"[API] Vértices recebidos: {len(vertices)}")
        print(f"[API] Parâmetros: loose_gap={loose_gap}, section_size={section_size}, gap_size={gap_size}")
        print(f"[API] tipo_poste={tipo_poste}, lista_nao_intercalar={lista_nao_intercalar}")
        
        # Chama a função principal gerar_matriz com tratamento de erro detalhado
        try:
            print(f"[API] Chamando gerar_matriz()...")
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
                vertices_kml=vertices
            )
            print(f"[API] ✅ Matriz gerada com {len(matriz)} registros")
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"\n{'='*80}")
            print(f"[API] ❌ ERRO ao chamar gerar_matriz():")
            print(f"{'='*80}")
            print(f"Tipo do erro: {type(e).__name__}")
            print(f"Mensagem: {str(e)}")
            print(f"\nStack trace completo:")
            print(error_traceback)
            print(f"{'='*80}\n")
            raise  # Re-raise para ser capturado pelo handler externo
        
        # Gera CSV em memória
        csv_buffer = io.StringIO()
        # Usa ponto e vírgula como separador e vírgula como decimal (formato brasileiro)
        matriz.to_csv(csv_buffer, sep=';', decimal=',', index=False, encoding='utf-8-sig')
        csv_content = csv_buffer.getvalue()
        csv_base64 = base64.b64encode(csv_content.encode('utf-8-sig')).decode('utf-8')
        
        # Gera KML - a função criar_kml_quadrados_bissetriz cria na pasta "resultados"
        # Vamos usar pasta temporária e depois limpar
        import tempfile
        import shutil
        
        kml_filename = f"{trecho}_quadrados_bissetriz.kml"
        
        # Cria diretório temporário para trabalhar
        temp_dir = tempfile.mkdtemp(prefix=f"matriz_api_{os.getpid()}_")
        old_cwd = os.getcwd()
        
        try:
            # Muda para diretório temporário
            os.chdir(temp_dir)
            
            # Cria o KML (a função cria na pasta "resultados" relativa ao diretório atual)
            criar_kml_quadrados_bissetriz(matriz, kml_filename)
            
            # Lê o KML gerado (está em resultados/kml_filename)
            resultado_kml_path = os.path.join("resultados", kml_filename)
            if not os.path.exists(resultado_kml_path):
                raise Exception(f'Arquivo KML não foi gerado: {resultado_kml_path}')
            
            with open(resultado_kml_path, 'r', encoding='utf-8') as f:
                kml_content = f.read()
            
            kml_base64 = base64.b64encode(kml_content.encode('utf-8')).decode('utf-8')
                
        finally:
            # Restaura diretório original
            os.chdir(old_cwd)
            # Remove diretório temporário
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"[API] Aviso: Não foi possível remover diretório temporário {temp_dir}: {e}")
                pass
        
        # Nomes dos arquivos
        csv_filename = f"{trecho}_matriz_resultado.csv"
        
        # Retorna resposta
        response = jsonify({
            'success': True,
            'message': f'Matriz gerada com sucesso! {len(matriz)} registros.',
            'data': matriz.to_dict('records'),  # Dados da matriz em JSON
            'csv_content': csv_base64,
            'csv_filename': csv_filename,
            'kml_content': kml_base64,
            'kml_filename': kml_filename,
            'total_records': len(matriz)
        })
        
        # CORS headers
        response.headers.add('Access-Control-Allow-Origin', '*')
        
        return response
        
    except KeyError as e:
        return jsonify({
            'success': False,
            'message': f'Parâmetro obrigatório faltando: {str(e)}'
        }), 400
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        
        print(f"\n{'='*80}")
        print(f"[API] ❌ ERRO CAPTURADO NO HANDLER:")
        print(f"{'='*80}")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print(f"\nStack trace completo:")
        print(error_traceback)
        print(f"{'='*80}\n")
        
        # Extrai informações úteis do erro
        error_info = {
            'type': type(e).__name__,
            'message': str(e),
            'file': None,
            'line': None,
            'function': None
        }
        
        # Tenta extrair informações do traceback
        tb_lines = error_traceback.split('\n')
        for i, line in enumerate(tb_lines):
            if 'File "' in line and 'line' in line:
                # Extrai nome do arquivo e linha
                import re
                match = re.search(r'File "([^"]+)", line (\d+)', line)
                if match:
                    error_info['file'] = match.group(1)
                    error_info['line'] = match.group(2)
                # Próxima linha geralmente tem a função
                if i + 1 < len(tb_lines):
                    func_match = re.search(r'in (\w+)', tb_lines[i + 1])
                    if func_match:
                        error_info['function'] = func_match.group(1)
                break
        
        response = jsonify({
            'success': False,
            'message': f'Erro ao gerar matriz: {str(e)}',
            'error_type': error_info['type'],
            'error_file': error_info['file'],
            'error_line': error_info['line'],
            'error_function': error_info['function'],
            'traceback': error_traceback
        })
        response.status_code = 500
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

# Rotas para servir frontend (devem vir DEPOIS das rotas da API)
@app.route('/')
def index():
    """Serve o frontend na raiz do domínio"""
    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    
    # Verifica se o arquivo existe
    if not os.path.exists(index_path):
        print(f"❌ Erro: Arquivo não encontrado: {index_path}")
        print(f"📁 FRONTEND_DIR: {FRONTEND_DIR}")
        print(f"📁 Diretório atual: {os.getcwd()}")
        print(f"📁 Conteúdo de FRONTEND_DIR: {os.listdir(FRONTEND_DIR) if os.path.exists(FRONTEND_DIR) else 'DIRETÓRIO NÃO EXISTE'}")
        from flask import abort
        abort(500)
    
    try:
        return send_file(index_path)
    except Exception as e:
        print(f"❌ Erro ao servir index.html: {e}")
        from flask import abort
        abort(500)

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos do frontend (CSS, JS, imagens, etc.)"""
    # Ignora rotas da API (já processadas acima)
    if filename.startswith('api/'):
        from flask import abort
        abort(404)
    
    # Serve arquivos do frontend
    file_path = os.path.join(FRONTEND_DIR, filename)
    
    # Verifica se o arquivo existe
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        from flask import abort
        abort(404)
    
    try:
        return send_from_directory(FRONTEND_DIR, filename)
    except Exception as e:
        print(f"❌ Erro ao servir arquivo {filename}: {e}")
        from flask import abort
        abort(404)

if __name__ == '__main__':
    import socket
    import os
    
    # Em produção, usa PORT da variável de ambiente (Heroku, Railway, etc.)
    # Em desenvolvimento, procura porta disponível (8000-8009)
    port = int(os.environ.get('PORT', 0))
    
    if port == 0:
        # Modo desenvolvimento: procura porta disponível
        for attempt in range(10):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', 8000 + attempt))
                sock.close()
                port = 8000 + attempt
                break
            except OSError:
                if attempt == 9:
                    print("❌ Nenhuma porta disponível entre 8000-8009")
                    sys.exit(1)
                continue
    
    # Detecta se está em produção (Heroku, Railway, etc. definem PORT)
    is_production = os.environ.get('PORT') is not None
    debug_mode = not is_production
    
    print("=" * 80)
    print("🚀 Servidor Flask iniciando...")
    print("=" * 80)
    if is_production:
        print("🌐 Modo: PRODUÇÃO")
    else:
        print("🔧 Modo: DESENVOLVIMENTO")
    print(f"📡 API disponível em: http://0.0.0.0:{port}/api/gerar-matriz/")
    print(f"🧪 Teste: http://0.0.0.0:{port}/api/test/")
    print("=" * 80)
    if not is_production:
        print("Pressione Ctrl+C para parar o servidor")
        print("=" * 80)
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


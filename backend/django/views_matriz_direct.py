"""
View Django para chamar diretamente a função gerar_matriz do backend/core/matriz_csv_to_kml.py
"""
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.matriz_csv_to_kml import gerar_matriz

@csrf_exempt
def gerar_matriz_direct(request):
    """
    View que chama diretamente a função gerar_matriz do backend/core/matriz_csv_to_kml.py
    
    Parâmetros esperados no JSON:
    - trecho: string
    - module_name: string (ex: "MT7", "MT8")
    - module_data: objeto (dados do módulo da tabela)
    - loose_gap: string ("SIM" ou "NÃO")
    - section_size: number (vao_medio)
    - gap_size: number (tramo_max)
    - num_poste_inicial: string
    - tipo_poste: string
    - lista_nao_intercalar: array de números (índices)
    - vertices: array de arrays [[lat, lon, id], ...]
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Método não permitido. Use POST.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON inválido.")

    try:
        trecho = data["trecho"]
        module_name = data["module_name"]
        module_data = data.get("module_data", {})  # Opcional
        loose_gap = data["loose_gap"]
        section_size = data["section_size"]
        gap_size = data["gap_size"]
        num_poste_inicial = data["num_poste_inicial"]
        tipo_poste = data["tipo_poste"]
        lista_nao_intercalar = data.get("lista_nao_intercalar", [])
        vertices = data["vertices"]
    except KeyError as e:
        return HttpResponseBadRequest(f"Parâmetro obrigatório faltando: {e.args[0]}")

    try:
        # Chama a função Python diretamente
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
            vertices_kml=vertices  # Passa os vértices diretamente
        )
        
        # Converte DataFrame para dicionário para retornar como JSON
        matriz_dict = matriz.to_dict('records')
        
        return JsonResponse({
            'success': True,
            'data': matriz_dict,
            'message': 'Matriz gerada com sucesso'
        }, safe=False)
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Erro ao gerar matriz: {error_traceback}")
        return JsonResponse({
            'success': False,
            'message': f'Erro ao gerar matriz: {str(e)}',
            'traceback': error_traceback
        }, status=500)


from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .marcar_vertices_angulo_deflexao import InvalidAbacoException
import json
import random
from .models import Project
from . import utils
from .models import Module

# Create your views here.
def tela(request):
    return render(request, 'project.html')

def get_modules(request):
    all_modules = request.GET.get('all_modules', 'false').lower() == 'true'
    tensao = request.GET.get('tensao')
    local = request.GET.get('local')
    tipo_rede = request.GET.get('tipo_rede')
    fases = request.GET.get('fases')
    cabo = request.GET.get('cabo')

    queryset = Module.objects.all()

    if all_modules:
        return JsonResponse(list(queryset.values('id', 'nome', 'descricao')), safe=False)
    
    if tensao:
        queryset = queryset.filter(tensao__iexact=tensao)
    if local:
        queryset = queryset.filter(local__iexact=local)
    if tipo_rede:
        queryset = queryset.filter(tipo_rede__iexact=tipo_rede)
    if fases:
        queryset = queryset.filter(fases__iexact=fases)
    if cabo:
        queryset = queryset.filter(cabo__iexact=cabo)

    resultado = list(queryset.values('id', 'nome', 'tensao', 'local', 'tipo_rede', 'fases', 'cabo', 'descricao'))

    return JsonResponse(resultado, safe=False)

def get_module_params(request):
    module_id = request.GET.get('id')
    if not module_id:
        return HttpResponseBadRequest("ID do módulo é obrigatório.")

    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return HttpResponseBadRequest("Módulo não encontrado.")

    params = {
        'tensao': module.tensao,
        'local': module.local,
        'tipo_rede': module.tipo_rede,
        'fases': module.fases,
        'cabo': module.cabo,
        'descricao': module.descricao,
        'vao_limite_maximo': module.vao_limite_maximo,
        'vao_medio_maximo': module.vao_medio_maximo
    }

    return JsonResponse(params)

def get_module_optional_params(request):
    module_id = request.GET.get('id')
    if not module_id:
        return HttpResponseBadRequest("ID do módulo é obrigatório.")

    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return HttpResponseBadRequest("Módulo não encontrado.")

    optional_params = {
        'tipo_trafo': module.tipo_trafo,
        'telefone': module.telefone,
        'padmedicao': module.padmedicao,
        'notalig': module.notalig,
        'numero_projeto': module.numero_projeto,
        'poste_intercalado': module.poste_intercalado,
        'vao_frouxo': module.vao_frouxo,
        'plpt': module.plpt,
        'tramo': module.tramo,
        'cadunico': module.cadunico,
        'equipamento': module.equipamento,
        'ponto_equipamento': module.ponto_equipamento,
        'parcprojeto': module.parcprojeto,
        'emprconstrucao': module.emprconstrucao,
        'cliente': module.cliente,
        'mosaico_geral': module.mosaico_geral,
        'acesso_local': module.acesso_local,
        'kit_interno': module.kit_interno,
        'financiamentopad': module.financiamentopad,
        'linha_viva': module.linha_viva,
        'area_ambiental': module.area_ambiental,
        'carga_instalada': module.carga_instalada,
        'tip_orc_mod': module.tip_orc_mod
    }

    return JsonResponse(optional_params)

def generate_project_id(request):
    while True:
        novo_id = random.randint(10000000, 99999999)
        if not Project.objects.filter(id=novo_id).exists():
            break

    return JsonResponse({'id': novo_id})

@csrf_exempt
def gerar_matriz_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método não permitido. Use POST.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON inválido.")

    try:
        trecho = data["trecho"]
        num_poste_inicial = data["num_poste_inicial"]
        tipo_poste = data["tipo_poste"]
        vertices = data["vertices"]
        modulo = data["modulo"]
        comprimento_vao = data.get("comprimento_vano", 30)
        lista_nao_intercalar = data.get("lista_nao_intercalar", [])
    except KeyError as e:
        return HttpResponseBadRequest(f"Parâmetro obrigatório faltando: {e.args[0]}")

    # Recupera parâmetros do módulo
    module_name, section_size, loose_gap = utils.get_module(modulo)

    # Gera a matriz
    try:
        tabela_dict = utils.gerar_matriz(
            trecho, module_name, vertices,
            loose_gap, section_size, comprimento_vao,
            num_poste_inicial, tipo_poste, lista_nao_intercalar
        )
    except InvalidAbacoException as e:
        return JsonResponse({"message": str(e)}, status=422)
    print(tabela_dict)
    if tabela_dict:
        return JsonResponse(tabela_dict, safe=False)
    else:
        return JsonResponse({"message": "Não foi possível gerar a matriz."}, status=422)
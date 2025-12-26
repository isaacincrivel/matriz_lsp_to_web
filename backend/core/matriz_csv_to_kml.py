import pandas as pd

# Importando funções dos módulos organizados
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.calculo_geografico import distance, angle, polar, distance_ptos, angulo_deflexao
from backend.core.processamento_vertices import get_loose_gap, dividir_tramo, intercalar_vertices
from backend.core.transformacao_csv import transformar_csv_para_uma_linha_por_vertice
from backend.abacos.abaco_mosaico import mtz_abaco, point_in_polygon, mosaico
from backend.exportacao.exportacao import exportar_para_kml, salvar_csv
from backend.exportacao.kml import criar_kml_quadrados_bissetriz
from backend.elementos.colocar_encabecamento_rede import colocar_encabecamento_rede
from backend.elementos.colocar_poste_estrutura import colocar_poste_estrutura
from backend.elementos.marcar_vertices_angulo_deflexao import marcar_vertices_angulo_deflexao

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar, vertices_kml=None):
    """
    Gera a matriz de pontos com base nos parâmetros fornecidos.
    
    Args:
        trecho: string - Código do trecho
        module_name: string - Nome do módulo
        module_data: dict - Dados do módulo da tabela
        loose_gap: string - "SIM" ou "NÃO" para vão frouxo
        section_size: number - Vão médio (da tabela)
        gap_size: number - Tramo máximo (da tabela)
        num_poste_inicial: string - Número do poste inicial (sempre "00000000")
        tipo_poste: string - Tipo do poste ("Implantar" ou "Existente")
        lista_nao_intercalar: list - Lista de índices (base 0) onde não intercalar postes
        vertices_kml: list, optional - Lista de vértices do KML no formato [[lat, lon, sequencia], ...]
                                      Se fornecido, usa esses vértices ao invés de ler do CSV
    """
    # 🐛 BREAKPOINT PARA DEPURAÇÃO - Descomente a linha abaixo para ativar o debugger
    # import pdb; pdb.set_trace()  # Pausa aqui quando a função é chamada
    # Se vértices foram fornecidos, usa eles diretamente
    if vertices_kml is not None:
        # Cria um DataFrame simples a partir dos vértices KML
        vertices_data = []
        for i, v in enumerate(vertices_kml):
            if len(v) >= 2:
                sequencia = v[2] if len(v) > 2 else i
                vertices_data.append({
                    'sequencia': sequencia,
                    'lat': v[0],
                    'long': v[1]
                })
        
        matriz_teste_transformada = pd.DataFrame(vertices_data)
        matriz_teste_filtrada = matriz_teste_transformada.copy()
    else:
        # Transforma o CSV para uma linha por vértice (comportamento original)
        matriz_teste_transformada = transformar_csv_para_uma_linha_por_vertice("matriz_teste.csv")
        
        # Remove colunas duplicadas de forma mais robusta
        # Primeiro, identifica colunas duplicadas exatas
        colunas_duplicadas_exatas = matriz_teste_transformada.columns[matriz_teste_transformada.columns.duplicated()].tolist()
        if colunas_duplicadas_exatas:
            # Remove colunas duplicadas exatas, mantendo apenas a primeira
            matriz_teste_transformada = matriz_teste_transformada.loc[:, ~matriz_teste_transformada.columns.duplicated()]
        
        # Remove colunas com sufixos .1, .2, etc. (mantém apenas a primeira)
        colunas_unicas = []
        colunas_base_vistas = set()
        for col in matriz_teste_transformada.columns:
            col_base = col.split('.')[0]  # Remove sufixos .1, .2, etc.
            if col_base not in colunas_base_vistas:
                colunas_unicas.append(col)
                colunas_base_vistas.add(col_base)
            # Se já viu essa coluna base, pula (mantém apenas a primeira)
        
        matriz_teste_transformada = matriz_teste_transformada[colunas_unicas]
        
        # Garante que não há colunas duplicadas no índice das colunas
        if matriz_teste_transformada.columns.duplicated().any():
            matriz_teste_transformada = matriz_teste_transformada.loc[:, ~matriz_teste_transformada.columns.duplicated()]
        
        # Salva o CSV transformado para referência (atualiza o arquivo final)
        matriz_teste_transformada.to_csv("matriz_teste_transformada_final.csv", sep=";", decimal=",", index=False)
        
        # Usa o DataFrame transformado como base (já tem uma linha por vértice)
        matriz_teste_filtrada = matriz_teste_transformada.copy()
        
        # Garante que não há duplicatas e índices estão corretos
        matriz_teste_filtrada = matriz_teste_filtrada.drop_duplicates(subset=['sequencia'], keep='first')
        matriz_teste_filtrada = matriz_teste_filtrada.reset_index(drop=True)
    
    # Cria a lista de vértices dinamicamente a partir do DataFrame
    vertices = []
    for index, row in matriz_teste_filtrada.iterrows():
        # Verifica se as coordenadas não estão vazias
        lat_str = str(row['lat']).strip()
        lon_str = str(row['long']).strip()
        
        if lat_str == '' or lon_str == '' or lat_str == 'nan' or lon_str == 'nan':
            continue  # Pula linhas com coordenadas vazias
        
        # Converte coordenadas para float
        lat = float(lat_str.replace(',', '.')) if isinstance(lat_str, str) else float(lat_str)
        lon = float(lon_str.replace(',', '.')) if isinstance(lon_str, str) else float(lon_str)
        
        # Converte sequência para int de forma segura
        sequencia_valor = row['sequencia']
        if hasattr(sequencia_valor, 'iloc'):
            sequencia = int(sequencia_valor.iloc[0])
        elif hasattr(sequencia_valor, 'item'):
            sequencia = int(sequencia_valor.item())
        else:
            sequencia = int(sequencia_valor)
        
        # Adiciona o vértice à lista
        vertices.append((lat, lon, sequencia, ""))
    
    # Ordena os vértices por sequência para garantir a ordem correta
    vertices.sort(key=lambda x: x[2])
    
    print(f"Vértices carregados dinamicamente do CSV: {len(vertices)} pontos")
    print(f"Sequências encontradas: {[v[2] for v in vertices]}")
    
    # Cria DataFrame com todas as colunas do CSV transformado + colunas adicionais necessárias
    colunas_base = [
        "sequencia", "status", "lat", "long", 
        "num_poste", "tipo_poste",
        "estru_mt_nv1", "estru_mt_nv2", "estru_mt_nv3",
        "est_bt_nv1", "est_bt_nv2",
        "estai_ancora", "base_reforcada", "base_concreto",
        "aterr_neutro", "chave", "trafo", "equipamento", "faixa", "cort_arvores_isol",
        "adiconal_1", "qdt_adic_1", "adiconal_2", "qdt_adic_2",
        "adiconal_3", "qdt_adic_3", "adiconal_4", "qdt_adic_4",
        "adiconal_5", "qdt_adic_5", "adiconal_6", "qdt_adic_6",
        "adiconal_7", "qdt_adic_7",
        "rotacao_poste", "modulo", "municipio"
    ]
    colunas_csv = list(matriz_teste_transformada.columns)  # Todas as colunas do CSV transformado
    
    # Remove colunas duplicadas (só se vertices_kml não foi fornecido, pois nesse caso não há colunas extras)
    if vertices_kml is None:
        colunas_finais = colunas_base.copy()
        for coluna in colunas_csv:
            if coluna not in colunas_base:
                colunas_finais.append(coluna)
    else:
        colunas_finais = colunas_base.copy()
    
    # cria a matriz de pontos com as colunas finais
    matriz = pd.DataFrame(columns=colunas_finais)
    
    #VARIVEL new_vertices = lista de vertices com o vão frouxo instalado
    #VARIVEL loose_gap = "SIM" ou "NÃO" (vão frouxo)
    #VARIVEL section_size = tamanho do vão em metros
    #VARIVEL gap_size = tamanho do tramo em metros
    #VARIVEL module_name = nome do módulo
    #VARIVEL lista_nao_intercalar = lista de índices base 0 onde não intercalar postes
    #VARIVEL vertices_kml = lista de vértices do KML no formato [[lat, lon, sequencia], ...]
    #VARIVEL trecho = código do trecho 

    #instalação de vão frouxo - Loose Gap    
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)

    # neste ponto, a variavel new_vertices vai ficar alem dos pontos intercalados, com 5 elementos em cada tupla sendo
    # (lat, lon, sequencia_original, sequencia_ajustada, status)


     # apos a função get_loose_gap, a variável new_vertices vai ficar alem dos pontos intercalados, com 4 elementos em 
     # cada elemento da lista new_vertices é um tupla com 4 elementos: (lat, lon, sequencia, status)
     # o status é "SIM" se é ou não encabeçamento
     # sequencia é a sequencia dos vertices originais
     



    #print(f"🟢 DEPOIS get_loose_gap: {len(new_vertices)} vértices (loose_gap={loose_gap})")
    #if loose_gap == "SIM":
    #    print(f"   Primeiros 3 vértices após get_loose_gap: {new_vertices[:3]}")

    # Divisão do vão em tramos menores
    print(f"🔵 ANTES dividir_tramo: {len(new_vertices)} vértices")
    
    try:
        new_vertices = dividir_tramo(new_vertices, section_size)
        print(f"🟢 DEPOIS dividir_tramo: {len(new_vertices)} vértices")
    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO em dividir_tramo():")
        print(f"Tipo: {type(e).__name__}, Mensagem: {str(e)}")
        print(traceback.format_exc())
        print(f"{'='*80}\n")
        raise

    # Aplica marcação SIM baseada no ângulo de deflexão - Angulo de deflexão
    print(f"🔵 Chamando marcar_vertices_angulo_deflexao() com {len(new_vertices)} vértices...")
    try:
        new_vertices = marcar_vertices_angulo_deflexao(new_vertices, gap_size, module_name, lista_nao_intercalar)
        print(f"🟢 DEPOIS marcar_vertices_angulo_deflexao: {len(new_vertices)} vértices")
    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO em marcar_vertices_angulo_deflexao():")
        print(f"Tipo: {type(e).__name__}, Mensagem: {str(e)}")
        print(f"Parâmetros: gap_size={gap_size}, module_name={module_name}, lista_nao_intercalar={lista_nao_intercalar}")
        print(traceback.format_exc())
        print(f"{'='*80}\n")
        raise
    
    # Aplica encabeçamento automático baseado na distância - Encabeçamento automático
    print(f"🔵 Chamando colocar_encabecamento_rede()...")
    try:
        new_vertices = colocar_encabecamento_rede(new_vertices, section_size)
        print(f"🟢 DEPOIS colocar_encabecamento_rede: {len(new_vertices)} vértices")
    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO em colocar_encabecamento_rede():")
        print(f"Tipo: {type(e).__name__}, Mensagem: {str(e)}")
        print(traceback.format_exc())
        print(f"{'='*80}\n")
        raise

    # Intercala os postes entre os vertices
    print(f"🔵 Chamando intercalar_vertices()...")
    try:
        new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)
        print(f"🟢 DEPOIS intercalar_vertices: {len(new_vertices)} vértices")
    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO em intercalar_vertices():")
        print(f"Tipo: {type(e).__name__}, Mensagem: {str(e)}")
        print(traceback.format_exc())
        print(f"{'='*80}\n")
        raise

    # Preserva todas as colunas originais do CSV sem renomear
    # Não renomeia mais as colunas para preservar os dados originais

    # Obtém os dados de estruturas e postes para cada vértice
    print(f"🔵 Chamando colocar_poste_estrutura() com {len(new_vertices)} vértices...")
    try:
        pontos_matriz_estruturas = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)
        print(f"🟢 DEPOIS colocar_poste_estrutura: {len(pontos_matriz_estruturas)} pontos processados")
    except Exception as e:
        import traceback
        print(f"\n{'='*80}")
        print(f"❌ ERRO em colocar_poste_estrutura():")
        print(f"Tipo: {type(e).__name__}, Mensagem: {str(e)}")
        print(f"Parâmetros: loose_gap={loose_gap}, tipo_poste={tipo_poste}, module_name={module_name}")
        print(traceback.format_exc())
        print(f"{'='*80}\n")
        raise
    
    # Garante que pontos_matriz_estruturas seja um dicionário
    if pontos_matriz_estruturas is None or not isinstance(pontos_matriz_estruturas, dict):
        print(f"[AVISO] pontos_matriz_estruturas não é um dicionário (tipo: {type(pontos_matriz_estruturas)}), usando dicionário vazio")
        pontos_matriz_estruturas = {}

    # Nota: criar_kml_quadrados_bissetriz será chamada na função main
    
    # Adiciona os dados dos vértices processados
    print(f"🔵 Processando {len(new_vertices)} vértices para criar matriz final...")
    for i, vertex in enumerate(new_vertices):
        # Tenta encontrar o vértice original correspondente
        sequencia_original = vertex[2] if len(vertex) > 2 else i
        
        # Busca na matriz_teste_filtrada pela sequência original (apenas se não vier do KML)
        row_correspondente = pd.DataFrame()
        if vertices_kml is None:
            try:
                # Converte sequencia_original para o tipo correto
                sequencia_original_int = int(float(sequencia_original)) if sequencia_original is not None else None
                
                # Usa .iloc com índice numérico para evitar problemas de reindexação
                mask = matriz_teste_filtrada['sequencia'].astype(int) == sequencia_original_int
                indices_match = matriz_teste_filtrada.index[mask]
                
                if len(indices_match) > 0:
                    row_correspondente = matriz_teste_filtrada.loc[[indices_match[0]]]
            except (ValueError, KeyError, TypeError) as e:
                pass
        
        # Extrai status do vértice (4º elemento se existir) - usado para outras finalidades, não para o campo status do CSV
        status_vertice = vertex[3] if len(vertex) > 3 else ""
        
        # Obtém dados de estruturas do dicionário pontos_matriz_estruturas
        # Garante que seja sempre um dicionário
        try:
            if pontos_matriz_estruturas is not None and isinstance(pontos_matriz_estruturas, dict):
                dados_estrutura = pontos_matriz_estruturas.get(vertex, {})
                # Garante que dados_estrutura seja um dicionário
                if dados_estrutura is None or not isinstance(dados_estrutura, dict):
                    dados_estrutura = {}
            else:
                dados_estrutura = {}
        except Exception as e:
            import traceback
            print(f"\n{'='*80}")
            print(f"❌ ERRO ao obter dados_estrutura para vértice {i}:")
            print(f"Vértice: {vertex}")
            print(f"Tipo do erro: {type(e).__name__}, Mensagem: {str(e)}")
            print(traceback.format_exc())
            print(f"{'='*80}\n")
            dados_estrutura = {}
        
        # Cria linha para "implantar" com todas as colunas necessárias
        new_row_implantar = {
            "trecho": trecho,
            "sequencia": dados_estrutura.get("sequencia", sequencia_original),
            "status": "implantar",
            "lat": f"{vertex[0]:.9f}".replace(".", ","),
            "long": f"{vertex[1]:.9f}".replace(".", ","),            
            "num_post": dados_estrutura.get("num_poste", num_poste_inicial if sequencia_original == 0 else ""),
            "tipo_poste": dados_estrutura.get("tipo_poste", ""),
            "estru_mt_nv1": dados_estrutura.get("estru_mt_nv1", ""),
            "estru_mt_nv2": dados_estrutura.get("estru_mt_nv2", ""),
            "estru_mt_nv3": dados_estrutura.get("estru_mt_nv3", ""),
            "est_bt_nv1": dados_estrutura.get("est_bt_nv1", ""),
            "est_bt_nv2": dados_estrutura.get("est_bt_nv2", ""),
            "estai_ancora": dados_estrutura.get("estai_ancora", ""),
            "base_reforcada": dados_estrutura.get("base_reforcada", ""),
            "base_concreto": dados_estrutura.get("base_concreto", ""),
            "aterr_neutro": dados_estrutura.get("aterr_neutro", ""),
            "chave": dados_estrutura.get("chave", ""),
            "trafo": dados_estrutura.get("trafo", ""),
            "equipamento": dados_estrutura.get("equipamento", ""),
            "faixa": dados_estrutura.get("faixa", ""),
            "cort_arvores_isol": dados_estrutura.get("cort_arvores_isol", ""),
            "adiconal_1": dados_estrutura.get("adiconal_1", ""),
            "qdt_adic_1": dados_estrutura.get("qdt_adic_1", ""),
            "adiconal_2": dados_estrutura.get("adiconal_2", ""),
            "qdt_adic_2": dados_estrutura.get("qdt_adic_2", ""),
            "adiconal_3": dados_estrutura.get("adiconal_3", ""),
            "qdt_adic_3": dados_estrutura.get("qdt_adic_3", ""),
            "adiconal_4": dados_estrutura.get("adiconal_4", ""),
            "qdt_adic_4": dados_estrutura.get("qdt_adic_4", ""),
            "adiconal_5": dados_estrutura.get("adiconal_5", ""),
            "qdt_adic_5": dados_estrutura.get("qdt_adic_5", ""),
            "adiconal_6": dados_estrutura.get("adiconal_6", ""),
            "qdt_adic_6": dados_estrutura.get("qdt_adic_6", ""),
            "rotacao_poste": dados_estrutura.get("rotacao_poste", ""),
            "modulo": module_name,
            "municipio": ""
        }
        
        # Adiciona todas as colunas do CSV transformado para "implantar" (se existirem e vier do CSV)
        if not row_correspondente.empty:
            try:
                row = row_correspondente.iloc[0]
                for coluna in matriz_teste_transformada.columns:
                    if coluna not in new_row_implantar:
                        # row é um pandas Series, usa indexação direta ao invés de .get()
                        try:
                            valor = row[coluna] if coluna in row.index else ""
                            new_row_implantar[coluna] = str(valor) if pd.notna(valor) else ""
                        except (KeyError, IndexError):
                            new_row_implantar[coluna] = ""
            except Exception as e:
                print(f"[AVISO] Erro ao processar row_correspondente: {e}")
                pass
        else:
            # Se não há dados do CSV, preenche colunas extras com string vazia
            for col in colunas_finais:
                if col not in new_row_implantar:
                    new_row_implantar[col] = ""
        
        matriz.loc[len(matriz)] = new_row_implantar
        
        # Cria linhas para "existente", "retirar" e "deslocar"
        status_extras = ["existente", "retirar", "deslocar"]
        
        for status_extra in status_extras:
            new_row = {
                "trecho": trecho,
                "sequencia": dados_estrutura.get("sequencia", sequencia_original),
                "status": status_extra
            }
            
            # Preenche todas as outras colunas com string vazia
            for col in colunas_finais:
                if col not in new_row:
                    new_row[col] = ""
            
            matriz.loc[len(matriz)] = new_row


    return matriz

##################################################################################################################################
def parsear_kml_para_vertices(caminho_kml):
    """
    Parseia um arquivo KML e extrai os vértices no formato esperado.
    
    Args:
        caminho_kml: Caminho para o arquivo KML
        
    Returns:
        tuple: (vertices_kml, trecho) onde vertices_kml é [[lat, lon, sequencia], ...]
    """
    try:
        from xml.etree import ElementTree as ET
        
        # Lê o arquivo KML
        tree = ET.parse(caminho_kml)
        root = tree.getroot()
        
        # Registra namespace do KML (pode variar, então busca automaticamente)
        # Remove namespaces do XML para facilitar busca
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}')[1]  # Remove namespace
        
        # Tenta extrair o nome do trecho do Document
        trecho = "T001"  # Padrão
        doc_name = root.find('.//Document/name')
        if doc_name is not None and doc_name.text:
            trecho = doc_name.text.strip()
        else:
            # Tenta do primeiro Placemark
            first_placemark = root.find('.//Placemark/name')
            if first_placemark is not None and first_placemark.text:
                trecho = first_placemark.text.strip()
        
        # Lista para armazenar todos os vértices
        all_vertices = []
        vertex_map = {}  # Para evitar duplicatas: key = "lat_lon", value = sequencia
        sequence = 1
        
        # Função auxiliar para adicionar vértice se não existir
        def add_vertex_if_new(lat, lon):
            nonlocal sequence
            key = f"{lat:.9f}_{lon:.9f}"
            if key not in vertex_map:
                vertex_map[key] = sequence
                all_vertices.append([lat, lon, sequence])
                sequence += 1
        
        # Processa Placemarks
        placemarks = root.findall('.//Placemark')
        
        # Primeiro, processa LineString (prioridade para manter ordem)
        for placemark in placemarks:
            line_string = placemark.find('.//LineString/coordinates')
            if line_string is not None and line_string.text:
                coord_text = line_string.text.strip()
                for coord in coord_text.split():
                    parts = coord.split(',')
                    if len(parts) >= 2:
                        try:
                            lon = float(parts[0])
                            lat = float(parts[1])
                            add_vertex_if_new(lat, lon)
                        except ValueError:
                            continue
        
        # Depois, processa Polygon
        for placemark in placemarks:
            polygon = placemark.find('.//Polygon/outerBoundaryIs/LinearRing/coordinates')
            if polygon is not None and polygon.text:
                coord_text = polygon.text.strip()
                for coord in coord_text.split():
                    parts = coord.split(',')
                    if len(parts) >= 2:
                        try:
                            lon = float(parts[0])
                            lat = float(parts[1])
                            add_vertex_if_new(lat, lon)
                        except ValueError:
                            continue
        
        # Por último, processa Points isolados
        for placemark in placemarks:
            point = placemark.find('.//Point/coordinates')
            if point is not None and point.text:
                parts = point.text.strip().split(',')
                if len(parts) >= 2:
                    try:
                        lon = float(parts[0])
                        lat = float(parts[1])
                        add_vertex_if_new(lat, lon)
                    except ValueError:
                        continue
        
        if len(all_vertices) == 0:
            raise ValueError("Nenhum vértice encontrado no arquivo KML. Verifique se o arquivo contém LineString, Polygon ou Point.")
        
        return all_vertices, trecho
        
    except Exception as e:
        raise ValueError(f"Erro ao parsear arquivo KML: {e}")

##################################################################################################################################
def testar_gerar_matriz():
    """
    Função de teste para simular as entradas da função gerar_matriz.
    Use esta função para depurar diretamente no código Python.
    
    Para usar:
    1. Descomente o breakpoint na função gerar_matriz (linha ~39)
    2. Execute: python backend/core/testar_gerar_matriz.py
    """
    import os
    
    # Caminho padrão do arquivo KML modelo
    caminho_kml_padrao = r"C:\Users\User\Desktop\testexy.kml"
    
    # Solicita o caminho do arquivo KML
    print("=" * 80)
    print("IMPORTAR ARQUIVO KML")
    print("=" * 80)
    print(f"Caminho padrão: {caminho_kml_padrao}")
    caminho_kml = input("Digite o caminho completo do arquivo KML (ou pressione Enter para usar o arquivo padrão): ").strip()
    
    # Se não forneceu caminho, usa o arquivo padrão
    if not caminho_kml:
        caminho_kml = caminho_kml_padrao
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_kml):
        print(f"AVISO: Arquivo KML não encontrado: {caminho_kml}")
        print("Usando dados de teste (vértices fixos)...")
        trecho = "TESTEXXyx.kml"
        vertices_kml = [
            [-17.1136297307818, -49.11767411000091, 1],
            [-17.11345701706738, -49.11426432948661, 2],
            [-17.11651960580667, -49.10948863380214, 3],
            [-17.12849402521782, -49.09688735289248, 4],
            [-17.12986237350835, -49.09723104379758, 5],
            [-17.13109055166651, -49.09997207690454, 6],
            [-17.13175936407751, -49.10016793420279, 7],
            [-17.13465925674163, -49.09536762672727, 8],
            [-17.13552518620229, -49.09270943110433, 9]
        ]
    else:
        if not caminho_kml.lower().endswith('.kml') and not caminho_kml.lower().endswith('.kmz'):
            print("Aviso: O arquivo não tem extensão .kml ou .kmz")
        
        print(f"Parseando arquivo KML: {caminho_kml}")
        vertices_kml, trecho = parsear_kml_para_vertices(caminho_kml)
        print(f"Trecho extraído do KML: {trecho}")
        print(f"Total de vértices extraídos: {len(vertices_kml)}")
    
    # Simula os dados de entrada baseados no arquivo dados_gerar_matriz.json
    module_name = "10105"
    module_data = {
        "codigo_modulo": "10105",
        "descrição_modulo": "Construção - 13,8kV - Rural - MONOF - Cabo 1/0CAA - Pecuária",
        "distribuidora_estado": "Goiás",
        "tipo_obra": "construção",
        "tensão": "13,8kV",
        "local": "rural",
        "fases": "1",
        "neutro": "não",
        "cabo": "1/0CAA",
        "vao_medio": 80,
        "vao_max": 300,
        "tramo_max": 700,
        "custo_med_poste": 12000,
        "%custo_poste_tang": 90,
        "%custo_poste_enc": 120
    }
    loose_gap = "SIM"
    section_size = 700  
    gap_size = 80 
    num_poste_inicial = "00000000"
    tipo_poste = "Existente"  # Pode ser "Implantar" ou "Existente" - padrão: "Existente"
    
    # Solicita os segmentos onde não intercalar postes
    print("\n" + "=" * 80)
    print("NÃO INTERCALAR POSTES")
    print("=" * 80)
    print("Digite os números dos vértices iniciais dos segmentos onde NÃO devem ser intercalados postes.")
    print("Formato: números separados por ponto e vírgula (ex: 2;4)")
    print("Exemplo: '2;4' significa não intercalar no trecho 2->3 e no trecho 4->5")
    print("Deixe em branco se não houver segmentos para pular.")
    entrada_nao_intercalar = input("Digite os vértices (ex: 2;4) ou Enter para nenhum: ").strip()
    
    # Converte a entrada para lista_nao_intercalar (valores das sequências originais)
    lista_nao_intercalar = []
    if entrada_nao_intercalar:
        try:
            # Divide por ponto e vírgula
            segmentos = entrada_nao_intercalar.split(';')
            for seg in segmentos:
                seg_limpo = seg.strip()
                if seg_limpo:
                    # Mantém o valor original da sequência (não converte para índice)
                    # Se usuário digita 2, significa vértice com sequência 2
                    vertice_num = int(seg_limpo)
                    if vertice_num > 0:
                        lista_nao_intercalar.append(vertice_num)
            print(f"Segmentos onde não intercalar postes: {lista_nao_intercalar} (sequências originais)")
        except ValueError as e:
            print(f"AVISO: Erro ao processar entrada '{entrada_nao_intercalar}': {e}")
            print("Usando lista vazia (não pulando nenhum segmento)")
            lista_nao_intercalar = []
    else:
        print("Nenhum segmento será pulado (todos os segmentos serão intercalados se necessário)")
    
    # vertices_kml e trecho já foram definidos acima (importados do KML ou dados de teste)
    
    print("=" * 80)
    print("TESTE: Simulando entrada da função gerar_matriz")
    print("=" * 80)
    print(f"trecho: {trecho}")
    print(f"module_name: {module_name}")
    print(f"loose_gap: {loose_gap}")
    print(f"section_size: {section_size}")
    print(f"gap_size: {gap_size}")
    print(f"num_poste_inicial: {num_poste_inicial}")
    print(f"tipo_poste: {tipo_poste}")
    print(f"lista_nao_intercalar: {lista_nao_intercalar}")
    print(f"vertices_kml: {len(vertices_kml)} vértices")
    print("=" * 80)
    print("Chamando gerar_matriz()...")
    print("(O código vai pausar no breakpoint se estiver ativado)")
    print("=" * 80 + "\n")
    
    # Chama a função gerar_matriz com os parâmetros simulados
    try:
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
            vertices_kml=vertices_kml
        )
        
        print("\n" + "=" * 80)
        print("SUCESSO: Matriz gerada com sucesso!")
        print("=" * 80)
        print(f"Total de registros na matriz: {len(matriz)}")
        print(f"Colunas: {list(matriz.columns)}")
        print("\nPrimeiras 5 linhas:")
        print(matriz.head())
        print("=" * 80)
        
        # Salva o arquivo CSV na pasta resultados
        print("\n" + "=" * 80)
        print("Salvando CSV...")
        print("=" * 80)
        salvar_csv(matriz, "matriz_resultado.csv")
        
        # Cria KML com quadrados na bissetriz
        print("\n" + "=" * 80)
        print("Criando KML com quadrados na bissetriz...")
        print("=" * 80)
        criar_kml_quadrados_bissetriz(matriz, "quadrados_bissetriz.kml")

        
        
        
        return matriz
        
    except Exception as e:
        import traceback
        print("\n" + "=" * 80)
        print("ERRO ao gerar matriz:")
        print("=" * 80)
        print(f"Erro: {str(e)}")
        print("\nTraceback completo:")
        print(traceback.format_exc())
        print("=" * 80)
        raise

##################################################################################################################################
def main():
    trecho = "T1"
    module_naGIme = "MT7"
    module_data = ["MT10", 100, "SIM"]
    loose_gap = "SIM"
    section_size = 500
    gap_size = 120
    num_poste_inicial = "2255555"
    tipo_poste = "EXISTENTE"
    lista_nao_intercalar = [2, 4] 

    # Agora os vértices são carregados dinamicamente do CSV
    matriz = gerar_matriz(trecho, module_naGIme, module_data, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar)

    # Salva o arquivo CSV na pasta resultados
    salvar_csv(matriz, "matriz_resultado.csv")
    
    # Exporta os pontos para KML na pasta resultados
    print("\n=== Exportando para KML ===")
    exportar_para_kml(matriz, "pontos_matriz.kml")
    
    # Cria KML com quadrados na bissetriz
    print("\n=== Criando KML com quadrados na bissetriz ===")
    criar_kml_quadrados_bissetriz(matriz, "quadrados_bissetriz.kml")

if __name__ == "__main__":
    # Para depurar: descomente a linha abaixo e comente main()
    # testar_gerar_matriz()
    main()
import pandas as pd

# Importando funções dos módulos organizados
from calculo_geografico import distance, angle, polar, distance_ptos, angulo_deflexao
from processamento_vertices import get_loose_gap, dividir_tramo, intercalar_vertices
from abaco_mosaico import mtz_abaco, point_in_polygon, mosaico
from exportacao import exportar_para_kml, salvar_csv
from kml import criar_kml_quadrados_bissetriz
from colocar_encabecamento_rede import colocar_encabecamento_rede
from colocar_poste_estrutura import colocar_poste_estrutura
from marcar_vertices_angulo_deflexao import marcar_vertices_angulo_deflexao

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    # Carrega o arquivo matriz_teste.csv para obter todas as colunas
    matriz_teste = pd.read_csv("matriz_teste.csv", sep=";", decimal=",")
    
    # Filtra apenas as linhas com status "Implantar" para obter os vértices reais
    matriz_teste_filtrada = matriz_teste[matriz_teste['status'] == 'Implantar'].copy()
    
    # Cria a lista de vértices dinamicamente a partir do CSV
    vertices = []
    for index, row in matriz_teste_filtrada.iterrows():
        # Verifica se as coordenadas não estão vazias
        lat_str = str(row['lat']).strip()
        lon_str = str(row['long']).strip()
        
        if lat_str == '' or lon_str == '' or lat_str == 'nan' or lon_str == 'nan':
            continue  # Pula linhas com coordenadas vazias
        
        # Converte coordenadas para float
        lat = float(lat_str.replace(',', '.'))
        lon = float(lon_str.replace(',', '.'))
        sequencia = int(row['sequencia'])
        
        # Adiciona o vértice à lista
        vertices.append((lat, lon, sequencia, ""))
    
    # Ordena os vértices por sequência para garantir a ordem correta
    vertices.sort(key=lambda x: x[2])
    
    print(f"Vértices carregados dinamicamente do CSV: {len(vertices)} pontos")
    print(f"Sequências encontradas: {[v[2] for v in vertices]}")
    
    # Cria DataFrame com todas as colunas do CSV original + colunas adicionais necessárias
    colunas_base = ["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste"]
    colunas_csv = list(matriz_teste.columns)  # Todas as colunas do CSV original
    
    # Remove colunas duplicadas
    colunas_finais = colunas_base.copy()
    for coluna in colunas_csv:
        if coluna not in colunas_base:
            colunas_finais.append(coluna)
    
    matriz = pd.DataFrame(columns=colunas_finais)
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)

    new_vertices = dividir_tramo(new_vertices, section_size)

    # Aplica marcação SIM baseada no ângulo de deflexão
    new_vertices = marcar_vertices_angulo_deflexao(new_vertices, gap_size, module_name)

    # Aplica encabeçamento automático baseado na distância
    new_vertices = colocar_encabecamento_rede(new_vertices, section_size)

    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)

    # Preserva todas as colunas originais do CSV sem renomear
    # Não renomeia mais as colunas para preservar os dados originais

    #pontos_matriz = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)

    # Nota: criar_kml_quadrados_bissetriz será chamada na função main
    
    # Adiciona os dados da matriz de pontos ao DataFrame
    for i, vertex in enumerate(new_vertices):
        # Busca dados correspondentes na matriz_teste_filtrada baseado na sequência original
        dados_csv = {}
        
        # Tenta encontrar o vértice original correspondente
        sequencia_original = vertex[2] if len(vertex) > 2 else i
        
        # Busca na matriz_teste_filtrada pela sequência original
        row_correspondente = matriz_teste_filtrada[matriz_teste_filtrada['sequencia'] == sequencia_original]
        
        if not row_correspondente.empty:
            row = row_correspondente.iloc[0]
            # Copia TODAS as colunas do CSV original
            for coluna in matriz_teste.columns:
                dados_csv[coluna] = str(row.get(coluna, ""))
        else:
            # Se não encontrar, usa dados vazios
            for coluna in matriz_teste.columns:
                dados_csv[coluna] = ""
        
        # Cria nova linha com todas as colunas
        new_row = {
            "trecho": trecho,
            "sequencia": i,
            "lat": f"{vertex[0]:.9f}".replace(".", ","),
            "long": f"{vertex[1]:.9f}".replace(".", ","),
            "numero_poste": num_poste_inicial if i == 0 else "",
            "tipo_poste": tipo_poste if i == 0 else ""
        }
        
        # Adiciona todas as colunas do CSV original
        for coluna in matriz_teste.columns:
            new_row[coluna] = dados_csv.get(coluna, "")
        
        matriz.loc[len(matriz)] = new_row
    return matriz

##################################################################################################################################
def main():
    trecho = "T1"
    module_naGIme = "MT7"
    module_data = ["MT10", 100, "SIM"]
    loose_gap = "SIM"
    section_size = 500
    gap_size = 100
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
    main()
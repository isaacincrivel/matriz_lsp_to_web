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
from transformacao_csv import transformar_csv_para_uma_linha_por_vertice

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    # Transforma o CSV para uma linha por vértice
    matriz_teste_transformada = transformar_csv_para_uma_linha_por_vertice("matriz_teste.csv")
    
    # Salva o CSV transformado para referência
    matriz_teste_transformada.to_csv("matriz_teste_transformada.csv", sep=";", decimal=",", index=False)
    
    # Carrega o CSV transformado (versão final já limpa)
    matriz_teste_transformada = pd.read_csv("matriz_teste_transformada_final.csv", sep=";", decimal=",")
    
    # Usa o DataFrame transformado como base (já tem uma linha por vértice)
    matriz_teste_filtrada = matriz_teste_transformada.copy()
    
    # Garante que não há duplicatas e índices estão corretos
    matriz_teste_filtrada = matriz_teste_filtrada.drop_duplicates(subset=['sequencia'], keep='first')
    matriz_teste_filtrada = matriz_teste_filtrada.reset_index(drop=True)
    
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
    colunas_base = ["trecho", "sequencia", "lat", "long", "modalidade", "numero_poste", "tipo_poste"]
    colunas_csv = list(matriz_teste_transformada.columns)  # Todas as colunas do CSV transformado
    
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

    # Intercala os vértices
    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)

    # Preserva todas as colunas originais do CSV sem renomear
    # Não renomeia mais as colunas para preservar os dados originais

    #pontos_matriz = colocar_poste_estrutura(new_vertices, loose_gap, tipo_poste, module_name)

    # Nota: criar_kml_quadrados_bissetriz será chamada na função main
    
    # Adiciona apenas os dados dos vértices originais do CSV (evita linhas vazias)
    for i, vertex in enumerate(new_vertices):
        # Tenta encontrar o vértice original correspondente
        sequencia_original = vertex[2] if len(vertex) > 2 else i
        
        # Busca na matriz_teste_filtrada pela sequência original
        row_correspondente = matriz_teste_filtrada[matriz_teste_filtrada['sequencia'] == sequencia_original]
        
        # Só adiciona se encontrar dados correspondentes (vértice original)
        if not row_correspondente.empty:
            row = row_correspondente.iloc[0]
            
            # Cria linha para "implantar" com todos os dados
            new_row_implantar = {
                "trecho": trecho,
                "sequencia": sequencia_original,  # Usa a sequência original
                "lat": f"{vertex[0]:.9f}".replace(".", ","),
                "long": f"{vertex[1]:.9f}".replace(".", ","),
                "modalidade": "implantar",
                "numero_poste": num_poste_inicial if sequencia_original == 0 else "",
                "tipo_poste": tipo_poste if sequencia_original == 0 else ""
            }
            
            # Adiciona todas as colunas do CSV transformado para "implantar"
            for coluna in matriz_teste_transformada.columns:
                new_row_implantar[coluna] = str(row.get(coluna, ""))
            
            matriz.loc[len(matriz)] = new_row_implantar
            
            # Cria linhas para "existente", "retirar" e "deslocar" com apenas trecho, sequencia e modalidade
            modalidades_extras = ["existente", "retirar", "deslocar"]
            
            for modalidade in modalidades_extras:
                new_row = {
                    "trecho": trecho,
                    "sequencia": sequencia_original,
                    "modalidade": modalidade
                }
                
                # Preenche todas as outras colunas com string vazia
                for col in colunas_finais:
                    if col not in new_row:
                        new_row[col] = ""
                
                matriz.loc[len(matriz)] = new_row
    return matriz

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
    main()
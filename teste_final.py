import pandas as pd

def transformar_csv_para_uma_linha_por_vertice(arquivo_csv):
    """Função de transformação copiada do arquivo principal"""
    df_original = pd.read_csv(arquivo_csv, sep=";", decimal=",")
    vertices_unicos = df_original['sequencia'].unique()
    novas_linhas = []
    
    for sequencia in vertices_unicos:
        linhas_vertice = df_original[df_original['sequencia'] == sequencia]
        linha_implantar = linhas_vertice[linhas_vertice['status'] == 'Implantar']
        
        if linha_implantar.empty:
            continue
        
        linha_mestre = linha_implantar.iloc[0].copy()
        linha_mestre = linha_mestre.drop('status')
        
        for status in ['Existente', 'Retirar', 'deslocar']:
            linha_status = linhas_vertice[linhas_vertice['status'] == status]
            
            if not linha_status.empty:
                linha_status = linha_status.iloc[0]
                
                for coluna in linha_status.index:
                    if (coluna not in ['sequencia', 'status'] and 
                        pd.notna(linha_status[coluna]) and 
                        str(linha_status[coluna]).strip() != ''):
                        nova_coluna = f"{coluna}_{status.lower()}"
                        linha_mestre[nova_coluna] = linha_status[coluna]
        
        novas_linhas.append(linha_mestre)
    
    df_transformado = pd.DataFrame(novas_linhas)
    
    # Garante que não há sequências duplicadas
    df_transformado = df_transformado.drop_duplicates(subset=['sequencia'], keep='first')
    
    # Reseta os índices para evitar problemas com índices duplicados
    df_transformado = df_transformado.reset_index(drop=True)
    
    colunas_sequencia = ['sequencia']
    colunas_originais = [col for col in df_original.columns if col != 'status']
    colunas_sufixos = [col for col in df_transformado.columns if col not in colunas_originais]
    
    ordem_colunas = colunas_sequencia + colunas_originais + sorted(colunas_sufixos)
    df_transformado = df_transformado[ordem_colunas]
    
    return df_transformado

if __name__ == "__main__":
    print("=== Teste Final ===")
    
    # Testa a transformação
    df_transformado = transformar_csv_para_uma_linha_por_vertice("matriz_teste.csv")
    print(f"Transformação: {len(df_transformado)} vértices")
    
    # Testa o filtro de coordenadas
    df_filtrado = df_transformado[
        (df_transformado['lat'].notna()) & 
        (df_transformado['long'].notna())
    ].copy()
    
    df_filtrado = df_filtrado[
        (df_filtrado['lat'].astype(str).str.strip() != '') & 
        (df_filtrado['long'].astype(str).str.strip() != '') &
        (df_filtrado['lat'].astype(str).str.strip() != 'nan') & 
        (df_filtrado['long'].astype(str).str.strip() != 'nan')
    ].copy()
    
    # Garante que não há sequências duplicadas
    df_filtrado = df_filtrado.drop_duplicates(subset=['sequencia'], keep='first')
    df_filtrado = df_filtrado.reset_index(drop=True)
    
    print(f"Vértices com coordenadas válidas: {len(df_filtrado)}")
    
    # Testa a busca por sequência
    for i in range(min(3, len(df_filtrado))):
        try:
            sequencia_teste = df_filtrado.iloc[i]['sequencia']
            row_correspondente = df_filtrado[df_filtrado['sequencia'] == sequencia_teste]
            print(f"Vértice {sequencia_teste}: encontrado {len(row_correspondente)} linhas - OK")
        except Exception as e:
            print(f"Erro no vértice {i}: {e}")
    
    print("\nTeste concluído com sucesso!")

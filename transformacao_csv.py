import pandas as pd

def transformar_csv_para_uma_linha_por_vertice(arquivo_csv):
    """
    Transforma um CSV com múltiplas linhas por vértice (diferentes status) 
    em um CSV com uma única linha por vértice, usando sufixos para diferenciar os dados.
    
    Args:
        arquivo_csv (str): Caminho para o arquivo CSV de entrada
        
    Returns:
        pd.DataFrame: DataFrame transformado com uma linha por vértice
    """
    # Carrega o CSV original
    df_original = pd.read_csv(arquivo_csv, sep=";", decimal=",")
    
    # Obtém vértices únicos
    vertices_unicos = df_original['sequencia'].unique()
    novas_linhas = []
    
    for sequencia in vertices_unicos:
        # Filtra todas as linhas para este vértice
        linhas_vertice = df_original[df_original['sequencia'] == sequencia]
        
        # Busca a linha "Implantar" como linha mestra
        linha_implantar = linhas_vertice[linhas_vertice['status'] == 'Implantar']
        
        if linha_implantar.empty:
            continue  # Pula vértices sem linha "Implantar"
        
        # Usa a linha "Implantar" como base
        linha_mestre = linha_implantar.iloc[0].copy()
        
        # Remove a coluna status
        if 'status' in linha_mestre.index:
            linha_mestre = linha_mestre.drop('status')
        
        # Adiciona dados das outras camadas com sufixos
        for status, sufixo in [('Existente', '_exist'), ('Retirar', '_ret'), ('deslocar', '_desloc')]:
            linha_status = linhas_vertice[linhas_vertice['status'] == status]
            
            if not linha_status.empty:
                linha_status = linha_status.iloc[0]
                
                # Adiciona cada coluna com o sufixo apropriado
                for coluna in linha_status.index:
                    if (coluna not in ['sequencia', 'status'] and 
                        pd.notna(linha_status[coluna]) and 
                        str(linha_status[coluna]).strip() != ''):
                        
                        nova_coluna = f"{coluna}{sufixo}"
                        linha_mestre[nova_coluna] = linha_status[coluna]
        
        novas_linhas.append(linha_mestre)
    
    # Cria o DataFrame transformado
    df_transformado = pd.DataFrame(novas_linhas)
    
    # Remove duplicatas e reorganiza índices
    df_transformado = df_transformado.drop_duplicates(subset=['sequencia'], keep='first')
    df_transformado = df_transformado.reset_index(drop=True)
    
    # Remove colunas duplicadas (pandas adiciona .1, .2, etc.)
    colunas_unicas = []
    for col in df_transformado.columns:
        col_base = col.split('.')[0]  # Remove sufixos .1, .2, etc.
        if col_base not in [c.split('.')[0] for c in colunas_unicas]:
            colunas_unicas.append(col)
    
    df_transformado = df_transformado[colunas_unicas]
    
    # Organiza as colunas em ordem lógica
    colunas_sequencia = ['sequencia']
    colunas_originais = [col for col in df_original.columns if col != 'status']
    colunas_sufixos = [col for col in df_transformado.columns if col not in colunas_originais]
    
    # Ordem: sequencia, colunas originais, colunas com sufixos
    ordem_colunas = colunas_sequencia + colunas_originais + sorted(colunas_sufixos)
    
    # Filtra apenas colunas que existem no DataFrame
    ordem_colunas = [col for col in ordem_colunas if col in df_transformado.columns]
    df_transformado = df_transformado[ordem_colunas]
    
    return df_transformado

def salvar_csv_transformado(df_transformado, arquivo_saida):
    """
    Salva o DataFrame transformado em um arquivo CSV.
    
    Args:
        df_transformado (pd.DataFrame): DataFrame transformado
        arquivo_saida (str): Caminho para o arquivo de saída
    """
    df_transformado.to_csv(arquivo_saida, sep=";", decimal=",", index=False)
    print(f"CSV transformado salvo em: {arquivo_saida}")
    print(f"Total de vértices: {len(df_transformado)}")
    print(f"Total de colunas: {len(df_transformado.columns)}")

if __name__ == "__main__":
    # Teste da função
    arquivo_entrada = "matriz_teste.csv"
    arquivo_saida = "matriz_teste_transformada.csv"
    
    try:
        df_transformado = transformar_csv_para_uma_linha_por_vertice(arquivo_entrada)
        salvar_csv_transformado(df_transformado, arquivo_saida)
        print("Transformação concluída com sucesso!")
    except Exception as e:
        print(f"Erro na transformação: {e}")

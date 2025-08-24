import pandas as pd

def teste_transformacao_direto():
    """Teste direto da transformação CSV - sem terminal"""
    
    print("=== Teste Direto da Transformação ===")
    
    try:
        # 1. Carrega o CSV original
        df_original = pd.read_csv("matriz_teste.csv", sep=";", decimal=",")
        print(f"✅ CSV carregado: {len(df_original)} linhas")
        
        # 2. Testa apenas os primeiros 2 vértices
        vertices_teste = [0, 1]
        novas_linhas = []
        
        for sequencia in vertices_teste:
            # Filtra linhas deste vértice
            linhas_vertice = df_original[df_original['sequencia'] == sequencia]
            linha_implantar = linhas_vertice[linhas_vertice['status'] == 'Implantar']
            
            if not linha_implantar.empty:
                linha_mestre = linha_implantar.iloc[0].copy()
                linha_mestre = linha_mestre.drop('status')
                
                # Adiciona sufixos
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
                print(f"✅ Vértice {sequencia}: processado")
        
        # 3. Cria DataFrame transformado
        df_transformado = pd.DataFrame(novas_linhas)
        df_transformado = df_transformado.drop_duplicates(subset=['sequencia'], keep='first')
        df_transformado = df_transformado.reset_index(drop=True)
        
        print(f"✅ Transformação: {len(df_transformado)} vértices")
        
        # 4. Testa filtro de coordenadas
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
        
        df_filtrado = df_filtrado.drop_duplicates(subset=['sequencia'], keep='first')
        df_filtrado = df_filtrado.reset_index(drop=True)
        
        print(f"✅ Vértices com coordenadas válidas: {len(df_filtrado)}")
        
        # 5. Testa busca por sequência
        for i in range(min(3, len(df_filtrado))):
            sequencia_teste = df_filtrado.iloc[i]['sequencia']
            row_correspondente = df_filtrado[df_filtrado['sequencia'] == sequencia_teste]
            print(f"✅ Vértice {sequencia_teste}: encontrado {len(row_correspondente)} linhas")
        
        # 6. Mostra colunas criadas
        colunas_sufixos = [col for col in df_transformado.columns if '_' in col]
        print(f"✅ Colunas com sufixos criadas: {len(colunas_sufixos)}")
        
        return "🎉 TESTE CONCLUÍDO COM SUCESSO!"
        
    except Exception as e:
        return f"❌ ERRO: {str(e)}"

if __name__ == "__main__":
    resultado = teste_transformacao_direto()
    print(f"\n{resultado}")


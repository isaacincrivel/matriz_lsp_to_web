import pandas as pd

def testar_sufixos():
    """Testa se os sufixos estão sendo aplicados corretamente"""
    print("=== TESTE DE SUFIXOS ===")
    
    # Carrega o CSV transformado
    df = pd.read_csv("matriz_teste_transformada_final.csv", sep=";", decimal=",")
    
    print(f"Total de linhas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    
    # Verifica algumas linhas para ver os dados
    for i in range(min(5, len(df))):
        print(f"\n--- Linha {i} ---")
        row = df.iloc[i]
        
        # Verifica os campos de poste
        tipo_poste = row.get('tipo_poste', '')
        tipo_poste_exist = row.get('tipo_poste_exist', '')
        tipo_poste_ret = row.get('tipo_poste_ret', '')
        tipo_poste_desloc = row.get('tipo_poste_desloc', '')
        
        print(f"tipo_poste: '{tipo_poste}'")
        print(f"tipo_poste_exist: '{tipo_poste_exist}'")
        print(f"tipo_poste_ret: '{tipo_poste_ret}'")
        print(f"tipo_poste_desloc: '{tipo_poste_desloc}'")
        
        # Determina o status
        status_poste = 'implantar'
        if tipo_poste_exist and tipo_poste_exist != '' and tipo_poste_exist != 'nan':
            status_poste = 'existente'
        elif tipo_poste_ret and tipo_poste_ret != '' and tipo_poste_ret != 'nan':
            status_poste = 'retirar'
        elif tipo_poste_desloc and tipo_poste_desloc != '' and tipo_poste_desloc != 'nan':
            status_poste = 'deslocar'
        
        print(f"Status determinado: {status_poste}")
        
        # Simula a lógica do KML
        tipo_poste_para_exibir = ''
        if status_poste == 'implantar':
            tipo_poste_para_exibir = tipo_poste
        elif status_poste == 'existente':
            tipo_poste_para_exibir = tipo_poste_exist
        elif status_poste == 'retirar':
            tipo_poste_para_exibir = tipo_poste_ret
        elif status_poste == 'deslocar':
            tipo_poste_para_exibir = tipo_poste_desloc
        
        # Aplica o sufixo
        texto_final = ''
        if tipo_poste_para_exibir and tipo_poste_para_exibir != 'N/A' and tipo_poste_para_exibir != 'nan':
            if status_poste == 'implantar':
                texto_final = tipo_poste_para_exibir
            elif status_poste == 'existente':
                texto_final = f"{tipo_poste_para_exibir} exist"
            elif status_poste == 'retirar':
                texto_final = f"{tipo_poste_para_exibir} ret"
            elif status_poste == 'deslocar':
                texto_final = f"{tipo_poste_para_exibir} desloc"
        
        print(f"Texto final: '{texto_final}'")

if __name__ == "__main__":
    testar_sufixos()

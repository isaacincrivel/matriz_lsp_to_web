import pandas as pd

# Carrega o CSV com colunas duplicadas
df = pd.read_csv('matriz_teste_transformada.csv', sep=';', decimal=',')

# Remove colunas duplicadas
df_clean = df.loc[:, ~df.columns.duplicated()]

# Remove colunas que terminam com .1, .2, etc. (colunas duplicadas renomeadas pelo pandas)
colunas_para_manter = []
for col in df_clean.columns:
    if not col.endswith('.1') and not col.endswith('.2') and not col.endswith('.3'):
        colunas_para_manter.append(col)

df_final = df_clean[colunas_para_manter]

# Salva o CSV limpo
df_final.to_csv('matriz_teste_transformada_final.csv', sep=';', decimal=',', index=False)

print(f"CSV limpo salvo com {len(df_final)} linhas e {len(df_final.columns)} colunas")
print("Colunas:", list(df_final.columns))

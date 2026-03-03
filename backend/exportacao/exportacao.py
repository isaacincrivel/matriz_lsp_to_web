import pandas as pd

##################################################################################################################################
# FUNÇÕES DE EXPORTAÇÃO
##################################################################################################################################

def exportar_para_kml(matriz, nome_arquivo="pontos_matriz.kml"):
    """
    Função que exporta os pontos da matriz para um arquivo KML.
    
    Args:
        matriz: DataFrame com os dados dos pontos
        nome_arquivo: Nome do arquivo KML a ser gerado
    
    Returns:
        bool: True se o arquivo foi gerado com sucesso, False caso contrário
    """
    import os
    
    # Cria o caminho completo para a pasta resultados
    pasta_resultados = "resultados"
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)
    
    # Caminho completo do arquivo
    caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
    
    try:
        # Cabeçalho do arquivo KML
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Pontos da Matriz</name>
    <description>Pontos gerados pelo sistema de plotagem</description>
    
    <!-- Estilo para postes -->
    <Style id="poste_style">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>
            </Icon>
            <scale>1.0</scale>
        </IconStyle>
        <LabelStyle>
            <color>ff0000ff</color>
            <scale>0.8</scale>
        </LabelStyle>
    </Style>
    
    <!-- Estilo para pontos intermediários -->
    <Style id="ponto_intermediario_style">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/paddle/blue-circle.png</href>
            </Icon>
            <scale>0.8</scale>
        </IconStyle>
        <LabelStyle>
            <color>ff0000ff</color>
            <scale>0.6</scale>
        </LabelStyle>
    </Style>
"""
        
        # Adiciona cada ponto ao KML
        for index, row in matriz.iterrows():
            lat = float(str(row['lat']).replace(',', '.'))
            lon = float(str(row['long']).replace(',', '.'))
            sequencia = row['sequencia']
            trecho = row.get('trecho', 'N/A')
            numero_poste = row.get('num_poste', row.get('numero_poste', ''))
            tipo_poste = row.get('tipo_poste', '')
            estrutura_mt = row.get('EST_1A', row.get('estru_mt_nv1', ''))
            estrutura_bt = row.get('EST_BT1A', row.get('EST_BT1', row.get('est_bt_nv1', '')))
            poste = row.get('tipo_poste', '')
            base = row.get('base_reforcada', '')
            
            # Determina o estilo baseado no tipo de ponto
            if numero_poste and numero_poste != "":
                style_id = "poste_style"
                nome_ponto = f"Poste {numero_poste}"
            else:
                style_id = "ponto_intermediario_style"
                nome_ponto = f"Ponto {sequencia}"
            
            # Cria a descrição detalhada
            descricao = f"""
            <![CDATA[
            <h3>{nome_ponto}</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><td><strong>Trecho:</strong></td><td>{trecho}</td></tr>
                <tr><td><strong>Sequência:</strong></td><td>{sequencia}</td></tr>
                <tr><td><strong>Latitude:</strong></td><td>{row['lat']}</td></tr>
                <tr><td><strong>Longitude:</strong></td><td>{row['long']}</td></tr>
                <tr><td><strong>Número do Poste:</strong></td><td>{numero_poste if numero_poste else 'N/A'}</td></tr>
                <tr><td><strong>Tipo do Poste:</strong></td><td>{tipo_poste if tipo_poste else 'N/A'}</td></tr>
                <tr><td><strong>Estrutura MT:</strong></td><td>{estrutura_mt if estrutura_mt else 'N/A'}</td></tr>
                <tr><td><strong>Estrutura BT:</strong></td><td>{estrutura_bt if estrutura_bt else 'N/A'}</td></tr>
                <tr><td><strong>Poste:</strong></td><td>{poste if poste else 'N/A'}</td></tr>
                <tr><td><strong>Base:</strong></td><td>{base if base else 'N/A'}</td></tr>
            </table>
            ]]>
            """
            
            # Adiciona o ponto ao KML
            kml_content += f"""
    <Placemark>
        <name>{nome_ponto}</name>
        <description>{descricao}</description>
        <styleUrl>#{style_id}</styleUrl>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
    </Placemark>
"""
        
        # Fecha o arquivo KML
        kml_content += """
</Document>
</kml>"""
        
        # Salva o arquivo KML
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        
        print(f"Arquivo KML '{caminho_completo}' gerado com sucesso.")
        print(f"Total de pontos exportados: {len(matriz)}")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar arquivo KML: {e}")
        return False

##################################################################################################################################

# Ordem das colunas conforme modelo MATRIZ_NOVA (para exportação CSV)
ORDEM_COLUNAS_MATRIZ_NOVA = [
    "sequencia", "deriva", "status",
    "CB_1A", "CB_1B", "CB_1C", "CB_1D", "CB_2A", "CB_2B", "CB_2C", "CB_2D",
    "CB_3A", "CB_3B", "CB_3C", "CB_3D", "CB_4A", "CB_4B", "CB_4C", "CB_4D",
    "CB_5A", "CB_5B", "CB_5C", "CB_5D", "CB_6A", "CB_6B", "CB_6C", "CB_6D",
    "CB_BT1A", "CB_BT1B", "CB_BT1C", "CB_BT1D", "CB_BT2A", "CB_BT2B", "CB_BT2C", "CB_BT2D",
    "CB_BT3A", "CB_BT3B", "CB_BT3C", "CB_BT3D",
    "lat", "long", "num_poste", "tipo_poste",
    "EST_1A", "EST_1B", "EST_1C", "EST_1D", "EST_2A", "EST_2B", "EST_2C", "EST_2D",
    "EST_3A", "EST_3B", "EST_3C", "EST_3D", "EST_4A", "EST_4B", "EST_4C", "EST_4D",
    "EST_5A", "EST_5B", "EST_5C", "EST_5D", "EST_6A", "EST_6B", "EST_6C", "EST_6D",
    "EST_BT1A", "EST_BT1B", "EST_BT1C", "EST_BT1D", "EST_BT2A", "EST_BT2B", "EST_BT2C", "EST_BT2D",
    "EST_BT3A", "EST_BT3B", "EST_BT3C", "EST_BT3D",
    "estai_ancora", "base_reforcada", "base_concreto", "aterr_neutro",
    "chave_fusivel", "chave_faca", "trafo", "para_raios", "religador",
    "banco_regulador", "banco_capacitor", "banco_reator",
    "faixa", "cort_arvores_isol", "cerca",
    "adiconal_1", "qdt_adic_1", "adiconal_2", "qdt_adic_2", "adiconal_3", "qdt_adic_3",
    "adiconal_4", "qdt_adic_4", "adiconal_5", "qdt_adic_5", "adiconal_6", "qdt_adic_6",
    "adiconal_7", "qdt_adic_7",
    "rotacao_poste", "municipio", "fuso", "utm_x", "utm_y", "azimute", "enc_tang"
]


def salvar_csv(matriz, nome_arquivo="matriz_resultado.csv"):
    """
    Salva a matriz em um arquivo CSV com tratamento de erros.
    Ordem das colunas conforme modelo MATRIZ_NOVA.
    
    Args:
        matriz: DataFrame a ser salvo
        nome_arquivo: Nome do arquivo CSV
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    import os
    
    # Cria o caminho completo para a pasta resultados
    pasta_resultados = "resultados"
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)
    
    # Caminho completo do arquivo
    caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
    
    try:
        # Limpa valores "nan" antes de salvar
        matriz_limpa = matriz.copy()
        
        # Substitui valores "nan" por strings vazias
        matriz_limpa = matriz_limpa.replace('nan', '')
        matriz_limpa = matriz_limpa.replace('NaN', '')
        
        # Também substitui valores NaN do pandas
        matriz_limpa = matriz_limpa.fillna('')
        
        # Reordena colunas conforme MATRIZ_NOVA (colunas existentes primeiro, depois extras)
        cols_ordenadas = [c for c in ORDEM_COLUNAS_MATRIZ_NOVA if c in matriz_limpa.columns]
        cols_extras = [c for c in matriz_limpa.columns if c not in ORDEM_COLUNAS_MATRIZ_NOVA]
        matriz_limpa = matriz_limpa[cols_ordenadas + cols_extras]
        
        # Converte coordenadas lat e long para usar vírgula como separador decimal
        if 'lat' in matriz_limpa.columns:
            matriz_limpa['lat'] = matriz_limpa['lat'].astype(str).str.replace('.', ',')
        if 'long' in matriz_limpa.columns:
            matriz_limpa['long'] = matriz_limpa['long'].astype(str).str.replace('.', ',')
        
        # Configura o pandas para usar vírgula como separador decimal
        pd.set_option('display.float_format', lambda x: f'{x:.8f}'.replace('.', ','))
        matriz_limpa.to_csv(caminho_completo, index=False, encoding='utf-8', sep=';', decimal=',')
        # Obtém o caminho absoluto para exibir ao usuário
        caminho_absoluto = os.path.abspath(caminho_completo)
        print(f"✅ Arquivo CSV gerado com sucesso!")
        print(f"📍 Local: {caminho_absoluto}")
        return True
    except PermissionError:
        # Se não conseguir salvar com o nome original, tenta com um nome diferente
        import time
        timestamp = int(time.time())
        arquivo_csv = f"matriz_resultado_{timestamp}.csv"
        caminho_alternativo = os.path.join(pasta_resultados, arquivo_csv)
        matriz_limpa.to_csv(caminho_alternativo, index=False, encoding='utf-8', sep=';', decimal=',')
        caminho_absoluto_alt = os.path.abspath(caminho_alternativo)
        print(f"✅ Arquivo CSV gerado com sucesso (nome alternativo devido a erro de permissão)!")
        print(f"📍 Local: {caminho_absoluto_alt}")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo CSV: {e}")
        print("Dados da matriz:")
        print(matriz)
        return False 
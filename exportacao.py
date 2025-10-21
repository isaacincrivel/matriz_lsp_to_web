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
            trecho = row['trecho']
            numero_poste = row['numero_poste']
            tipo_poste = row['tipo_poste']
            estrutura_mt = row.get('estru_mt_nv1', '')
            estrutura_bt = row.get('est_bt_nv1', '')
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

def salvar_csv(matriz, nome_arquivo="matriz_resultado.csv"):
    """
    Salva a matriz em um arquivo CSV com tratamento de erros.
    
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
        
        # Converte coordenadas lat e long para usar vírgula como separador decimal
        if 'lat' in matriz_limpa.columns:
            matriz_limpa['lat'] = matriz_limpa['lat'].astype(str).str.replace('.', ',')
        if 'long' in matriz_limpa.columns:
            matriz_limpa['long'] = matriz_limpa['long'].astype(str).str.replace('.', ',')
        
        # Configura o pandas para usar vírgula como separador decimal
        pd.set_option('display.float_format', lambda x: f'{x:.8f}'.replace('.', ','))
        matriz_limpa.to_csv(caminho_completo, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV '{caminho_completo}' gerado com sucesso.")
        return True
    except PermissionError:
        # Se não conseguir salvar com o nome original, tenta com um nome diferente
        import time
        timestamp = int(time.time())
        arquivo_csv = f"matriz_resultado_{timestamp}.csv"
        caminho_alternativo = os.path.join(pasta_resultados, arquivo_csv)
        matriz_limpa.to_csv(caminho_alternativo, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV '{caminho_alternativo}' gerado com sucesso (nome alternativo devido a erro de permissão).")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo CSV: {e}")
        print("Dados da matriz:")
        print(matriz)
        return False 
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.core.calculo_geografico import angle, polar, distance
from backend.elementos.kml_elementos import colocar_elemento_kml

"""
ARQUIVO KML PRINCIPAL
====================

Este arquivo contém a função principal para criar KML com quadrados na bissetriz.
As funções modulares de elementos foram movidas para kml_elementos.py

Para adicionar novos elementos:
1. Edite o arquivo kml_elementos.py
2. Adicione a condição em cria_desenho_elemento_kml()
3. A variável já está na lista de variaveis_elementos em colocar_elemento_kml()
"""

def criar_kml_quadrados_bissetriz(pontos_matriz, nome_arquivo="quadrados_bissetriz.kml"):


    tipo_cabo = "1#4CAA"
    tipo_tensao = "13,8kV"
    tipo_modalidade = "monofasico"

    
    """
    Cria um arquivo KML com quadrados de 5x3 metros posicionados na bissetriz do ângulo
    entre vértices consecutivos, ficando tangente aos vértices anterior e posterior.
    Também cria uma linha conectando os vértices com informações de poste, estrutura e base.
    
    Args:
        pontos_matriz: DataFrame ou dicionário com os dados dos pontos
        nome_arquivo: Nome do arquivo KML a ser gerado
    
    Returns:
        bool: True se o arquivo foi gerado com sucesso, False caso contrário
    """
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
    <name>Quadrados na Bissetriz</name>
         <description>Quadrados de 5x3 metros posicionados na bissetriz dos ângulos</description>
    
    <!-- Estilo para poste IMPLANTAR (vazio) -->
    <Style id="poste_implantar_style">
        <PolyStyle>
            <color>ff0000ff</color>
            <fill>0</fill>
            <outline>1</outline>
        </PolyStyle>
        <LineStyle>
            <color>ff0000ff</color>
            <width>2</width>
        </LineStyle>
    </Style>
    
    <!-- Estilo para poste EXISTENTE (preenchido) -->
    <Style id="poste_existente_style">
        <PolyStyle>
            <color>ff0000ff</color>
            <fill>1</fill>
            <outline>1</outline>
        </PolyStyle>
        <LineStyle>
            <color>ff0000ff</color>
            <width>2</width>
        </LineStyle>
    </Style>
    
    <!-- Estilo para poste RETIRAR (vazado com X) -->
    <Style id="poste_retirar_style">
        <PolyStyle>
            <color>ff0000ff</color>
            <fill>0</fill>
            <outline>1</outline>
        </PolyStyle>
        <LineStyle>
            <color>ff0000ff</color>
            <width>2</width>
        </LineStyle>
    </Style>
    
    <!-- Estilo para poste DESLOCAR (vazado com diagonal) -->
    <Style id="poste_deslocar_style">
        <PolyStyle>
            <color>ff0000ff</color>
            <fill>0</fill>
            <outline>1</outline>
        </PolyStyle>
        <LineStyle>
            <color>ff0000ff</color>
            <width>2</width>
        </LineStyle>
    </Style>
    
         <!-- Estilo para a linha conectando os vértices -->
     <Style id="linha_vertices_style">
         <LineStyle>
             <color>ff00ff00</color>
             <width>1.5</width>
         </LineStyle>
     </Style>
     
     <!-- Estilo para linhas azuis (retirar e deslocar) -->
     <Style id="linha_azul_style">
         <LineStyle>
             <color>ffff0000</color>
             <width>2</width>
         </LineStyle>
     </Style>
    
    <!-- Estilo para labels visíveis -->
    <Style id="label_style">
        <LabelStyle>
            <color>ff0000ff</color>
            <scale>0.8</scale>
            <colorMode>normal</colorMode>
        </LabelStyle>
        <IconStyle>
            <scale>0</scale>
        </IconStyle>
    </Style>
    
    <!-- Estilo para estai âncora -->
    <Style id="estai_ancora_style">
        <LineStyle>
            <color>ff0000ff</color>
            <width>2</width>
        </LineStyle>
    </Style>
    
         <!-- Estilo para quadrado do estai âncora -->
     <Style id="estai_ancora_quadrado_style">
         <PolyStyle>
             <color>ff0000ff</color>
             <fill>1</fill>
             <outline>1</outline>
         </PolyStyle>
         <LineStyle>
             <color>ff0000ff</color>
             <width>1</width>
         </LineStyle>
     </Style>
     
     <!-- Estilo para distâncias entre vértices (amarelo) -->
     <Style id="distancia_style">
         <LabelStyle>
             <color>ff7fffff</color>
             <scale>0.8</scale>
             <colorMode>normal</colorMode>
         </LabelStyle>
         <IconStyle>
             <scale>0</scale>
         </IconStyle>
     </Style>
"""
        
        # Converte pontos_matriz para lista de coordenadas e dados
        pontos = []
        dados_pontos = []
        
        # Verifica se é DataFrame ou dicionário
        if hasattr(pontos_matriz, 'iterrows'):
            # É um DataFrame
            for index, row in pontos_matriz.iterrows():
                # Verifica se as coordenadas não estão vazias
                lat_str = str(row['lat']).strip()
                lon_str = str(row['long']).strip()
                
                if lat_str == '' or lon_str == '' or lat_str == 'nan' or lon_str == 'nan':
                    continue  # Pula linhas com coordenadas vazias
                
                lat = float(lat_str.replace(',', '.'))
                lon = float(lon_str.replace(',', '.'))
                pontos.append((lat, lon))
                # Determina o status do poste baseado nas colunas com sufixos
                poste_implantar = row.get('tipo_poste', '').strip()
                poste_existente = row.get('tipo_poste_exist', '').strip()
                poste_retirar = row.get('tipo_poste_ret', '').strip()
                poste_deslocar = row.get('tipo_poste_desloc', '').strip()
                
                # Determina qual status tem o poste
                # Se há dados válidos em poste_existente, retirar ou deslocar, usa esse status
                # Se não há dados válidos em nenhuma coluna com sufixo, usa implantar
                status_poste = 'implantar'  # padrão
                if (poste_existente and poste_existente != '' and poste_existente != 'nan' and 
                    str(poste_existente).strip().lower() != 'nan'):
                    status_poste = 'existente'
                elif (poste_retirar and poste_retirar != '' and poste_retirar != 'nan' and 
                      str(poste_retirar).strip().lower() != 'nan'):
                    status_poste = 'retirar'
                elif (poste_deslocar and poste_deslocar != '' and poste_deslocar != 'nan' and 
                      str(poste_deslocar).strip().lower() != 'nan'):
                    status_poste = 'deslocar'
                
                # Obtém a sequência da coluna do CSV e converte para string se necessário
                sequencia_valor = row.get('sequencia', '')
                if sequencia_valor != '' and sequencia_valor != 'nan':
                    try:
                        sequencia_str = str(int(float(str(sequencia_valor).replace(',', '.'))))
                    except (ValueError, TypeError):
                        sequencia_str = str(sequencia_valor)
                else:
                    sequencia_str = ''
                
                # Busca estruturas com sufixos (_exist, _ret, _desloc)
                # Função auxiliar para tratar valores None/NaN
                def tratar_valor(valor):
                    if valor is None or (hasattr(valor, '__iter__') and str(valor).strip().lower() in ['nan', 'none', '']):
                        return ''
                    return str(valor).strip()
                
                # Busca estruturas MT - tenta diferentes variações de nomes de colunas
                # O transformacao_csv cria colunas como estru_mt_nv1_ret, estru_mt_nv1_exist, estru_mt_nv1_desloc
                estrutura_mt_exist = tratar_valor(row.get('estru_mt_nv1_exist', '')) or tratar_valor(row.get('estrutura_mt_exist', ''))
                estrutura_mt_ret = tratar_valor(row.get('estru_mt_nv1_ret', '')) or tratar_valor(row.get('estrutura_mt_ret', ''))
                estrutura_mt_desloc = tratar_valor(row.get('estru_mt_nv1_desloc', '')) or tratar_valor(row.get('estrutura_mt_desloc', ''))
                estrutura_mt_nv2_exist = tratar_valor(row.get('estru_mt_nv2_exist', '')) or tratar_valor(row.get('estrutura_mt_nv2_exist', ''))
                estrutura_mt_nv2_ret = tratar_valor(row.get('estru_mt_nv2_ret', '')) or tratar_valor(row.get('estrutura_mt_nv2_ret', ''))
                estrutura_mt_nv2_desloc = tratar_valor(row.get('estru_mt_nv2_desloc', '')) or tratar_valor(row.get('estrutura_mt_nv2_desloc', ''))
                estrutura_mt_nv3_exist = tratar_valor(row.get('estru_mt_nv3_exist', '')) or tratar_valor(row.get('estrutura_mt_nv3_exist', ''))
                estrutura_mt_nv3_ret = tratar_valor(row.get('estru_mt_nv3_ret', '')) or tratar_valor(row.get('estrutura_mt_nv3_ret', ''))
                estrutura_mt_nv3_desloc = tratar_valor(row.get('estru_mt_nv3_desloc', '')) or tratar_valor(row.get('estrutura_mt_nv3_desloc', ''))
                estrutura_bt_exist = tratar_valor(row.get('est_bt_nv1_exist', '')) or tratar_valor(row.get('estrutura_bt_exist', '')) or tratar_valor(row.get('est_bt_exist', ''))
                estrutura_bt_ret = tratar_valor(row.get('est_bt_nv1_ret', '')) or tratar_valor(row.get('estrutura_bt_ret', '')) or tratar_valor(row.get('est_bt_ret', ''))
                estrutura_bt_desloc = tratar_valor(row.get('est_bt_nv1_desloc', '')) or tratar_valor(row.get('estrutura_bt_desloc', '')) or tratar_valor(row.get('est_bt_desloc', ''))
                estrutura_bt_nv2_exist = tratar_valor(row.get('est_bt_nv2_exist', '')) or tratar_valor(row.get('estrutura_bt_nv2_exist', ''))
                estrutura_bt_nv2_ret = tratar_valor(row.get('est_bt_nv2_ret', '')) or tratar_valor(row.get('estrutura_bt_nv2_ret', ''))
                estrutura_bt_nv2_desloc = tratar_valor(row.get('est_bt_nv2_desloc', '')) or tratar_valor(row.get('estrutura_bt_nv2_desloc', ''))
                
                # Debug temporário para sequência 9
                if sequencia_str == '9':
                    print(f"\n=== DEBUG POSTE 9 ===")
                    print(f"Colunas disponíveis com 'ret': {[col for col in row.index if 'ret' in str(col).lower()]}")
                    print(f"estru_mt_nv1: {row.get('estru_mt_nv1', 'NÃO ENCONTRADO')}")
                    print(f"estru_mt_nv1_ret: {row.get('estru_mt_nv1_ret', 'NÃO ENCONTRADO')}")
                    print(f"estrutura_mt_ret (tratado): {estrutura_mt_ret}")
                    print(f"tipo_poste_exist: {row.get('tipo_poste_exist', 'NÃO ENCONTRADO')}")
                    print(f"status_poste: {status_poste}")
                    print(f"===================\n")
                
                # Busca também estruturas com sufixos usando nomes alternativos
                # O transformacao_csv cria colunas como estru_mt_nv1_ret, então busca diretamente
                estrutura_mt_ret_alt = tratar_valor(row.get('estru_mt_nv1_ret', ''))
                estrutura_mt_exist_alt = tratar_valor(row.get('estru_mt_nv1_exist', ''))
                estrutura_mt_desloc_alt = tratar_valor(row.get('estru_mt_nv1_desloc', ''))
                
                # Usa a estrutura encontrada (pode ser de qualquer uma das buscas)
                if not estrutura_mt_ret:
                    estrutura_mt_ret = estrutura_mt_ret_alt
                if not estrutura_mt_exist:
                    estrutura_mt_exist = estrutura_mt_exist_alt
                if not estrutura_mt_desloc:
                    estrutura_mt_desloc = estrutura_mt_desloc_alt
                
                dados_pontos.append({
                    'sequencia': sequencia_str,  # Usa o valor da coluna sequencia do CSV
                    'numero_poste': row.get('num_poste', ''),
                    'tipo_poste': row.get('tipo_poste', ''),
                    'estrutura_mt': row.get('estru_mt_nv1', ''),  # Nome correto da coluna
                    'estrutura_mt_nv2': row.get('estru_mt_nv2', ''),
                    'estrutura_mt_nv3': row.get('estru_mt_nv3', ''),
                    'estrutura_bt': row.get('est_bt_nv1', ''),  # Nome correto da coluna
                    'estrutura_bt_nv2': row.get('est_bt_nv2', ''),
                    'poste': row.get('tipo_poste', ''),  # Campo correto
                    'tipo_poste': row.get('tipo_poste', ''),
                    'base': row.get('base_reforcada', ''),  # Campo correto
                    'base_concreto': row.get('base_concreto', ''),
                    'estai_ancora': row.get('estai_ancora', ''),
                    'status': row.get('status', ''),
                    'rotacao_poste': row.get('rotacao_poste', ''),
                    'status_poste': status_poste,  # Novo campo para status do poste
                    'poste_implantar': poste_implantar,
                    'poste_existente': poste_existente,
                    'poste_retirar': poste_retirar,
                    'poste_deslocar': poste_deslocar,
                    # Estruturas com sufixos
                    'estrutura_mt_exist': estrutura_mt_exist,
                    'estrutura_mt_ret': estrutura_mt_ret,
                    'estrutura_mt_desloc': estrutura_mt_desloc,
                    'estrutura_mt_nv2_exist': estrutura_mt_nv2_exist,
                    'estrutura_mt_nv2_ret': estrutura_mt_nv2_ret,
                    'estrutura_mt_nv2_desloc': estrutura_mt_nv2_desloc,
                    'estrutura_mt_nv3_exist': estrutura_mt_nv3_exist,
                    'estrutura_mt_nv3_ret': estrutura_mt_nv3_ret,
                    'estrutura_mt_nv3_desloc': estrutura_mt_nv3_desloc,
                    'estrutura_bt_exist': estrutura_bt_exist,
                    'estrutura_bt_ret': estrutura_bt_ret,
                    'estrutura_bt_desloc': estrutura_bt_desloc,
                    'estrutura_bt_nv2_exist': estrutura_bt_nv2_exist,
                    'estrutura_bt_nv2_ret': estrutura_bt_nv2_ret,
                    'estrutura_bt_nv2_desloc': estrutura_bt_nv2_desloc
                })
        else:
            # É um dicionário - precisa converter para o formato esperado
            vertices_list = list(pontos_matriz.keys())
            for i, vertex in enumerate(vertices_list):
                lat, lon = vertex[0], vertex[1]
                pontos.append((lat, lon))
                dados_vertex = pontos_matriz.get(vertex, {})
                # Tenta obter a sequência do vértice (posição 2) ou do dicionário, senão usa o índice
                if len(vertex) > 2 and vertex[2] != '':
                    sequencia_valor = vertex[2]
                    try:
                        sequencia_str = str(int(float(str(sequencia_valor).replace(',', '.'))))
                    except (ValueError, TypeError):
                        sequencia_str = str(sequencia_valor)
                else:
                    sequencia_str = str(i)
                dados_pontos.append({
                    'sequencia': sequencia_str,  # Usa a sequência do vértice ou do CSV
                    'numero_poste': dados_vertex.get('numero_poste', ''),
                    'tipo_poste': dados_vertex.get('tipo_poste', ''),
                    'estrutura_mt': dados_vertex.get('estrutura_mt', ''),
                    'estrutura_mt_nv2': dados_vertex.get('estrutura_mt_nv2', ''),
                    'estrutura_mt_nv3': dados_vertex.get('estrutura_mt_nv3', ''),
                    'estrutura_bt': dados_vertex.get('estrutura_bt', ''),
                    'estrutura_bt_nv2': dados_vertex.get('estrutura_bt_nv2', ''),
                    'poste': dados_vertex.get('poste', ''),
                    'base': dados_vertex.get('base', ''),
                    'base_concreto': dados_vertex.get('base_concreto', ''),  # Adiciona base_concreto
                    'estai_ancora': dados_vertex.get('estai_ancora', ''),  # Adiciona estai_ancora
                    'status': dados_vertex.get('status', ''),  # Adiciona status
                    'rotacao_poste': dados_vertex.get('rotacao_poste', '')
                })
        
        # Adiciona a linha conectando todos os vértices
        coordenadas_linha = ""
        for i, (lat, lon) in enumerate(pontos):
            coordenadas_linha += f"{lon},{lat},0 "
        
        kml_content += f"""
    <Placemark>
        <name>Linha dos Vértices</name>
        <description>
            <![CDATA[
            <h3>Linha Conectando os Vértices</h3>
            <p>Linha que conecta todos os vértices da rota</p>
            ]]>
        </description>
        <styleUrl>#linha_vertices_style</styleUrl>
        <LineString>
            <coordinates>
                {coordenadas_linha.strip()}
            </coordinates>
        </LineString>
    </Placemark>
"""
        
        # Adiciona as distâncias entre os vértices como labels visíveis
        
        for i in range(len(pontos) - 1):
            pt_atual = pontos[i]
            pt_proximo = pontos[i + 1]
            
            # Calcula a distância entre os dois pontos
            distancia = distance(pt_atual[0], pt_atual[1], pt_proximo[0], pt_proximo[1])
            
            # Calcula o ponto médio entre os dois vértices
            lat_medio = (pt_atual[0] + pt_proximo[0]) / 2
            lon_medio = (pt_atual[1] + pt_proximo[1]) / 2
            
            # Formata a distância (em metros)
            distancia_formatada = f"{distancia:.0f}m"
            
            kml_content += f"""
    <Placemark>
        <name>{distancia_formatada}</name>
        <description>
            <![CDATA[
            <h3>Distância entre Vértices</h3>
            <p><strong>De:</strong> Vértice {i+1}</p>
            <p><strong>Para:</strong> Vértice {i+2}</p>
            <p><strong>Distância:</strong> {distancia_formatada}</p>
            ]]>
        </description>
        <styleUrl>#distancia_style</styleUrl>
        <Point>
            <coordinates>{lon_medio},{lat_medio},0</coordinates>
        </Point>
    </Placemark>
"""
        
        # Função auxiliar para verificar se valor é válido
        def valor_valido(valor):
            if not valor:
                return False
            valor_str = str(valor).strip().lower()
            return valor_str not in ['', 'nan', 'none', 'n/a']
        
        # Para cada ponto, cria um quadrado na bissetriz
        for i in range(len(pontos)):
            pt_atual = pontos[i]
            
            # Para pontos extremos, usa lógica especial
            if i == 0:  # Primeiro ponto (derivação)
                pt_posterior = pontos[i + 1]
                # Para o primeiro ponto, usa o ângulo do primeiro para o segundo
                angulo_anterior = angle(pt_atual[0], pt_atual[1], pt_posterior[0], pt_posterior[1]) - 180
                angulo_posterior = angle(pt_atual[0], pt_atual[1], pt_posterior[0], pt_posterior[1])
            elif i == len(pontos) - 1:  # Último ponto
                pt_anterior = pontos[i - 1]
                # Para o último ponto, usa o ângulo do penúltimo para o último
                angulo_anterior = angle(pt_anterior[0], pt_anterior[1], pt_atual[0], pt_atual[1])
                angulo_posterior = angle(pt_anterior[0], pt_anterior[1], pt_atual[0], pt_atual[1]) + 180
            else:  # Pontos intermediários
                pt_anterior = pontos[i - 1]
                pt_posterior = pontos[i + 1]
                # Calcula os ângulos para o ponto anterior e posterior
                angulo_anterior = angle(pt_anterior[0], pt_anterior[1], pt_atual[0], pt_atual[1])
                angulo_posterior = angle(pt_atual[0], pt_atual[1], pt_posterior[0], pt_posterior[1])
            
            # Calcula a bissetriz (média dos ângulos)
            # Se a diferença for maior que 180°, ajusta
            diff_angulo = abs(angulo_posterior - angulo_anterior)
            if diff_angulo > 180:
                if angulo_posterior > angulo_anterior:
                    angulo_anterior += 360
                else:
                    angulo_posterior += 360
            
            bissetriz = (angulo_anterior + angulo_posterior) / 2
            
            # Obtém os dados do ponto atual
            dados_atual = dados_pontos[i]
            
            # Aplica a rotação baseada no campo rotacao_poste
            rotacao_poste = dados_atual.get('rotacao_poste', '').lower().strip()
            angulo_final = bissetriz  # valor padrão
            
            if rotacao_poste == 'tang' or rotacao_poste == 'tangente':
                angulo_final = bissetriz
            elif rotacao_poste == 'bissetriz1' or rotacao_poste == 'bicetriz1':
                angulo_final = bissetriz
            elif rotacao_poste == 'bissetriz2' or rotacao_poste == 'bicetriz2':
                angulo_final = bissetriz + 90
            elif rotacao_poste == 'topo1':
                angulo_final = angulo_anterior + 90
            elif rotacao_poste == 'topo2':
                angulo_final = angulo_posterior + 90
            
            # Normaliza o ângulo final para ficar entre 0 e 360 graus
            while angulo_final < 0:
                angulo_final += 360
            while angulo_final >= 360:
                angulo_final -= 360
            
            # Obtém a informação de base_concreto para uso posterior
            base_concreto = str(dados_atual.get('base_concreto', '')).strip()
            
            # Define dimensões padrão para todos os postes
            largura = 5.0  # 5 metros (lado maior)
            altura = 3.0   # 3 metros (lado menor)
            

            
            # Calcula os vértices do quadrado
            centro_lat, centro_lon = pt_atual
            
            # Vértice 1: frente-esquerda
            lat1, lon1 = polar(centro_lat, centro_lon, largura/2, angulo_final - 90)
            lat1, lon1 = polar(lat1, lon1, altura/2, angulo_final)
            
            # Vértice 2: frente-direita
            lat2, lon2 = polar(centro_lat, centro_lon, largura/2, angulo_final + 90)
            lat2, lon2 = polar(lat2, lon2, altura/2, angulo_final)
            
            # Vértice 3: trás-direita
            lat3, lon3 = polar(centro_lat, centro_lon, largura/2, angulo_final + 90)
            lat3, lon3 = polar(lat3, lon3, altura/2, angulo_final + 180)
            
            # Vértice 4: trás-esquerda
            lat4, lon4 = polar(centro_lat, centro_lon, largura/2, angulo_final - 90)
            lat4, lon4 = polar(lat4, lon4, altura/2, angulo_final + 180)
            
            # Cria o texto visível para o quadrado com as informações solicitadas
            sequencia = dados_atual['sequencia'] if dados_atual['sequencia'] != '' else 'N/A'
            estrutura_mt = dados_atual['estrutura_mt'] if dados_atual['estrutura_mt'] != '' else 'N/A'
            estrutura_mt_nv2 = dados_atual['estrutura_mt_nv2'] if dados_atual['estrutura_mt_nv2'] != '' else 'N/A'
            estrutura_mt_nv3 = dados_atual['estrutura_mt_nv3'] if dados_atual['estrutura_mt_nv3'] != '' else 'N/A'
            estrutura_bt = dados_atual['estrutura_bt'] if dados_atual['estrutura_bt'] != '' else 'N/A'
            estrutura_bt_nv2 = dados_atual['estrutura_bt_nv2'] if dados_atual['estrutura_bt_nv2'] != '' else 'N/A'
            
            # Determina o estilo baseado no status do poste
            status_poste = dados_atual.get('status_poste', 'implantar')
            if status_poste == 'existente':
                estilo_poste = "poste_existente_style"
            elif status_poste == 'retirar':
                estilo_poste = "poste_retirar_style"
            elif status_poste == 'deslocar':
                estilo_poste = "poste_deslocar_style"
            else:
                estilo_poste = "poste_implantar_style"
            
            # Cria o texto visível que aparecerá na tela com todas as informações das estruturas
            # Filtra apenas os valores que não são 'nan' ou vazios
            valores_visiveis = []
            
            if sequencia is not None and str(sequencia) != 'N/A':
                valores_visiveis.append(str(sequencia))
            
            # Adiciona o tipo de poste correto baseado no status
            tipo_poste_para_exibir = ''
            if status_poste == 'implantar':
                tipo_poste_para_exibir = dados_atual.get('tipo_poste', '')
            elif status_poste == 'existente':
                tipo_poste_para_exibir = dados_atual.get('poste_existente', '')
            elif status_poste == 'retirar':
                tipo_poste_para_exibir = dados_atual.get('poste_retirar', '')
            elif status_poste == 'deslocar':
                tipo_poste_para_exibir = dados_atual.get('poste_deslocar', '')
            
            if (tipo_poste_para_exibir and 
                tipo_poste_para_exibir != 'N/A' and 
                tipo_poste_para_exibir != 'nan' and 
                str(tipo_poste_para_exibir).strip().lower() != 'nan'):
                if status_poste == 'implantar':
                    valores_visiveis.append(tipo_poste_para_exibir)
                elif status_poste == 'existente':
                    valores_visiveis.append(f"{tipo_poste_para_exibir} exist")
                elif status_poste == 'retirar':
                    valores_visiveis.append(f"{tipo_poste_para_exibir} ret")
                elif status_poste == 'deslocar':
                    valores_visiveis.append(f"{tipo_poste_para_exibir} desloc")
            
            # Adiciona estruturas com sufixos baseado no status (mesma lógica do poste)
            # Função auxiliar para extrair estrutura de strings como "PDT10/30(UP1" -> "UP1"
            def extrair_estrutura(valor):
                if not valor_valido(valor):
                    return ''
                valor_str = str(valor).strip()
                # Tenta extrair estrutura entre parênteses, ex: "PDT10/30(UP1" -> "UP1"
                if '(' in valor_str:
                    partes = valor_str.split('(')
                    if len(partes) > 1:
                        estrutura = partes[1].split(')')[0].split()[0]  # Pega até o primeiro espaço ou )
                        return estrutura.strip()
                # Se não tem parênteses, retorna o valor original
                return valor_str
            
            # Estrutura MT NV1 - Adiciona TODAS as estruturas encontradas
            estrutura_mt_exist = dados_atual.get('estrutura_mt_exist', '')
            estrutura_mt_ret = dados_atual.get('estrutura_mt_ret', '')
            estrutura_mt_desloc = dados_atual.get('estrutura_mt_desloc', '')
            
            # SEMPRE adiciona a estrutura normal (da linha Implantar) primeiro, se existir
            if valor_valido(estrutura_mt):
                estrutura_extraida = extrair_estrutura(estrutura_mt)
                estrutura_normal = estrutura_extraida if estrutura_extraida else estrutura_mt
                # Adiciona sem sufixo (é da linha Implantar)
                valores_visiveis.append(estrutura_normal)
            
            # Adiciona estrutura com sufixo _exist se existir
            if valor_valido(estrutura_mt_exist):
                estrutura_extraida = extrair_estrutura(estrutura_mt_exist)
                estrutura_texto = f"{estrutura_extraida} exist" if estrutura_extraida else f"{estrutura_mt_exist} exist"
                valores_visiveis.append(estrutura_texto)
            
            # Adiciona estrutura com sufixo _ret se existir
            if valor_valido(estrutura_mt_ret):
                estrutura_extraida = extrair_estrutura(estrutura_mt_ret)
                estrutura_texto = f"{estrutura_extraida} ret" if estrutura_extraida else f"{estrutura_mt_ret} ret"
                valores_visiveis.append(estrutura_texto)
            
            # Adiciona estrutura com sufixo _desloc se existir
            if valor_valido(estrutura_mt_desloc):
                estrutura_extraida = extrair_estrutura(estrutura_mt_desloc)
                estrutura_texto = f"{estrutura_extraida} desloc" if estrutura_extraida else f"{estrutura_mt_desloc} desloc"
                valores_visiveis.append(estrutura_texto)
            
            # Estrutura MT NV2 - Adiciona TODAS as estruturas encontradas
            estrutura_mt_nv2_exist = dados_atual.get('estrutura_mt_nv2_exist', '')
            estrutura_mt_nv2_ret = dados_atual.get('estrutura_mt_nv2_ret', '')
            estrutura_mt_nv2_desloc = dados_atual.get('estrutura_mt_nv2_desloc', '')
            
            # SEMPRE adiciona a estrutura normal primeiro, se existir
            if valor_valido(estrutura_mt_nv2):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv2)
                valores_visiveis.append(estrutura_extraida if estrutura_extraida else estrutura_mt_nv2)
            
            # Adiciona estruturas com sufixos se existirem
            if valor_valido(estrutura_mt_nv2_exist):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv2_exist)
                valores_visiveis.append(f"{estrutura_extraida} exist" if estrutura_extraida else f"{estrutura_mt_nv2_exist} exist")
            if valor_valido(estrutura_mt_nv2_ret):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv2_ret)
                valores_visiveis.append(f"{estrutura_extraida} ret" if estrutura_extraida else f"{estrutura_mt_nv2_ret} ret")
            if valor_valido(estrutura_mt_nv2_desloc):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv2_desloc)
                valores_visiveis.append(f"{estrutura_extraida} desloc" if estrutura_extraida else f"{estrutura_mt_nv2_desloc} desloc")
            
            # Estrutura MT NV3 - Adiciona TODAS as estruturas encontradas
            estrutura_mt_nv3_exist = dados_atual.get('estrutura_mt_nv3_exist', '')
            estrutura_mt_nv3_ret = dados_atual.get('estrutura_mt_nv3_ret', '')
            estrutura_mt_nv3_desloc = dados_atual.get('estrutura_mt_nv3_desloc', '')
            
            # SEMPRE adiciona a estrutura normal primeiro, se existir
            if valor_valido(estrutura_mt_nv3):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv3)
                valores_visiveis.append(estrutura_extraida if estrutura_extraida else estrutura_mt_nv3)
            
            # Adiciona estruturas com sufixos se existirem
            if valor_valido(estrutura_mt_nv3_exist):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv3_exist)
                valores_visiveis.append(f"{estrutura_extraida} exist" if estrutura_extraida else f"{estrutura_mt_nv3_exist} exist")
            if valor_valido(estrutura_mt_nv3_ret):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv3_ret)
                valores_visiveis.append(f"{estrutura_extraida} ret" if estrutura_extraida else f"{estrutura_mt_nv3_ret} ret")
            if valor_valido(estrutura_mt_nv3_desloc):
                estrutura_extraida = extrair_estrutura(estrutura_mt_nv3_desloc)
                valores_visiveis.append(f"{estrutura_extraida} desloc" if estrutura_extraida else f"{estrutura_mt_nv3_desloc} desloc")
            
            # Estrutura BT NV1 - Adiciona TODAS as estruturas encontradas
            estrutura_bt_exist = dados_atual.get('estrutura_bt_exist', '')
            estrutura_bt_ret = dados_atual.get('estrutura_bt_ret', '')
            estrutura_bt_desloc = dados_atual.get('estrutura_bt_desloc', '')
            
            # SEMPRE adiciona a estrutura normal primeiro, se existir
            if valor_valido(estrutura_bt):
                estrutura_extraida = extrair_estrutura(estrutura_bt)
                valores_visiveis.append(estrutura_extraida if estrutura_extraida else estrutura_bt)
            
            # Adiciona estruturas com sufixos se existirem
            if valor_valido(estrutura_bt_exist):
                estrutura_extraida = extrair_estrutura(estrutura_bt_exist)
                valores_visiveis.append(f"{estrutura_extraida} exist" if estrutura_extraida else f"{estrutura_bt_exist} exist")
            if valor_valido(estrutura_bt_ret):
                estrutura_extraida = extrair_estrutura(estrutura_bt_ret)
                valores_visiveis.append(f"{estrutura_extraida} ret" if estrutura_extraida else f"{estrutura_bt_ret} ret")
            if valor_valido(estrutura_bt_desloc):
                estrutura_extraida = extrair_estrutura(estrutura_bt_desloc)
                valores_visiveis.append(f"{estrutura_extraida} desloc" if estrutura_extraida else f"{estrutura_bt_desloc} desloc")
            
            # Estrutura BT NV2 - Adiciona TODAS as estruturas encontradas
            estrutura_bt_nv2_exist = dados_atual.get('estrutura_bt_nv2_exist', '')
            estrutura_bt_nv2_ret = dados_atual.get('estrutura_bt_nv2_ret', '')
            estrutura_bt_nv2_desloc = dados_atual.get('estrutura_bt_nv2_desloc', '')
            
            # SEMPRE adiciona a estrutura normal primeiro, se existir
            if valor_valido(estrutura_bt_nv2):
                estrutura_extraida = extrair_estrutura(estrutura_bt_nv2)
                valores_visiveis.append(estrutura_extraida if estrutura_extraida else estrutura_bt_nv2)
            
            # Adiciona estruturas com sufixos se existirem
            if valor_valido(estrutura_bt_nv2_exist):
                estrutura_extraida = extrair_estrutura(estrutura_bt_nv2_exist)
                valores_visiveis.append(f"{estrutura_extraida} exist" if estrutura_extraida else f"{estrutura_bt_nv2_exist} exist")
            if valor_valido(estrutura_bt_nv2_ret):
                estrutura_extraida = extrair_estrutura(estrutura_bt_nv2_ret)
                valores_visiveis.append(f"{estrutura_extraida} ret" if estrutura_extraida else f"{estrutura_bt_nv2_ret} ret")
            if valor_valido(estrutura_bt_nv2_desloc):
                estrutura_extraida = extrair_estrutura(estrutura_bt_nv2_desloc)
                valores_visiveis.append(f"{estrutura_extraida} desloc" if estrutura_extraida else f"{estrutura_bt_nv2_desloc} desloc")
            
            # Junta os valores com | apenas se houver valores válidos
            texto_visivel = " | ".join(valores_visiveis) if valores_visiveis else "Sem dados"
            
            # Adiciona o quadrado ao KML
            kml_content += f"""
    <Placemark>
        <name>Quadrado {i}</name>
        <description>
            <![CDATA[
            <h3>Quadrado na Bissetriz</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
            <p><strong>Status do Poste:</strong> {status_poste.upper()}</p>
            <p><strong>Coordenadas:</strong> {pt_atual[0]:.9f}, {pt_atual[1]:.9f}</p>
            <p><strong>Ângulo Anterior:</strong> {angulo_anterior:.2f}°</p>
            <p><strong>Ângulo Posterior:</strong> {angulo_posterior:.2f}°</p>
            <p><strong>Bissetriz:</strong> {bissetriz:.2f}°</p>
            <p><strong>Ângulo Final (Rotação):</strong> {angulo_final:.2f}°</p>
            <p><strong>Rotacao Poste:</strong> {rotacao_poste.upper()}</p>
            <p><strong>Base Concreto:</strong> {base_concreto}</p>
            <p><strong>Dimensões:</strong> {largura}m x {altura}m</p>

            <hr>
            <h4>Informações do Poste:</h4>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><td><strong>Sequência:</strong></td><td>{sequencia}</td></tr>
                <tr><td><strong>Status:</strong></td><td>{status_poste.upper()}</td></tr>
                <tr><td><strong>Número do Poste:</strong></td><td>{dados_atual['numero_poste'] if dados_atual['numero_poste'] else 'N/A'}</td></tr>
                <tr><td><strong>Estrutura MT NV1:</strong></td><td>{estrutura_mt}</td></tr>
                <tr><td><strong>Estrutura MT NV2:</strong></td><td>{estrutura_mt_nv2}</td></tr>
                <tr><td><strong>Estrutura MT NV3:</strong></td><td>{estrutura_mt_nv3}</td></tr>
                <tr><td><strong>Estrutura BT NV1:</strong></td><td>{estrutura_bt}</td></tr>
                <tr><td><strong>Estrutura BT NV2:</strong></td><td>{estrutura_bt_nv2}</td></tr>
                <tr><td><strong>Poste:</strong></td><td>{tipo_poste_para_exibir if tipo_poste_para_exibir else 'N/A'}</td></tr>
                <tr><td><strong>Base:</strong></td><td>{dados_atual['base'] if dados_atual['base'] else 'N/A'}</td></tr>
                <tr><td><strong>Base Concreto:</strong></td><td>{base_concreto}</td></tr>
                <tr><td><strong>Rotação Poste:</strong></td><td>{rotacao_poste.upper()}</td></tr>
            </table>
            ]]>
        </description>
        <styleUrl>#{estilo_poste}</styleUrl>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {lon1},{lat1},0 {lon2},{lat2},0 {lon3},{lat3},0 {lon4},{lat4},0 {lon1},{lat1},0
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
"""
            

            
            kml_content += """
        </Polygon>
    </Placemark>
"""
            
            # Adiciona elementos visuais especiais baseados no status do poste
            if status_poste == 'retirar':
                # Adiciona um X ligando os cantos do quadrado (azul)
                kml_content += f"""
     <Placemark>
         <name>X Retirar {i}</name>
         <description>X para poste a ser retirado</description>
         <styleUrl>#linha_azul_style</styleUrl>
         <LineString>
             <coordinates>
                 {lon1},{lat1},0 {lon3},{lat3},0
             </coordinates>
         </LineString>
     </Placemark>
     <Placemark>
         <name>X Retirar {i}</name>
         <description>X para poste a ser retirado</description>
         <styleUrl>#linha_azul_style</styleUrl>
         <LineString>
             <coordinates>
                 {lon2},{lat2},0 {lon4},{lat4},0
             </coordinates>
         </LineString>
     </Placemark>
 """
            elif status_poste == 'deslocar':
                # Adiciona uma linha diagonal (azul)
                kml_content += f"""
     <Placemark>
         <name>Diagonal Deslocar {i}</name>
         <description>Linha diagonal para poste a ser deslocado</description>
         <styleUrl>#linha_azul_style</styleUrl>
         <LineString>
             <coordinates>
                 {lon1},{lat1},0 {lon3},{lat3},0
             </coordinates>
         </LineString>
     </Placemark>
 """
            
            # Adiciona um label visível separado para as informações
            # Posiciona o label ligeiramente deslocado para a direita do centro do quadrado
            offset_lon = centro_lon + 0.0001  # Desloca 0.0001 graus para a direita
            offset_lat = centro_lat + 0.00005  # Desloca 0.00005 graus para cima
            
            kml_content += f"""
    <Placemark>
        <name>{texto_visivel}</name>
        <description>
            <![CDATA[
            <h3>Informações do Vértice {i}</h3>
            <p><strong>Sequência:</strong> {sequencia}</p>
                         <p><strong>Poste:</strong> {tipo_poste_para_exibir if tipo_poste_para_exibir else 'N/A'}</p>
            <p><strong>Estrutura MT:</strong> {estrutura_mt}</p>
            <p><strong>Estrutura BT:</strong> {estrutura_bt}</p>
            ]]>
        </description>
        <styleUrl>#label_style</styleUrl>
        <Point>
            <coordinates>{offset_lon},{offset_lat},0</coordinates>
        </Point>
    </Placemark>
"""
            
            # Chama a função modular para colocar elementos adicionais
            elementos_kml = colocar_elemento_kml(dados_atual, centro_lat, centro_lon, angulo_final, i, sequencia)
            kml_content += elementos_kml
        
        # Fecha o arquivo KML
        kml_content += """
</Document>
</kml>"""
        
        # Salva o arquivo KML
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        
        print(f"Arquivo KML '{caminho_completo}' gerado com sucesso.")
        print(f"Total de vértices: {len(pontos)}")
        print(f"Total de quadrados criados: {len(pontos)}")
        print(f"Quadrados 5x7 metros criados")
        print(f"Quadrados 6x6 criados para pontos com base_concreto='BC' (apenas bordas)")
        print(f"Estai âncora criado para pontos com estai_ancora='1EA' (linha + quadrado 1x1)")
        print(f"Linha conectando vértices criada")
        print(f"Labels visíveis adicionados com informações: Sequência, Poste, Estrutura MT, Estrutura BT")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar arquivo KML com quadrados: {e}")
        return False

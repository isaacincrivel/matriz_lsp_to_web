import os
from calculo_geografico import angle, polar

def criar_kml_quadrados_bissetriz(pontos_matriz, nome_arquivo="quadrados_bissetriz.kml"):
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
    <description>Quadrados de 5x3 metros (ou 6x6 metros para base_concreto=BC com apenas bordas) posicionados na bissetriz dos ângulos</description>
    
    <!-- Estilo para postes tipo 300 (quadrado vazio, só bordas) -->
    <Style id="poste_300_style">
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
    
    <!-- Estilo para postes tipo 600 (X no meio) -->
    <Style id="poste_600_style">
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
    
    <!-- Estilo para postes tipo 1000 (quadrado dentro) -->
    <Style id="poste_1000_style">
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
    
         <!-- Estilo padrão para outros tipos -->
     <Style id="quadrado_style">
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
     
    <!-- Estilo para a linha conectando os vértices -->
    <Style id="linha_vertices_style">
        <LineStyle>
            <color>ff00ff00</color>
            <width>3</width>
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
"""
        
        # Converte pontos_matriz para lista de coordenadas e dados
        pontos = []
        dados_pontos = []
        
        # Verifica se é DataFrame ou dicionário
        if hasattr(pontos_matriz, 'iterrows'):
            # É um DataFrame
            for index, row in pontos_matriz.iterrows():
                lat = float(str(row['lat']).replace(',', '.'))
                lon = float(str(row['long']).replace(',', '.'))
                pontos.append((lat, lon))
                dados_pontos.append({
                    'sequencia': index,  # Usa o índice do DataFrame
                    'numero_poste': row['numero_poste'],
                    'tipo_poste': row.get('tipo_poste', ''),  # Pode não existir mais
                    'estrutura_mt': row.get('estru_mt_nv1', ''),  # Usa o nome correto da coluna
                    'estrutura_mt_nv2': row.get('estru_mt_nv2', ''),
                    'estrutura_mt_nv3': row.get('estru_mt_nv3', ''),
                    'estrutura_bt': row.get('est_bt_nv1', ''),  # Usa o nome correto da coluna
                    'estrutura_bt_nv2': row.get('est_bt_nv2', ''),
                    'poste': row.get('tipo_poste', ''),  # Usa tipo_poste como poste (contém PDT10/600, etc.)
                    'tipo_poste': row.get('tipo_poste', ''),  # Usa tipo_poste para tipo_poste
                    'base': row.get('base_reforcada', ''),  # Usa base_reforcada como base
                    'base_concreto': row.get('base_concreto', ''),  # Adiciona base_concreto
                    'estai_ancora': row.get('estai_ancora', ''),  # Adiciona estai_ancora
                    'rotacao_poste': row.get('rotacao_poste', '')
                })
        else:
            # É um dicionário - precisa converter para o formato esperado
            vertices_list = list(pontos_matriz.keys())
            for i, vertex in enumerate(vertices_list):
                lat, lon = vertex[0], vertex[1]
                pontos.append((lat, lon))
                dados_vertex = pontos_matriz.get(vertex, {})
                dados_pontos.append({
                    'sequencia': i,  # Usa o índice do loop
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
            
            # Obtém informação do poste
            poste = dados_atual['poste'] if dados_atual['poste'] != '' else 'N/A'
            
            # Determina o tipo de poste baseado no texto após a "/"
            tipo_poste_numero = "padrao"
            if poste and '/' in str(poste):
                tipo_poste_numero = str(poste).split('/')[-1]
            
            # Define dimensões do poste baseadas no tipo (sempre as dimensões originais)
            if tipo_poste_numero == "600":
                largura = 5.0  # 5 metros
                altura = 3.0   # 3 metros
            elif tipo_poste_numero == "1000":
                largura = 7.0  # 7 metros
                altura = 4.0   # 4 metros
            else:
                # Tipo 300 ou padrão
                largura = 5.0  # 5 metros
                altura = 3.0   # 3 metros
            
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
            
            # Cria o texto visível que aparecerá na tela com todas as informações das estruturas
            # Filtra apenas os valores que não são 'nan' ou vazios
            valores_visiveis = []
            
            if sequencia is not None and str(sequencia) != 'N/A':
                valores_visiveis.append(str(sequencia))
            if poste and poste != 'N/A' and poste != 'nan':
                valores_visiveis.append(poste)
            if estrutura_mt and estrutura_mt != 'N/A' and estrutura_mt != 'nan':
                valores_visiveis.append(estrutura_mt)
            if estrutura_mt_nv2 and estrutura_mt_nv2 != 'N/A' and estrutura_mt_nv2 != 'nan':
                valores_visiveis.append(estrutura_mt_nv2)
            if estrutura_mt_nv3 and estrutura_mt_nv3 != 'N/A' and estrutura_mt_nv3 != 'nan':
                valores_visiveis.append(estrutura_mt_nv3)
            if estrutura_bt and estrutura_bt != 'N/A' and estrutura_bt != 'nan':
                valores_visiveis.append(estrutura_bt)
            if estrutura_bt_nv2 and estrutura_bt_nv2 != 'N/A' and estrutura_bt_nv2 != 'nan':
                valores_visiveis.append(estrutura_bt_nv2)
            
            # Junta os valores com | apenas se houver valores válidos
            texto_visivel = " | ".join(valores_visiveis) if valores_visiveis else "Sem dados"
            
            # Seleciona o estilo baseado no tipo de poste (normal)
            if tipo_poste_numero == "300":
                estilo_poste = "poste_300_style"
            elif tipo_poste_numero == "600":
                estilo_poste = "poste_600_style"
            elif tipo_poste_numero == "1000":
                estilo_poste = "poste_1000_style"
            else:
                estilo_poste = "quadrado_style"
            
            # Adiciona o quadrado ao KML
            kml_content += f"""
    <Placemark>
        <name>Quadrado {i}</name>
        <description>
            <![CDATA[
            <h3>Quadrado na Bissetriz</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
            <p><strong>Coordenadas:</strong> {pt_atual[0]:.9f}, {pt_atual[1]:.9f}</p>
            <p><strong>Ângulo Anterior:</strong> {angulo_anterior:.2f}°</p>
            <p><strong>Ângulo Posterior:</strong> {angulo_posterior:.2f}°</p>
            <p><strong>Bissetriz:</strong> {bissetriz:.2f}°</p>
            <p><strong>Ângulo Final (Rotação):</strong> {angulo_final:.2f}°</p>
            <p><strong>Rotacao Poste:</strong> {rotacao_poste.upper()}</p>
            <p><strong>Base Concreto:</strong> {base_concreto}</p>
            <p><strong>Dimensões:</strong> {largura}m x {altura}m</p>
            <p><strong>Tipo de Poste:</strong> {tipo_poste_numero}</p>
            <hr>
            <h4>Informações do Poste:</h4>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><td><strong>Sequência:</strong></td><td>{sequencia}</td></tr>
                <tr><td><strong>Número do Poste:</strong></td><td>{dados_atual['numero_poste'] if dados_atual['numero_poste'] else 'N/A'}</td></tr>
                <tr><td><strong>Tipo do Poste:</strong></td><td>{dados_atual['tipo_poste'] if dados_atual['tipo_poste'] else 'N/A'}</td></tr>
                <tr><td><strong>Estrutura MT NV1:</strong></td><td>{estrutura_mt}</td></tr>
                <tr><td><strong>Estrutura MT NV2:</strong></td><td>{estrutura_mt_nv2}</td></tr>
                <tr><td><strong>Estrutura MT NV3:</strong></td><td>{estrutura_mt_nv3}</td></tr>
                <tr><td><strong>Estrutura BT NV1:</strong></td><td>{estrutura_bt}</td></tr>
                <tr><td><strong>Estrutura BT NV2:</strong></td><td>{estrutura_bt_nv2}</td></tr>
                <tr><td><strong>Poste:</strong></td><td>{poste}</td></tr>
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
            
            # Adiciona elementos específicos baseados no tipo de poste
            # Para base_concreto=BC, ainda adiciona elementos internos baseados no tipo de poste
            if tipo_poste_numero == "600":
                # Adiciona metade pintada na diagonal (triângulo)
                # Calcula os pontos para o triângulo diagonal
                tri_lat1, tri_lon1 = polar(centro_lat, centro_lon, largura/2, angulo_final - 90)
                tri_lat1, tri_lon1 = polar(tri_lat1, tri_lon1, altura/2, angulo_final)
                
                tri_lat2, tri_lon2 = polar(centro_lat, centro_lon, largura/2, angulo_final + 90)
                tri_lat2, tri_lon2 = polar(tri_lat2, tri_lon2, altura/2, angulo_final + 180)
                
                tri_lat3, tri_lon3 = polar(centro_lat, centro_lon, largura/2, angulo_final - 90)
                tri_lat3, tri_lon3 = polar(tri_lat3, tri_lon3, altura/2, angulo_final + 180)
                
                kml_content += f"""
            <innerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {tri_lon1},{tri_lat1},0 {tri_lon2},{tri_lat2},0 {tri_lon3},{tri_lat3},0 {tri_lon1},{tri_lat1},0
                    </coordinates>
                </LinearRing>
            </innerBoundaryIs>
"""
            elif tipo_poste_numero == "1000":
                # Adiciona um quadrado interno
                # Calcula os vértices do quadrado interno (metade do tamanho)
                inner_largura = largura / 2
                inner_altura = altura / 2
                
                # Vértices do quadrado interno
                inner_lat1, inner_lon1 = polar(centro_lat, centro_lon, inner_largura/2, angulo_final - 90)
                inner_lat1, inner_lon1 = polar(inner_lat1, inner_lon1, inner_altura/2, angulo_final)
                
                inner_lat2, inner_lon2 = polar(centro_lat, centro_lon, inner_largura/2, angulo_final + 90)
                inner_lat2, inner_lon2 = polar(inner_lat2, inner_lon2, inner_altura/2, angulo_final)
                
                inner_lat3, inner_lon3 = polar(centro_lat, centro_lon, inner_largura/2, angulo_final + 90)
                inner_lat3, inner_lon3 = polar(inner_lat3, inner_lon3, inner_altura/2, angulo_final + 180)
                
                inner_lat4, inner_lon4 = polar(centro_lat, centro_lon, inner_largura/2, angulo_final - 90)
                inner_lat4, inner_lon4 = polar(inner_lat4, inner_lon4, inner_altura/2, angulo_final + 180)
                
                kml_content += f"""
            <innerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {inner_lon1},{inner_lat1},0 {inner_lon2},{inner_lat2},0 {inner_lon3},{inner_lat3},0 {inner_lon4},{inner_lat4},0 {inner_lon1},{inner_lat1},0
                    </coordinates>
                </LinearRing>
            </innerBoundaryIs>
"""
            
            kml_content += """
        </Polygon>
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
            <p><strong>Poste:</strong> {poste}</p>
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
            
            # Verifica se tem base_concreto "BC" para adicionar elemento adicional
            if base_concreto == 'BC':
                # Define dimensões da base concreta: 6x6 metros
                base_largura = 6.0
                base_altura = 6.0
                
                # Calcula os vértices da base_concreto (6x6 metros)
                # Vértice 1: frente-esquerda
                base_lat1, base_lon1 = polar(centro_lat, centro_lon, base_largura/2, angulo_final - 90)
                base_lat1, base_lon1 = polar(base_lat1, base_lon1, base_altura/2, angulo_final)
                
                # Vértice 2: frente-direita
                base_lat2, base_lon2 = polar(centro_lat, centro_lon, base_largura/2, angulo_final + 90)
                base_lat2, base_lon2 = polar(base_lat2, base_lon2, base_altura/2, angulo_final)
                
                # Vértice 3: trás-direita
                base_lat3, base_lon3 = polar(centro_lat, centro_lon, base_largura/2, angulo_final + 90)
                base_lat3, base_lon3 = polar(base_lat3, base_lon3, base_altura/2, angulo_final + 180)
                
                # Vértice 4: trás-esquerda
                base_lat4, base_lon4 = polar(centro_lat, centro_lon, base_largura/2, angulo_final - 90)
                base_lat4, base_lon4 = polar(base_lat4, base_lon4, base_altura/2, angulo_final + 180)
                
                kml_content += f"""
    <Placemark>
        <name>Base Concreto {i}</name>
        <description>
            <![CDATA[
            <h3>Base de Concreto</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
            <p><strong>Coordenadas:</strong> {pt_atual[0]:.9f}, {pt_atual[1]:.9f}</p>
            <p><strong>Ângulo Final (Rotação):</strong> {angulo_final:.2f}°</p>
            <p><strong>Dimensões:</strong> {base_largura}m x {base_altura}m</p>
            <p><strong>Tipo:</strong> Base de Concreto (BC)</p>
            ]]>
        </description>
        <styleUrl>#poste_300_style</styleUrl>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {base_lon1},{base_lat1},0 {base_lon2},{base_lat2},0 {base_lon3},{base_lat3},0 {base_lon4},{base_lat4},0 {base_lon1},{base_lat1},0
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
"""
            
            # Verifica se tem estai âncora (1EA)
            estai_ancora = str(dados_atual.get('estai_ancora', '')).strip()
            if estai_ancora == '1EA':
                # Cria uma linha com quadrado de 1x1 na ponta
                # A linha sai do centro do poste na direção do ângulo do poste + 180 graus
                linha_comprimento = 10.0  # 10 metros de comprimento
                
                # Rotaciona 180 graus em relação ao ângulo do poste
                angulo_estai = angulo_final + 270
                
                # Ponto final da linha (onde fica o quadrado)
                linha_lat_fim, linha_lon_fim = polar(centro_lat, centro_lon, linha_comprimento, angulo_estai)
                
                # Adiciona a linha do estai âncora
                kml_content += f"""
    <Placemark>
        <name>Estai Âncora {i}</name>
        <description>
            <![CDATA[
            <h3>Estai Âncora</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
                         <p><strong>Comprimento:</strong> {linha_comprimento}m</p>
             <p><strong>Ângulo:</strong> {angulo_estai:.2f}°</p>
            ]]>
        </description>
        <styleUrl>#estai_ancora_style</styleUrl>
        <LineString>
            <coordinates>
                {centro_lon},{centro_lat},0 {linha_lon_fim},{linha_lat_fim},0
            </coordinates>
        </LineString>
    </Placemark>
"""
                
                # Adiciona o quadrado de 1x1 na ponta da linha
                quadrado_tamanho = 1.0  # 1 metro
                
                                # Vértices do quadrado de 1x1 na ponta da linha
                quad_lat1, quad_lon1 = polar(linha_lat_fim, linha_lon_fim, quadrado_tamanho/2, angulo_estai - 90)
                quad_lat1, quad_lon1 = polar(quad_lat1, quad_lon1, quadrado_tamanho/2, angulo_estai)
                
                quad_lat2, quad_lon2 = polar(linha_lat_fim, linha_lon_fim, quadrado_tamanho/2, angulo_estai + 90)
                quad_lat2, quad_lon2 = polar(quad_lat2, quad_lon2, quadrado_tamanho/2, angulo_estai)
                
                quad_lat3, quad_lon3 = polar(linha_lat_fim, linha_lon_fim, quadrado_tamanho/2, angulo_estai + 90)
                quad_lat3, quad_lon3 = polar(quad_lat3, quad_lon3, quadrado_tamanho/2, angulo_estai + 180)
                
                quad_lat4, quad_lon4 = polar(linha_lat_fim, linha_lon_fim, quadrado_tamanho/2, angulo_estai - 90)
                quad_lat4, quad_lon4 = polar(quad_lat4, quad_lon4, quadrado_tamanho/2, angulo_estai + 180)
                
                kml_content += f"""
    <Placemark>
        <name>Quadrado Estai Âncora {i}</name>
        <description>
            <![CDATA[
            <h3>Quadrado do Estai Âncora</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
                         <p><strong>Dimensões:</strong> 1m x 1m</p>
             <p><strong>Ângulo:</strong> {angulo_estai:.2f}°</p>
            ]]>
        </description>
        <styleUrl>#estai_ancora_quadrado_style</styleUrl>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {quad_lon1},{quad_lat1},0 {quad_lon2},{quad_lat2},0 {quad_lon3},{quad_lat3},0 {quad_lon4},{quad_lat4},0 {quad_lon1},{quad_lat1},0
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
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
        print(f"Total de vértices: {len(pontos)}")
        print(f"Total de quadrados criados: {len(pontos)}")
        print(f"Quadrados 6x6 criados para pontos com base_concreto='BC' (apenas bordas)")
        print(f"Estai âncora criado para pontos com estai_ancora='1EA' (linha + quadrado 1x1)")
        print(f"Linha conectando vértices criada")
        print(f"Labels visíveis adicionados com informações: Sequência, Poste, Estrutura MT, Estrutura BT")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar arquivo KML com quadrados: {e}")
        return False

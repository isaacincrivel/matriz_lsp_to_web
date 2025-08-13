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
    <description>Quadrados de 5x3 metros posicionados na bissetriz dos ângulos</description>
    
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
                    'tipo_poste': row['tipo_poste'],
                    'estrutura_mt': row['estrutura_mt'],
                    'estrutura_bt': row['estrutura_bt'],
                    'poste': row['poste'],
                    'base': row['base']
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
                    'estrutura_bt': dados_vertex.get('estrutura_bt', ''),
                    'poste': dados_vertex.get('poste', ''),
                    'base': dados_vertex.get('base', '')
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
        
        # Para cada ponto (exceto o primeiro e último), cria um quadrado na bissetriz
        for i in range(1, len(pontos) - 1):
            pt_anterior = pontos[i - 1]
            pt_atual = pontos[i]
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
            
            # Calcula os vértices do quadrado de 5x3 metros
            # O quadrado será orientado na direção da bissetriz
            largura = 5.0  # 5 metros
            altura = 3.0   # 3 metros
            
            # Calcula os quatro vértices do quadrado
            # Ponto central do quadrado será o vértice atual
            centro_lat, centro_lon = pt_atual
            
            # Vértice 1: frente-esquerda
            lat1, lon1 = polar(centro_lat, centro_lon, largura/2, bissetriz - 90)
            lat1, lon1 = polar(lat1, lon1, altura/2, bissetriz)
            
            # Vértice 2: frente-direita
            lat2, lon2 = polar(centro_lat, centro_lon, largura/2, bissetriz + 90)
            lat2, lon2 = polar(lat2, lon2, altura/2, bissetriz)
            
            # Vértice 3: trás-direita
            lat3, lon3 = polar(centro_lat, centro_lon, largura/2, bissetriz + 90)
            lat3, lon3 = polar(lat3, lon3, altura/2, bissetriz + 180)
            
            # Vértice 4: trás-esquerda
            lat4, lon4 = polar(centro_lat, centro_lon, largura/2, bissetriz - 90)
            lat4, lon4 = polar(lat4, lon4, altura/2, bissetriz + 180)
            
            # Obtém os dados do ponto atual
            dados_atual = dados_pontos[i]
            
            # Cria o texto visível para o quadrado com as informações solicitadas
            sequencia = dados_atual['sequencia'] if dados_atual['sequencia'] != '' else 'N/A'
            poste = dados_atual['poste'] if dados_atual['poste'] != '' else 'N/A'
            estrutura_mt = dados_atual['estrutura_mt'] if dados_atual['estrutura_mt'] != '' else 'N/A'
            estrutura_bt = dados_atual['estrutura_bt'] if dados_atual['estrutura_bt'] != '' else 'N/A'
            
            # Cria o texto visível que aparecerá na tela
            texto_visivel = f"Seq:{sequencia} | P:{poste} | MT:{estrutura_mt} | BT:{estrutura_bt}"
            
            # Determina o tipo de poste baseado no texto após a "/"
            tipo_poste_numero = "padrao"
            if poste and '/' in str(poste):
                tipo_poste_numero = str(poste).split('/')[-1]
            
            # Seleciona o estilo baseado no tipo de poste
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
            <p><strong>Dimensões:</strong> 5m x 3m</p>
            <p><strong>Tipo de Poste:</strong> {tipo_poste_numero}</p>
            <hr>
            <h4>Informações do Poste:</h4>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><td><strong>Sequência:</strong></td><td>{sequencia}</td></tr>
                <tr><td><strong>Número do Poste:</strong></td><td>{dados_atual['numero_poste'] if dados_atual['numero_poste'] else 'N/A'}</td></tr>
                <tr><td><strong>Tipo do Poste:</strong></td><td>{dados_atual['tipo_poste'] if dados_atual['tipo_poste'] else 'N/A'}</td></tr>
                <tr><td><strong>Estrutura MT:</strong></td><td>{estrutura_mt}</td></tr>
                <tr><td><strong>Estrutura BT:</strong></td><td>{estrutura_bt}</td></tr>
                <tr><td><strong>Poste:</strong></td><td>{poste}</td></tr>
                <tr><td><strong>Base:</strong></td><td>{dados_atual['base'] if dados_atual['base'] else 'N/A'}</td></tr>
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
            if tipo_poste_numero == "600":
                # Adiciona metade pintada na diagonal (triângulo)
                # Calcula os pontos para o triângulo diagonal
                tri_lat1, tri_lon1 = polar(centro_lat, centro_lon, largura/2, bissetriz - 90)
                tri_lat1, tri_lon1 = polar(tri_lat1, tri_lon1, altura/2, bissetriz)
                
                tri_lat2, tri_lon2 = polar(centro_lat, centro_lon, largura/2, bissetriz + 90)
                tri_lat2, tri_lon2 = polar(tri_lat2, tri_lon2, altura/2, bissetriz + 180)
                
                tri_lat3, tri_lon3 = polar(centro_lat, centro_lon, largura/2, bissetriz - 90)
                tri_lat3, tri_lon3 = polar(tri_lat3, tri_lon3, altura/2, bissetriz + 180)
                
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
                inner_lat1, inner_lon1 = polar(centro_lat, centro_lon, inner_largura/2, bissetriz - 90)
                inner_lat1, inner_lon1 = polar(inner_lat1, inner_lon1, inner_altura/2, bissetriz)
                
                inner_lat2, inner_lon2 = polar(centro_lat, centro_lon, inner_largura/2, bissetriz + 90)
                inner_lat2, inner_lon2 = polar(inner_lat2, inner_lon2, inner_altura/2, bissetriz)
                
                inner_lat3, inner_lon3 = polar(centro_lat, centro_lon, inner_largura/2, bissetriz + 90)
                inner_lat3, inner_lon3 = polar(inner_lat3, inner_lon3, inner_altura/2, bissetriz + 180)
                
                inner_lat4, inner_lon4 = polar(centro_lat, centro_lon, inner_largura/2, bissetriz - 90)
                inner_lat4, inner_lon4 = polar(inner_lat4, inner_lon4, inner_altura/2, bissetriz + 180)
                
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
        
        # Fecha o arquivo KML
        kml_content += """
</Document>
</kml>"""
        
        # Salva o arquivo KML
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        
        print(f"Arquivo KML '{caminho_completo}' gerado com sucesso.")
        print(f"Total de vértices: {len(pontos)}")
        print(f"Total de quadrados criados: {len(pontos) - 2}")
        print(f"Linha conectando vértices criada")
        print(f"Labels visíveis adicionados com informações: Sequência, Poste, Estrutura MT, Estrutura BT")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar arquivo KML com quadrados: {e}")
        return False

from calculo_geografico import polar

"""
MÓDULO DE ELEMENTOS KML
=======================

Este módulo contém as funções modulares para criar elementos KML específicos:

1. colocar_elemento_kml() - Função principal que verifica todas as variáveis
2. cria_desenho_elemento_kml() - Função que cria o desenho específico de cada elemento

VARIÁVEIS SUPORTADAS:
- estai_ancora: "1EA" -> Linha + quadrado 1x1
- base_concreto: "BC" -> Octógono de raio 6m (apenas bordas)
- aterr_neutro: "AN" -> Círculo pequeno
- base_reforcada: (a implementar)
- chave: (a implementar)
- trafo: (a implementar)
- equipamento: (a implementar)
- faixa: (a implementar)
- cort_arvores_isol: (a implementar)
- adiconal_1 a adiconal_7: (a implementar)
- qdt_adic_1 a qdt_adic_6: (a implementar)

Para adicionar novos elementos:
1. Adicione a condição em cria_desenho_elemento_kml()
2. A variável já está na lista de variaveis_elementos em colocar_elemento_kml()
"""

def cria_desenho_elemento_kml(elemento_tipo, dados_elemento, centro_lat, centro_lon, angulo_final, i, sequencia):
    """
    Cria o desenho específico de cada elemento KML
    
    Args:
        elemento_tipo: Tipo do elemento (base_concreto, estai_ancora, etc.)
        dados_elemento: Dados específicos do elemento
        centro_lat, centro_lon: Coordenadas do centro
        angulo_final: Ângulo de orientação
        i: Índice do vértice
        sequencia: Número da sequência
    
    Returns:
        str: Conteúdo KML do elemento
    """
    kml_content = ""
    
    if elemento_tipo == "base_concreto" and dados_elemento == "BC":
        # Base de concreto: octógono de raio 6 metros
        raio = 6.0
        
        # Cria um octógono (8 lados) com raio de 6 metros
        pontos_octogono = []
        for angulo in range(0, 360, 45):  # 360° / 8 = 45° entre cada vértice
            # Calcula a posição de cada vértice do octógono
            angulo_rad = angulo * 3.14159 / 180
            # Aplica a rotação do poste ao octógono
            angulo_final_rad = angulo_final * 3.14159 / 180
            angulo_total = angulo_rad + angulo_final_rad
            
            # Calcula as coordenadas do vértice
            lat_vertice = centro_lat + raio * 0.00001 * (angulo_total)
            lon_vertice = centro_lon + raio * 0.00001 * (angulo_total)
            pontos_octogono.append(f"{lon_vertice},{lat_vertice},0")
        
        coordenadas_octogono = " ".join(pontos_octogono)
        
        kml_content = f"""
    <Placemark>
        <name>Base Concreto {i}</name>
        <description>
            <![CDATA[
            <h3>Base de Concreto</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
            <p><strong>Coordenadas:</strong> {centro_lat:.9f}, {centro_lon:.9f}</p>
            <p><strong>Ângulo Final (Rotação):</strong> {angulo_final:.2f}°</p>
            <p><strong>Raio:</strong> {raio}m</p>
            <p><strong>Forma:</strong> Octógono (8 lados)</p>
            <p><strong>Tipo:</strong> Base de Concreto (BC)</p>
            ]]>
        </description>
        <styleUrl>#poste_implantar_style</styleUrl>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {coordenadas_octogono}
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
"""
    
    elif elemento_tipo == "estai_ancora" and dados_elemento == "1EA":
        # Estai âncora: linha + quadrado 1x1
        linha_comprimento = 10.0
        angulo_estai = angulo_final + 270
        
        # Ponto final da linha
        linha_lat_fim, linha_lon_fim = polar(centro_lat, centro_lon, linha_comprimento, angulo_estai)
        
        # Linha do estai âncora
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
        
        # Quadrado de 1x1 na ponta da linha
        quadrado_tamanho = 1.0
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
    
    elif elemento_tipo == "aterr_neutro" and dados_elemento == "AN":
        # Aterramento neutro: círculo pequeno
        raio = 0.5  # 0.5 metros de raio
        
        # Cria um círculo simples (aproximado por um octágono)
        pontos_circulo = []
        for angulo in range(0, 360, 45):
            angulo_rad = angulo * 3.14159 / 180
            lat_circulo = centro_lat + raio * 0.00001 * (angulo_rad + angulo_final * 3.14159 / 180)
            lon_circulo = centro_lon + raio * 0.00001 * (angulo_rad + angulo_final * 3.14159 / 180)
            pontos_circulo.append(f"{lon_circulo},{lat_circulo},0")
        
        coordenadas_circulo = " ".join(pontos_circulo)
        
        kml_content = f"""
    <Placemark>
        <name>Aterramento Neutro {i}</name>
        <description>
            <![CDATA[
            <h3>Aterramento Neutro</h3>
            <p><strong>Vértice:</strong> {i}</p>
            <p><strong>Sequência:</strong> {sequencia}</p>
            <p><strong>Coordenadas:</strong> {centro_lat:.9f}, {centro_lon:.9f}</p>
            <p><strong>Raio:</strong> {raio}m</p>
            <p><strong>Tipo:</strong> Aterramento Neutro (AN)</p>
            ]]>
        </description>
        <styleUrl>#poste_implantar_style</styleUrl>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        {coordenadas_circulo}
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
"""
    
    # Adicionar outros elementos conforme necessário
    # elif elemento_tipo == "chave" and dados_elemento == "valor":
    #     # Implementar desenho da chave
    #     pass
    # elif elemento_tipo == "trafo" and dados_elemento == "valor":
    #     # Implementar desenho do transformador
    #     pass
    
    return kml_content

def colocar_elemento_kml(dados_atual, centro_lat, centro_lon, angulo_final, i, sequencia):
    """
    Verifica as condições de cada variável e chama a função de desenho apropriada
    
    Args:
        dados_atual: Dicionário com todos os dados do ponto
        centro_lat, centro_lon: Coordenadas do centro
        angulo_final: Ângulo de orientação
        i: Índice do vértice
        sequencia: Número da sequência
    
    Returns:
        str: Conteúdo KML de todos os elementos
    """
    kml_content = ""
    
    # Lista de variáveis para verificar
    variaveis_elementos = [
        "estai_ancora",
        "base_reforcada", 
        "base_concreto",
        "aterr_neutro",
        "chave",
        "trafo",
        "equipamento",
        "faixa",
        "cort_arvores_isol",
        "adiconal_1",
        "qdt_adic_1",
        "adiconal_2", 
        "qdt_adic_2",
        "adiconal_3",
        "qdt_adic_3", 
        "adiconal_4",
        "qdt_adic_4",
        "adiconal_5",
        "qdt_adic_5",
        "adiconal_6",
        "qdt_adic_6", 
        "adiconal_7"
    ]
    
    # Verifica cada variável
    for variavel in variaveis_elementos:
        valor = str(dados_atual.get(variavel, '')).strip()
        
        if valor and valor != 'nan' and valor != '':
            # Chama a função de desenho para cada elemento
            elemento_kml = cria_desenho_elemento_kml(variavel, valor, centro_lat, centro_lon, angulo_final, i, sequencia)
            kml_content += elemento_kml
    
    return kml_content

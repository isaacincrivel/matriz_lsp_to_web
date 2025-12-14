from math import radians, sin, cos, sqrt, atan2, degrees, asin
import pandas as pd
import math


##################################################################################################################################

def distance(lat1, lon1, lat2, lon2):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


##################################################################################################################################
def angle(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    initial_bearing = atan2(x, y)
    initial_bearing = degrees(initial_bearing)
    return (initial_bearing + 360) % 360

##################################################################################################################################
def polar(lat, lon, distancia_metros, bearing_graus):
    R = 6371000
    lat1 = radians(lat)
    lon1 = radians(lon)
    bearing = radians(bearing_graus)
    distancia = distancia_metros
    lat2 = asin(sin(lat1) * cos(distancia / R) + cos(lat1) * sin(distancia / R) * cos(bearing))
    lon2 = lon1 + atan2(
        sin(bearing) * sin(distancia / R) * cos(lat1),
        cos(distancia / R) - sin(lat1) * sin(lat2)
    )
    return degrees(lat2), degrees(lon2)

##################################################################################################################################
def get_loose_gap(loose_gap, vertices):
    if loose_gap != "SIM":
        return vertices, "NÃO"
    
    else:
        first_point = vertices[0]
        second_point = vertices[1]
        distance_between = distance(first_point[0], first_point[1], second_point[0], second_point[1])

        if  distance_between > 60:
            angle_between = angle(first_point[0], first_point[1], second_point[0], second_point[1])
            new_point = polar(first_point[0], first_point[1], 30, angle_between)
            return [first_point, new_point, second_point] + vertices[2:], "SIM"
        return vertices, "NÃO"


##################################################################################################################################
def dividir_tramo(vertices, section_size):
    new_vertices = []
    for i in range(len(vertices) - 1):
        pto1 = vertices[i]
        pto2 = vertices[i + 1]
        new_vertices.append(pto1)
        dst1 = distance(pto1[0], pto1[1], pto2[0], pto2[1])
        if dst1 > section_size:
            num_divisoes = int(dst1 // section_size)
            distancia_por_tramo = dst1 / (num_divisoes + 1)
            ang = angle(pto1[0], pto1[1], pto2[0], pto2[1])
            for j in range(1, num_divisoes + 1):
                novo_pto = polar(pto1[0], pto1[1], distancia_por_tramo * j, ang)
                new_vertices.append(novo_pto)
    new_vertices.append(vertices[-1])
    return new_vertices

##################################################################################################################################
def intercalar_vertices(vertices, lista_nao_intercalar, gap_size):
    new_vertices = []
    for i in range(len(vertices) - 1):
        pto1 = vertices[i]
        pto2 = vertices[i + 1]
        new_vertices.append(pto1)
        
        if i in lista_nao_intercalar:
            continue
        
        dst = distance(pto1[0], pto1[1], pto2[0], pto2[1])
        if dst > gap_size:
            num_divisoes = int(dst // gap_size)
            if num_divisoes > 0:
                distancia_por_tramo = dst / (num_divisoes + 1)
                ang = angle(pto1[0], pto1[1], pto2[0], pto2[1])
                for j in range(1, num_divisoes + 1):
                    novo_pto = polar(pto1[0], pto1[1], distancia_por_tramo * j, ang)
                    new_vertices.append(novo_pto)

    new_vertices.append(vertices[-1])
    return new_vertices


##################################################################################################################################
def distance_ptos (pto1 , pto2):

    distance_between = distance(pto1[0], pto1[1], pto2[0], pto2[1])
    
    return distance_between



##################################################################################################################################
def mtz_abaco(str1):
    abacos = {}    
    abacos["MT7"] = [
        
        ["PDT10/300", "UP1", "",  "BS", [(-1.0, 0.0), (-1.0, 217.143), (160.0, 217.143), (160.0, 0.0), (-1.0, 0.0)]], #ms1
        ["UP1","", "PDT10/600", "BC", [(160.0, 0.0), (160.0, 217.143), (350.0, 0.0), (160.0, 0.0)]], #ms2
        ["UP4","", "PDT10/600", "BC", [(160.0, 217.143), (160.0, 300.0), (600.0, 100.0), (600.0, 0.0), (350.0, 0.0), (160.0, 217.143)]], #ms3
        ["UP4","", "PDT10/600", "BC", [(-1.0, 217.143), (-1.0, 401.143), (160.0, 217.143), (-1.0, 217.143)]],#ms4
        ["UP4","", "PDT10/1000", "BC", [(-1.0, 401.143), (-1.0, 500.0), (600.0, 500.0), (600.0, 100.0), (160.0, 300.0), (160.0, 217.143), (-1.0, 401.143)]], #ms5
        ["U3/U3","", "PDT10/1500", "BC", [(600.0, 220.0), (600.0, 500.0), (900.0, 500.0), (900.0, 220.0), (600.0, 220.0)]], #ms6
        ["U3","", "PDT10/1000", "ES", [(600.0, 0.0), (600.0, 220.0), (900.0, 220.0), (900.0, 0.0), (600.0, 0.0)]], #ms7    
        ["U3","", "PDT10/600", "BC", [(900.0, 220.0), (1000.0, 220.0), (1000.0, 1.39955e-12), (900.0, 9.09495e-13), (900.0, 220.0)]], #ms8
        ["U3","", "PDT10/1000", "BC", [(900.0, 220.0), (900.0, 500.0), (1000.0, 500.0), (1000.0, 220.0), (900.0, 220.0)]], #ms9
        ["U3","", "PDT11/300", "BS", [(1000.0, 35.0), (1100.0, 35.0), (1100.0, 9.09495e-13), (1000.0, 1.39266e-12), (1000.0, 35.0)]], #ms10
        ["U3","", "PDT11/1000", "BC", [(1000.0, 220.0), (1100.0, 220.0), (1100.0, 35.0), (1000.0, 35.0), (1000.0, 220.0)]], #ms11
        ["U3","", "EXIST", "BE", [(1100.0, 35.0), (1200.0, 35.0), (1200.0, 9.09495e-13), (1100.0, 1.39266e-12), (1100.0, 35.0)]], #ms12
        ["U3","", "EXIST", "ES", [(1100.0, 220.0), (1200.0, 220.0), (1200.0, 35.0), (1100.0, 35.0), (1100.0, 220.0)]] #ms13
    ]  
    abacos["MT8"] = [
        ["UP1","", "PDT10/300", "BS", [(-1.0, 0.0), (160.0, 0.0), (160.0, 217.143), (-1.0, 217.143), (-1.0, 0.0)]],
        ["UP1","", "PDT10/300", "ES", [(160.0, 217.143), (160.0, 0.0), (350.0, 0.0), (160.0, 217.143)]],
        ["UP4","", "PDT10/300", "ED", [(-1.0, 217.143), (-1.0, 500.0), (160.0, 500.0), (160.0, 300.0), (600.0, 180.0), (600.0, 0.0), (350.0, 0.0), (160.0, 217.143), (-1.0, 217.143)]],
        ["U3","U3", "PDT10/300", "ED", [(600.0, 220.0), (600.0, 0.0), (900.0, 0.0), (900.0, 220.0), (600.0, 220.0)]],
        ["UP4","", "PDT10/300", "ET", [(160.0, 300.0), (160.0, 500.0), (600.0, 500.0), (600.0, 180.0), (160.0, 300.0)]],
        ["U3/U3","", "PDT10/600", "ET", [(600.0, 220.0), (600.0, 500.0), (900.0, 500.0), (900.0, 220.0), (600.0, 220.0)]],
        ["U3","", "PDT10/300", "ET", [(900.0, 220.0), (900.0, 500.0), (1100.0, 500.0), (1100.0, 220.0), (900.0, 220.0)]],
        ["U3","", "PDT10/300", "ES", [(900.0, 0.0), (900.0, 220.0), (1100.0, 220.0), (1100.0, 0.0), (900.0, 0.0)]],
        ["UP4","", "PDT10/300", "ED", [(1100.0, 217.143), (1300.0, 217.143), (1300.0, 0.0), (1100.0, 0.0), (1100.0, 217.143)]]
    ]
    return abacos.get(str1, [])

##################################################################################################################################
def point_in_polygon(polygon, point):
    x, y = point
    odd = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi < y and yj >= y) or (yj < y and yi >= y)):
            if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                odd = not odd
        j = i
    return odd

##################################################################################################################################
def mosaico(ang1, dist1, str1):
    ang1 = ang1 * 10
    abaco = mtz_abaco(str1)
    ptx = (ang1, dist1)

    for entry in abaco:
        def_estrutura, def_estruturabt,  def_poste, def_base, polygon = entry
        if point_in_polygon(polygon, ptx):
            return [def_estrutura, def_estruturabt, def_poste, def_base]

    ## se não der nada tem que retornar algo padrão
    print(f"ERRO: Não foi possível encontrar correspondência no ábaco para:")
    print(f"  - Ângulo: {ang1}")
    print(f"  - Distância: {dist1}")
    print(f"  - Módulo: {str1}")
    print(f"  - Ponto: {ptx}")
    print(f"  - Ábaco disponível: {len(abaco)} entradas")
    return None

##################################################################################################################################
def gravar_pontos_matriz(new_vertices, sequencia, estrutura_mt, estrutura_bt, poste, base):
    """
    Função que grava os pontos da matriz com seus dados associados.
    
    Args:
        new_vertices: Lista de vértices (pontos) no formato [(lat, lon), ...]
        sequencia: Índice do ponto na lista (0, 1, 2, ...)
        estrutura_mt: Dados da estrutura MT (ex: "D1")
        estrutura_bt: Dados da estrutura BT (ex: "D2")
        poste: Dados do poste (ex: "P23")
        base: Dados da base (ex: "B1")
    
    Returns:
        dict: Dicionário com os pontos e seus dados associados
    """
    pontos_matriz = {}
    
    # Verifica se a sequência é válida
    if sequencia < 0 or sequencia >= len(new_vertices):
        print(f"Erro: Sequência {sequencia} inválida. Deve estar entre 0 e {len(new_vertices)-1}")
        return pontos_matriz
    
    # Adiciona todos os pontos de new_vertices ao dicionário
    for i, ponto in enumerate(new_vertices):
        pontos_matriz[ponto] = {}
    
    # Adiciona os dados específicos no ponto indicado pela sequência
    ponto_especifico = new_vertices[sequencia]
    pontos_matriz[ponto_especifico] = {
        "estrutura_mt": estrutura_mt,
        "estrutura_bt": estrutura_bt,
        "poste": poste,
        "base": base
    }
    
    return pontos_matriz

##################################################################################################################################
def poste_derivacao( new_vertices, loose_gap, tipo_poste, module_name):   
    pto1 = new_vertices[0]
    pto2 = new_vertices[1]
  
    # se poste não for existente colocar poste
    if tipo_poste == "EXISTENTE":

        ### Se poste existente e instalou vão frouxo, colocar estrutura de derivação existente       
            resultado = mosaico ( 115, distance_ptos (pto1 , pto2),  module_name)      
            if resultado is None:
                 def_estrutura, def_estruturabt, def_poste, def_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
            else:
                def_estrutura, def_estruturabt, def_poste, def_base = resultado[0], resultado[1], resultado[2], resultado[3]

    ## Se poste intercalado                    
    else:
        if loose_gap == "SIM":
            resultado = mosaico ( 105, distance_ptos (pto1 , pto2),  module_name)
            if resultado is None:
                def_estrutura, def_estruturabt, def_poste, def_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
            else:
                def_estrutura, def_estruturabt, def_poste, def_base = resultado[0], resultado[1], resultado[2], resultado[3]
        else:
            ## Se poste intercalado e não instalou vão frouxo, usar mesma regra de fim de linha
            resultado = mosaico ( 95, distance_ptos (pto1 , pto2),  module_name)
            if resultado is None:
                def_estrutura, def_estruturabt, def_poste, def_base = "ESTRUTURA_MT", "ESTRUTURA_BT", "PADRAO", "BASE_PADRAO"
            else:
                def_estrutura, def_estruturabt, def_poste, def_base = resultado[0], resultado[1], resultado[2], resultado[3]
    return def_estrutura, def_estruturabt, def_poste, def_base

##################################################################################################################################
def gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar):
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste", "estrutura_mt", "estrutura_bt", "poste", "base"])
    
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)
    new_vertices = dividir_tramo(new_vertices, section_size)
    new_vertices = intercalar_vertices(new_vertices, lista_nao_intercalar, gap_size)




    mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base = poste_derivacao (new_vertices, loose_gap, tipo_poste, module_name)
    pontos_matriz = gravar_pontos_matriz(new_vertices, 0, mtz_estruturamt, mtz_estruturabt, mtz_postes, mtz_base)

    # Adiciona os dados da matriz de pontos ao DataFrame
    for i, vertex in enumerate(new_vertices):
        dados_ponto = pontos_matriz.get(vertex, {})
        new_row = {
            "trecho": trecho,
            "sequencia": i,
            "lat": f"{vertex[0]:.9f}".replace(".", ","),
            "long": f"{vertex[1]:.9f}".replace(".", ","),
            "numero_poste": num_poste_inicial if i == 0 else "",
            "tipo_poste": tipo_poste if i == 0 else "",
            "estrutura_mt": dados_ponto.get("estrutura_mt", ""),
            "estrutura_bt": dados_ponto.get("estrutura_bt", ""),
            "poste": dados_ponto.get("poste", ""),
            "base": dados_ponto.get("base", "")
        }
        matriz.loc[len(matriz)] = new_row
    return matriz

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
            estrutura_mt = row['estrutura_mt']
            estrutura_bt = row['estrutura_bt']
            poste = row['poste']
            base = row['base']
            
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
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        
        print(f"Arquivo KML '{nome_arquivo}' gerado com sucesso.")
        print(f"Total de pontos exportados: {len(matriz)}")
        return True
        
    except Exception as e:
        print(f"Erro ao gerar arquivo KML: {e}")
        return False

##################################################################################################################################
def main():
    trecho = "T1"
    module_name = "MT7"
    module_data = ["MT10", 100, "SIM"]
    loose_gap = "SIM"
    section_size = 500
    gap_size = 120
    num_poste_inicial = "2255555"
    tipo_poste = "EXISTENTE"
    lista_nao_intercalar = [0, 3, 5] 

    vertices = [
        (-17.041935, -49.224541),
        (-17.045514, -49.217512),
        (-17.047802, -49.214406),
        (-17.047725, -49.213698),
        (-17.046803, -49.213231)
    ]                          
    matriz = gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar)

#, lista_nao_intercalar


    try:
        arquivo_csv = "matriz_resultado.csv"
        # Configura o pandas para usar vírgula como separador decimal
        pd.set_option('display.float_format', lambda x: f'{x:.8f}'.replace('.', ','))
        matriz.to_csv(arquivo_csv, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV '{arquivo_csv}' gerado com sucesso.")
    except PermissionError:
        # Se não conseguir salvar com o nome original, tenta com um nome diferente
        import time
        timestamp = int(time.time())
        arquivo_csv = f"matriz_resultado_{timestamp}.csv"
        matriz.to_csv(arquivo_csv, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"Arquivo CSV '{arquivo_csv}' gerado com sucesso (nome alternativo devido a erro de permissão).")
    except Exception as e:
        print(f"Erro ao salvar arquivo CSV: {e}")
        print("Dados da matriz:")
        print(matriz)
    
    # Exporta os pontos para KML
    print("\n=== Exportando para KML ===")
    exportar_para_kml(matriz, "pontos_matriz.kml")

if __name__ == "__main__":
    main()



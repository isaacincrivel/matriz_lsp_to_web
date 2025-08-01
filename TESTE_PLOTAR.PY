from math import radians, sin, cos, sqrt, atan2, degrees, asin
import pandas as pd
import math

def distance(lat1, lon1, lat2, lon2):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c



def angle(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    initial_bearing = atan2(x, y)
    initial_bearing = degrees(initial_bearing)
    return (initial_bearing + 360) % 360

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


def get_loose_gap(loose_gap, vertices):
    if loose_gap != "SIM":
        return vertices, "NÃO"
    first_point = vertices[0]
    second_point = vertices[1]
    distance_between = distance(first_point[0], first_point[1], second_point[0], second_point[1])
    if distance_between > 60:
        angle_between = angle(first_point[0], first_point[1], second_point[0], second_point[1])
        new_point = polar(first_point[0], first_point[1], 30, angle_between)
        return [first_point, new_point, second_point] + vertices[2:]
    return vertices, "SIM"


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

def gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste):
    matriz = pd.DataFrame(columns=["trecho", "sequencia", "lat", "long", "numero_poste", "tipo_poste"])
    #new_vertices = get_loose_gap(loose_gap, vertices)
    new_vertices, loose_gap = get_loose_gap(loose_gap, vertices)
    new_vertices = dividir_tramo(new_vertices, section_size)

    new_vertices = poste_derivacao (new_vertices, loose_gap, tipo_poste, module_name)




### COLOCAR DERIVAÇÃO

#### COLOCAR PONTOS INTERMEDIARIOS






    for i, vertex in enumerate(new_vertices):
        new_row = {
            "trecho": trecho,
            "sequencia": i,
            "lat": vertex[0],
            "long": vertex[1],
            "numero_poste": num_poste_inicial if i == 0 else "",
            "tipo_poste": tipo_poste if i == 0 else ""
        }
        matriz.loc[len(matriz)] = new_row
    return matriz

def main():
    trecho = "T1"
    module_name = "MT10"
    module_data = ["MT10", 100, "SIM"]
    loose_gap = "SIM"
    section_size = 500
    gap_size = 80
    num_poste_inicial = "2255555"
    tipo_poste = "EXISTENTE"
    vao_frouxo = "SIM"


    vertices = [
        (-17.041935, -49.224541),
        (-17.045514, -49.217512),
        (-17.047802, -49.214406),
        (-17.047725, -49.213698),
        (-17.046803, -49.213231)
    ]

    matriz = gerar_matriz(trecho, module_name, module_data, vertices, loose_gap, section_size, gap_size, num_poste_inicial, tipo_poste, vao_frouxo)

    
    arquivo_csv = "matriz_resultado.csv"
    matriz.to_csv(arquivo_csv, index=False, encoding='utf-8-sig', sep=';')
    print(f"Arquivo CSV '{arquivo_csv}' gerado com sucesso.")

if __name__ == "__main__":
    main()





def poste_derivacao( new_vertices, loose_gap, tipo_poste, module_name):   
    pto1 = new_vertices[0]
    pto2 = new_vertices[1]
  
    # se poste não for existente colocar poste
    if tipo_poste == "EXISTENTE":

        ### Se poste existente e instalou vão frouxo, colocar estrutura de derivação existente       
            def_poste, def_estrutura, def_base = mosaico ( 115, distance_ptos (pto1 , pto2),  module_name)      

    ## Se poste intercalado                    
    else:
        if loose_gap == "SIM":
            def_poste, def_estrutura, def_base = mosaico ( 105, distance_ptos (pto1 , pto2),  module_name)
        else:
            ## Se poste intercalado e não instalou vão frouxo, usar mesma regra de fim de linha
            def_poste, def_estrutura, def_base = mosaico ( 95, distance_ptos (pto1 , pto2),  module_name)
    return def_poste, def_estrutura, def_base




################################ FUNÇÃO NOVA
def distance_ptos (pto1 , pto2):

    distance_between = distance(pto1[0], pto1[1], pto2[0], pto2[1])
    
    return distance_between



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
        ["U3","", "PDT10/600", "BC", [(900.0, 220.0) (1000.0, 220.0) (1000.0, 1.39955e-12) (900.0, 9.09495e-13) (900.0, 220.0)] ] , #ms8
        ["U3","", "PDT10/1000", "BC", [((900.0, 220.0) (900.0, 500.0) (1000.0, 500.0) (1000.0, 220.0) (900.0, 220.0))]], #ms9
        ["U3","", "PDT11/300", "BS", [(1000.0, 35.0) (1100.0, 35.0) (1100.0, 9.09495e-13) (1000.0, 1.39266e-12) (1000.0, 35.0)]], #ms10
        ["U3","", "PDT11/1000", "BC", [(1000.0, 220.0) (1100.0, 220.0) (1100.0, 35.0) (1000.0, 35.0) (1000.0, 220.0)]], #ms11
        ["U3","", "EXIST", "BE", [(1100.0, 35.0) (1200.0, 35.0) (1200.0, 9.09495e-13) (1100.0, 1.39266e-12) (1100.0, 35.0)]], #ms12
        ["U3","", "EXIST", "ES", [(1100.0, 220.0) (1200.0, 220.0) (1200.0, 35.0) (1100.0, 35.0) (1100.0, 220.0)]] #ms13
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

def mosaico(ang1, dist1, str1):
    ang1 = ang1 * 10
    abaco = mtz_abaco(str1)
    ptx = (ang1, dist1)

    for entry in abaco:
        estru_mt_nv1, estru_mt_nv2, poste, base, polygon = entry
        if point_in_polygon(polygon, ptx):
            return [estru_mt_nv1, estru_mt_nv2, poste, base]

    ## se não der nada tem que retornar algo padrão
    return None

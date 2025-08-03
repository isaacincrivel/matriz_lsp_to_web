from math import radians, sin, cos, sqrt, atan2, degrees, asin

##################################################################################################################################
# FUNÇÕES DE CÁLCULO GEOGRÁFICO
##################################################################################################################################

def distance(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.
    
    Args:
        lat1, lon1: Coordenadas do primeiro ponto (latitude, longitude)
        lat2, lon2: Coordenadas do segundo ponto (latitude, longitude)
    
    Returns:
        float: Distância em metros
    """
    R = 6371000.0  # Raio da Terra em metros
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

##################################################################################################################################

def angle(lat1, lon1, lat2, lon2):
    """
    Calcula o ângulo (bearing) entre dois pontos geográficos.
    
    Args:
        lat1, lon1: Coordenadas do primeiro ponto (latitude, longitude)
        lat2, lon2: Coordenadas do segundo ponto (latitude, longitude)
    
    Returns:
        float: Ângulo em graus (0-360)
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    initial_bearing = atan2(x, y)
    initial_bearing = degrees(initial_bearing)
    return (initial_bearing + 360) % 360

##################################################################################################################################

def polar(lat, lon, distancia_metros, bearing_graus):
    """
    Calcula um novo ponto a partir de um ponto inicial, distância e ângulo.
    
    Args:
        lat, lon: Coordenadas do ponto inicial (latitude, longitude)
        distancia_metros: Distância em metros
        bearing_graus: Ângulo em graus
    
    Returns:
        tuple: (latitude, longitude) do novo ponto
    """
    R = 6371000  # Raio da Terra em metros
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

def distance_ptos(pto1, pto2):
    """
    Calcula a distância entre dois pontos representados como tuplas (lat, lon).
    
    Args:
        pto1: Primeiro ponto como (lat, lon)
        pto2: Segundo ponto como (lat, lon)
    
    Returns:
        float: Distância em metros
    """
    distance_between = distance(pto1[0], pto1[1], pto2[0], pto2[1])
    return distance_between 
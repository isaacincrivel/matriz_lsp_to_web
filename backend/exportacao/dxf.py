import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

"""
GERAÇÃO DE DXF A PARTIR DE KML
==============================

Gera um DXF R12 (AC1009) para máxima compatibilidade com CAD.
Entidades: POINT, POLYLINE+VERTEX, TEXT. Coordenadas em UTM (E/N).
"""


def _parse_coordinates_text(coord_text):
    coords = []
    for coord in coord_text.split():
        parts = coord.split(',')
        if len(parts) >= 2:
            try:
                lon = float(parts[0])
                lat = float(parts[1])
                coords.append((lon, lat))
            except ValueError:
                continue
    return coords


def _dxf_text(x, y, text, layer="TEXT"):
    """Texto em formato DXF R12 (sem subclass markers)."""
    safe_text = str(text).replace("\n", " ").strip()
    if not safe_text:
        return ""
    return (
        f"0\nTEXT\n8\n{layer}\n"
        f"10\n{x}\n20\n{y}\n30\n0\n"
        "40\n0.5\n"
        f"1\n{safe_text}\n"
    )

def _latlon_to_utm(lat, lon):
    # WGS84
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = f * (2 - f)
    e_prime_sq = e2 / (1 - e2)
    k0 = 0.9996

    # Zona UTM (não será exportada no DXF)
    zone = int((lon + 180) / 6) + 1
    lon0 = (zone - 1) * 6 - 180 + 3

    lat_rad = lat * 3.141592653589793 / 180.0
    lon_rad = lon * 3.141592653589793 / 180.0
    lon0_rad = lon0 * 3.141592653589793 / 180.0

    import math
    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)
    tan_lat = math.tan(lat_rad)

    N = a / (1 - e2 * sin_lat * sin_lat) ** 0.5
    T = tan_lat * tan_lat
    C = e_prime_sq * cos_lat * cos_lat
    A = cos_lat * (lon_rad - lon0_rad)

    M = a * (
        (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256) * lat_rad
        - (3 * e2 / 8 + 3 * e2 * e2 / 32 + 45 * e2 * e2 * e2 / 1024) * math.sin(2 * lat_rad)
        + (15 * e2 * e2 / 256 + 45 * e2 * e2 * e2 / 1024) * math.sin(4 * lat_rad)
        - (35 * e2 * e2 * e2 / 3072) * math.sin(6 * lat_rad)
    )

    easting = k0 * N * (
        A + (1 - T + C) * A**3 / 6 + (5 - 18 * T + T**2 + 72 * C - 58 * e_prime_sq) * A**5 / 120
    ) + 500000.0

    northing = k0 * (
        M + N * tan_lat * (
            A**2 / 2 + (5 - T + 9 * C + 4 * C**2) * A**4 / 24
            + (61 - 58 * T + T**2 + 600 * C - 330 * e_prime_sq) * A**6 / 720
        )
    )

    if lat < 0:
        northing += 10000000.0

    return easting, northing


def latlon_to_utm_with_zone(lat, lon):
    """
    Converte lat/lon (WGS84) para UTM.
    Returns:
        tuple: (zone, easting, northing)
    """
    zone = int((lon + 180) / 6) + 1
    e, n = _latlon_to_utm(lat, lon)
    return zone, e, n


def _to_utm_coords(coords):
    utm_coords = []
    for lon, lat in coords:
        e, n = _latlon_to_utm(lat, lon)
        utm_coords.append((e, n))
    return utm_coords


def criar_dxf_do_kml(kml_content, nome_arquivo="projeto.dxf"):
    """
    Cria um arquivo DXF simplificado a partir do conteúdo KML.

    Args:
        kml_content: string do arquivo KML
        nome_arquivo: nome do DXF a ser gerado

    Returns:
        tuple: (bool, caminho_arquivo, dxf_content)
    """
    try:
        from xml.etree import ElementTree as ET

        # Cria a pasta resultados
        pasta_resultados = "resultados"
        if not os.path.exists(pasta_resultados):
            os.makedirs(pasta_resultados)

        caminho_completo = os.path.join(pasta_resultados, nome_arquivo)

        # Parse do KML
        root = ET.fromstring(kml_content)


        # Remove namespaces
        for elem in root.iter():
            if "}" in elem.tag:
                elem.tag = elem.tag.split("}")[1]

        placemarks = root.findall(".//Placemark")

        # Mapeia labels de postes a partir de pontos com padrão "N | ..."
        poste_label_by_index = {}
        for placemark in placemarks:
            name_el = placemark.find("name")
            name = name_el.text.strip() if name_el is not None and name_el.text else ""
            if name:
                import re
                match = re.match(r"^\s*(\d+)\s*\|", name)
                if match:
                    poste_label_by_index[int(match.group(1))] = name

        def _label_for_polygon(name):
            if not name:
                return ""
            import re
            quad_match = re.match(r"^Quadrado\s+(\d+)", name, re.IGNORECASE)
            if quad_match:
                idx = int(quad_match.group(1))
                return poste_label_by_index.get(idx, "")
            base_match = re.match(r"^Base Concreto\s+(\d+)", name, re.IGNORECASE)
            if base_match:
                idx = int(base_match.group(1))
                return poste_label_by_index.get(idx, "")
            return ""

        dxf_entities = ""

        for placemark in placemarks:
            name_el = placemark.find("name")
            name = name_el.text.strip() if name_el is not None and name_el.text else ""

            point_el = placemark.find(".//Point/coordinates")
            if point_el is not None and point_el.text:
                coords = _parse_coordinates_text(point_el.text.strip())
                if coords:
                    utm = _to_utm_coords(coords)
                    x, y = utm[0]
                    if name and "|" in name:
                        dxf_entities += (
                            f"0\nPOINT\n8\nPOSTE\n"
                            f"10\n{x}\n20\n{y}\n30\n0\n"
                        )
                        dxf_entities += _dxf_text(x, y, name, layer="POSTE")

            line_el = placemark.find(".//LineString/coordinates")
            if line_el is not None and line_el.text:
                coords = _parse_coordinates_text(line_el.text.strip())
                if len(coords) >= 2:
                    utm = _to_utm_coords(coords)
                    # R12: POLYLINE + VERTEX + SEQEND (sem LWPOLYLINE)
                    dxf_entities += (
                        "0\nPOLYLINE\n8\nCABO\n"
                        "10\n0\n20\n0\n30\n0\n70\n0\n"
                    )
                    for x, y in utm:
                        dxf_entities += f"0\nVERTEX\n8\nCABO\n10\n{x}\n20\n{y}\n30\n0\n70\n0\n"
                    dxf_entities += "0\nSEQEND\n8\nCABO\n"
                    # Texto no ponto médio com distância total
                    import math
                    total = 0.0
                    for i in range(1, len(coords)):
                        lat1, lon1 = coords[i - 1][1], coords[i - 1][0]
                        lat2, lon2 = coords[i][1], coords[i][0]
                        dlat = math.radians(lat2 - lat1)
                        dlon = math.radians(lon2 - lon1)
                        a_val = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
                        c_val = 2 * math.atan2(math.sqrt(a_val), math.sqrt(1 - a_val))
                        total += 6371000 * c_val
                    dist_text = f"{total:.1f} m".replace(".", ",")
                    mid_index = len(utm) // 2
                    dxf_entities += _dxf_text(utm[mid_index][0], utm[mid_index][1], dist_text, layer="CABO")

            poly_el = placemark.find(".//Polygon/outerBoundaryIs/LinearRing/coordinates")
            if poly_el is not None and poly_el.text:
                coords = _parse_coordinates_text(poly_el.text.strip())
                if len(coords) >= 3:
                    utm = _to_utm_coords(coords)
                    layer = "POSTE"
                    if name.lower().startswith("base concreto"):
                        layer = "BASE"
                    # R12: POLYLINE fechada (70=1) + VERTEX + SEQEND
                    dxf_entities += (
                        f"0\nPOLYLINE\n8\n{layer}\n"
                        "10\n0\n20\n0\n30\n0\n70\n1\n"
                    )
                    for x, y in utm:
                        dxf_entities += f"0\nVERTEX\n8\n{layer}\n10\n{x}\n20\n{y}\n30\n0\n70\n0\n"
                    dxf_entities += f"0\nSEQEND\n8\n{layer}\n"
                    label = _label_for_polygon(name)
                    if label:
                        dxf_entities += _dxf_text(utm[0][0], utm[0][1], label, layer="POSTE")

        dxf_content = (
            "0\nSECTION\n2\nHEADER\n"
            "9\n$ACADVER\n1\nAC1009\n"
            "9\n$INSUNITS\n70\n6\n"
            "9\n$MEASUREMENT\n70\n1\n"
            "0\nENDSEC\n"
            "0\nSECTION\n2\nENTITIES\n"
            f"{dxf_entities}"
            "0\nENDSEC\n0\nEOF\n"
        )

        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(dxf_content)

        return True, caminho_completo, dxf_content
    except Exception as e:
        print(f"Erro ao gerar DXF: {e}")
        return False, "", ""

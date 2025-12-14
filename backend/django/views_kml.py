from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.exportacao.exportacao import exportar_para_kml
from lxml import etree

# Create your views here.

def tela(request):
    return render(request, "plot.html")

@csrf_exempt
def gerar_kml_e_geojson(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método não permitido. Use POST.")
    if 'matriz' not in request.FILES:
        return HttpResponseBadRequest("Arquivo 'matriz' não enviado.")

    matriz_file = request.FILES['matriz']

    # Leitura do arquivo
    if matriz_file.name.endswith(".csv"):
        matriz = pd.read_csv(matriz_file)
    elif matriz_file.name.endswith(".xlsx") or matriz_file.name.endswith(".xls"):
        matriz = pd.read_excel(matriz_file)
    else:
        return JsonResponse({"error": "Formato inválido"}, status=400)

    print(matriz)
    kml_content = exportar_para_kml(matriz)  # sua função retorna string KML
    if not kml_content:
        return JsonResponse({"error": "Não foi possível gerar a plotagem"}, status=400)

    # Parse KML com lxml
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    root = etree.fromstring(kml_content.encode("utf-8"))

    geojson_features = []

    for placemark in root.findall(".//kml:Placemark", namespaces=ns):
        geom = None
        # verifica LineString
        linestring = placemark.find(".//kml:LineString/kml:coordinates", namespaces=ns)
        if linestring is not None:
            coords = []
            for coord in linestring.text.strip().split():
                lon, lat, *_ = map(float, coord.split(","))
                coords.append([lon, lat])
            geom = {"type": "LineString", "coordinates": coords}

        # verifica Point
        point = placemark.find(".//kml:Point/kml:coordinates", namespaces=ns)
        if point is not None:
            lon, lat, *_ = map(float, point.text.strip().split(","))
            geom = {"type": "Point", "coordinates": [lon, lat]}

        # verifica Polygon
        polygon = placemark.find(".//kml:Polygon/kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", namespaces=ns)
        if polygon is not None:
            coords = []
            for coord in polygon.text.strip().split():
                lon, lat, *_ = map(float, coord.split(","))
                coords.append([lon, lat])
            geom = {"type": "Polygon", "coordinates": [coords]}

        if geom:
            geojson_features.append({
                "type": "Feature",
                "geometry": geom,
                "properties": {"name": placemark.findtext("kml:name", default="", namespaces=ns)}
            })

    geojson_data = {"type": "FeatureCollection", "features": geojson_features}

    return JsonResponse({
        "kml": kml_content,
        "geojson": geojson_data
    })
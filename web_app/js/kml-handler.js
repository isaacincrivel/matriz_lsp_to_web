// kml-handler.js - Manipulação de arquivos KML

class KMLHandler {
    constructor(mapController) {
        this.mapController = mapController;
    }

    // Importa KML do arquivo
    async importKML(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    const kmlText = e.target.result;
                    this.parseKML(kmlText);
                    resolve();
                } catch (error) {
                    reject(error);
                }
            };
            
            reader.onerror = () => reject(new Error('Erro ao ler arquivo'));
            reader.readAsText(file);
        });
    }

    // Faz parse do KML
    parseKML(kmlText) {
        const parser = new DOMParser();
        const kmlDoc = parser.parseFromString(kmlText, 'text/xml');
        
        // Verifica erros de parsing
        const parseError = kmlDoc.querySelector('parsererror');
        if (parseError) {
            throw new Error('Erro ao fazer parse do KML: ' + parseError.textContent);
        }

        // Limpa o mapa atual
        this.mapController.clearAll();
        if (window.appState) {
            window.appState.postes = [];
        }

        // Processa Placemarks (pontos e linhas)
        const placemarks = kmlDoc.querySelectorAll('Placemark');
        let sequence = 0;
        
        placemarks.forEach((placemark) => {
            const coords = this.extractCoordinates(placemark);
            
            if (coords.length === 0) {
                return; // Sem coordenadas, pula
            }

            // Se for um ponto (uma coordenada)
            if (coords.length === 1) {
                const [lon, lat] = coords[0];
                this.mapController.addMarker(lat, lon, sequence++);
            } 
            // Se for uma linha (múltiplas coordenadas)
            else {
                // Cria polilinha
                const latlngs = coords.map(([lon, lat]) => [lat, lon]);
                const polyline = L.polyline(latlngs, {
                    color: '#3388ff',
                    weight: 4
                }).addTo(this.mapController.map);

                this.mapController.polylines.push(polyline);
                this.mapController.drawLayer.addLayer(polyline);

                // Cria marcadores nos vértices
                latlngs.forEach(([lat, lon]) => {
                    this.mapController.addMarker(lat, lon, sequence++);
                });
            }
        });

        // Ajusta zoom para mostrar todos os elementos
        setTimeout(() => {
            this.mapController.fitBounds();
        }, 100);
    }

    // Extrai coordenadas de um Placemark
    extractCoordinates(placemark) {
        const coordinates = [];
        
        // Tenta encontrar coordenadas em Point
        const point = placemark.querySelector('Point coordinates');
        if (point) {
            const coords = this.parseCoordinateString(point.textContent);
            if (coords.length > 0) {
                coordinates.push(coords[0]);
            }
        }

        // Tenta encontrar coordenadas em LineString
        const lineString = placemark.querySelector('LineString coordinates');
        if (lineString) {
            const coords = this.parseCoordinateString(lineString.textContent);
            coordinates.push(...coords);
        }

        // Tenta encontrar coordenadas em Polygon
        const polygon = placemark.querySelector('Polygon outerBoundaryIs LinearRing coordinates');
        if (polygon) {
            const coords = this.parseCoordinateString(polygon.textContent);
            coordinates.push(...coords);
        }

        return coordinates;
    }

    // Faz parse de string de coordenadas do KML
    parseCoordinateString(coordString) {
        const coordinates = [];
        const lines = coordString.trim().split(/\s+/);
        
        lines.forEach(line => {
            const parts = line.split(',');
            if (parts.length >= 2) {
                const lon = parseFloat(parts[0]);
                const lat = parseFloat(parts[1]);
                if (!isNaN(lat) && !isNaN(lon)) {
                    coordinates.push([lon, lat]);
                }
            }
        });

        return coordinates;
    }

    // Exporta KML dos dados atuais
    exportKML() {
        if (!window.appState || window.appState.postes.length === 0) {
            throw new Error('Nenhum poste para exportar');
        }

        const postes = window.appState.postes;
        
        // Ordena por sequência
        const sortedPostes = [...postes].sort((a, b) => (a.sequencia || 0) - (b.sequencia || 0));
        
        // Cria estrutura KML
        let kml = `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Caminhamento de Rede</name>
        <description>Exportado em ${new Date().toLocaleString('pt-BR')}</description>
`;

        // Adiciona Placemarks para cada poste
        sortedPostes.forEach((poste) => {
            const lat = poste.lat;
            const lon = poste.lon;
            const seq = poste.sequencia;
            
            kml += `        <Placemark>
            <name>Poste ${seq}</name>
            <description>Sequência: ${seq}</description>
            <Point>
                <coordinates>${lon},${lat},0</coordinates>
            </Point>
        </Placemark>
`;
        });

        // Adiciona linha conectando os postes (se houver mais de um)
        if (sortedPostes.length > 1) {
            kml += `        <Placemark>
            <name>Linha de Rede</name>
            <LineString>
                <coordinates>
`;
            sortedPostes.forEach((poste) => {
                kml += `                    ${poste.lon},${poste.lat},0
`;
            });
            kml += `                </coordinates>
            </LineString>
        </Placemark>
`;
        }

        kml += `    </Document>
</kml>`;

        return kml;
    }

    // Faz download do KML
    downloadKML(filename = 'caminhamento_rede.kml') {
        try {
            const kmlContent = this.exportKML();
            const blob = new Blob([kmlContent], { type: 'application/vnd.google-earth.kml+xml' });
            saveAs(blob, filename);
            return true;
        } catch (error) {
            console.error('Erro ao exportar KML:', error);
            throw error;
        }
    }
}

// Exporta para uso global
window.KMLHandler = KMLHandler;


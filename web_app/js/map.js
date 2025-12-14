// map.js - Controle do mapa Leaflet

class MapController {
    constructor() {
        this.map = null;
        this.markers = [];
        this.polylines = [];
        this.drawControl = null;
        this.drawLayer = null;
        this.editMode = false;
        this.deleteMode = false;
        this.currentSequence = 0;
        this.isDrawing = false;
        
        this.init();
    }

    init() {
        // Inicializa o mapa
        this.map = L.map('line-map', {
            zoomControl: true,
            touchZoom: true,
            doubleClickZoom: true,
            scrollWheelZoom: true,
            boxZoom: true,
            keyboard: true,
            dragging: true
        });

        // Adiciona tiles do OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Tenta obter localização do usuário
        this.getUserLocation();

        // Inicializa camada de desenho
        this.initDrawLayer();

        // Event listeners
        this.map.on('click', (e) => this.onMapClick(e));
    }

    getUserLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    this.map.setView([lat, lon], 15);
                },
                (error) => {
                    // Se não conseguir, usa coordenadas padrão (Brasil)
                    this.map.setView([-15.7975, -47.8919], 5);
                }
            );
        } else {
            // Fallback para coordenadas padrão
            this.map.setView([-15.7975, -47.8919], 5);
        }
    }

    initDrawLayer() {
        // Camada para armazenar elementos desenhados
        this.drawLayer = new L.FeatureGroup();
        this.map.addLayer(this.drawLayer);

        // Configuração do controle de desenho
        const drawOptions = {
            position: 'topright',
            draw: {
                polyline: {
                    shapeOptions: {
                        color: '#3388ff',
                        weight: 4
                    }
                },
                polygon: false,
                rectangle: false,
                circle: false,
                marker: false,
                circlemarker: false
            },
            edit: {
                featureGroup: this.drawLayer,
                remove: false
            }
        };

        this.drawControl = new L.Control.Draw(drawOptions);
        this.map.addControl(this.drawControl);

        // Event listeners para desenho
        this.map.on(L.Draw.Event.CREATED, (e) => this.onDrawCreated(e));
        this.map.on(L.Draw.Event.EDITED, (e) => this.onDrawEdited(e));
        this.map.on(L.Draw.Event.DELETED, (e) => this.onDrawDeleted(e));
    }

    onMapClick(e) {
        // Se estiver em modo de adicionar poste, cria marcador
        if (window.appState && window.appState.addingPoste) {
            this.addMarker(e.latlng.lat, e.latlng.lng);
            window.appState.addingPoste = false;
        }
    }

    onDrawCreated(e) {
        const layer = e.layer;
        this.drawLayer.addLayer(layer);
        
        // Se for uma polilinha, cria marcadores nos vértices
        if (layer instanceof L.Polyline) {
            const latlngs = layer.getLatLngs();
            latlngs.forEach((latlng, index) => {
                this.addMarker(latlng.lat, latlng.lng);
            });
        }
        
        this.isDrawing = false;
    }

    onDrawEdited(e) {
        // Atualiza marcadores quando a linha é editada
        const layers = e.layers;
        layers.eachLayer((layer) => {
            if (layer instanceof L.Polyline) {
                this.updateMarkersFromPolyline(layer);
            }
        });
    }

    onDrawDeleted(e) {
        // Remove marcadores quando linha é deletada
        const layers = e.layers;
        layers.eachLayer((layer) => {
            if (layer instanceof L.Polyline && layer.vertexMarkers) {
                layer.vertexMarkers.forEach(marker => {
                    this.deletePoste(marker.sequence);
                });
            }
        });
    }

    addMarker(lat, lon, sequence = null) {
        if (sequence === null) {
            sequence = this.currentSequence++;
        }

        // Ícone personalizado para poste
        const posteIcon = L.divIcon({
            className: 'poste-marker',
            html: `<div class="marker-poste">
                <div class="marker-number">${sequence}</div>
                <div class="marker-pin"></div>
            </div>`,
            iconSize: [30, 40],
            iconAnchor: [15, 40],
            popupAnchor: [0, -40]
        });

        const marker = L.marker([lat, lon], {
            icon: posteIcon,
            draggable: true
        }).addTo(this.map);

        // Armazena dados do marcador
        marker.sequence = sequence;
        marker.data = {
            sequencia: sequence,
            lat: lat,
            lon: lon,
            status: {}
        };

        // Popup com informações básicas
        marker.bindPopup(`
            <div class="popup-poste">
                <strong>Poste #${sequence}</strong><br>
                <small>Lat: ${lat.toFixed(6)}</small><br>
                <small>Lon: ${lon.toFixed(6)}</small><br>
                <button class="btn-edit-poste" data-sequence="${sequence}">
                    Editar
                </button>
            </div>
        `);

        // Event listeners
        marker.on('click', () => {
            if (this.deleteMode) {
                if (confirm(`Deseja excluir o poste #${sequence}?`)) {
                    this.deletePoste(sequence);
                }
            } else if (this.editMode || !this.deleteMode) {
                // Abre formulário de edição
                if (window.formHandler) {
                    window.formHandler.openForm(marker.data, sequence);
                }
            }
        });

        marker.on('dragend', (e) => {
            const newLat = e.target.getLatLng().lat;
            const newLon = e.target.getLatLng().lng;
            marker.data.lat = newLat;
            marker.data.lon = newLon;
            // Atualiza no app state
            if (window.appState) {
                window.appState.updatePoste(sequence, {
                    lat: newLat,
                    lon: newLon
                });
            }
        });

        this.markers.push(marker);
        
        // Atualiza app state
        if (window.appState) {
            window.appState.addPoste(marker.data);
        }

        return marker;
    }

    updateMarkersFromPolyline(polyline) {
        const latlngs = polyline.getLatLngs();
        // Remove marcadores antigos desta linha
        // E cria novos baseados nos vértices
        latlngs.forEach((latlng) => {
            // Verifica se já existe marcador próximo
            const existingMarker = this.findMarkerNear(latlng.lat, latlng.lon, 0.0001);
            if (!existingMarker) {
                this.addMarker(latlng.lat, latlng.lon);
            }
        });
    }

    findMarkerNear(lat, lon, tolerance = 0.0001) {
        return this.markers.find(marker => {
            const markerLat = marker.getLatLng().lat;
            const markerLon = marker.getLatLng().lng;
            return Math.abs(markerLat - lat) < tolerance && 
                   Math.abs(markerLon - lon) < tolerance;
        });
    }

    getMarkerBySequence(sequence) {
        return this.markers.find(m => m.sequence === sequence);
    }

    deletePoste(sequence) {
        const marker = this.getMarkerBySequence(sequence);
        if (marker) {
            this.map.removeLayer(marker);
            this.markers = this.markers.filter(m => m !== marker);
            
            // Atualiza app state
            if (window.appState) {
                window.appState.removePoste(sequence);
            }
        }
    }

    editPoste(sequence) {
        const marker = this.getMarkerBySequence(sequence);
        if (marker && window.formHandler) {
            window.formHandler.openForm(marker.data, sequence);
        }
    }

    clearAll() {
        this.markers.forEach(marker => this.map.removeLayer(marker));
        this.markers = [];
        this.polylines.forEach(polyline => this.map.removeLayer(polyline));
        this.polylines = [];
        this.currentSequence = 0;
    }

    setEditMode(enabled) {
        this.editMode = enabled;
        this.map.getContainer().style.cursor = enabled ? 'pointer' : '';
    }

    setDeleteMode(enabled) {
        this.deleteMode = enabled;
        this.map.getContainer().style.cursor = enabled ? 'crosshair' : '';
    }

    startDrawing() {
        this.isDrawing = true;
        // Ativa o modo de desenho do Leaflet Draw
        if (this.drawControl) {
            // Simula clique no botão de desenho
            const drawButton = document.querySelector('.leaflet-draw-draw-polyline');
            if (drawButton) {
                drawButton.click();
            }
        }
    }

    fitBounds() {
        if (this.markers.length === 0) return;
        
        const group = new L.featureGroup(this.markers);
        this.map.fitBounds(group.getBounds().pad(0.1));
    }

    // Adiciona estilos CSS para os marcadores
    static addMarkerStyles() {
        if (document.getElementById('marker-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'marker-styles';
        style.textContent = `
            .poste-marker {
                background: transparent;
                border: none;
            }
            .marker-poste {
                position: relative;
                text-align: center;
            }
            .marker-number {
                background: #007bff;
                color: white;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.75rem;
                font-weight: bold;
                margin: 0 auto 2px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .marker-pin {
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 12px solid #007bff;
                margin: 0 auto;
            }
            .popup-poste {
                min-width: 150px;
            }
            .btn-edit-poste {
                margin-top: 0.5rem;
                padding: 0.25rem 0.75rem;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 0.25rem;
                cursor: pointer;
                font-size: 0.875rem;
            }
        `;
        document.head.appendChild(style);
    }
}

// Inicializa estilos quando o módulo carregar
MapController.addMarkerStyles();

// Exporta para uso global
window.MapController = MapController;


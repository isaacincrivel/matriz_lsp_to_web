// Sistema de Importação KML - Código Principal
// Versão preparada para desktop app

// Estado global para pontos manuais
let pontosManuais = [];
let map = null;
let mapInitialized = false;

// Estado do modo manual de criação de polilinha
let isManualModeActive = false;
let manualVertices = []; // Vértices criados manualmente [{lat, lon, number}, ...]
let tempPolyline = null; // Linha temporária do último ponto ao cursor
let manualPolyline = null; // Linha conectando os pontos manuais

// Estado da geolocalização
let userLocationMarker = null; // Marcador da localização do usuário
let userLocationAccuracyCircle = null; // Círculo de precisão da localização

// Aguarda o Leaflet estar carregado
function waitForLeaflet(callback, maxAttempts = 50) {
    let attempts = 0;
    function check() {
        attempts++;
        if (typeof L !== 'undefined') {
            console.log('Leaflet carregado!');
            callback();
        } else if (attempts < maxAttempts) {
            setTimeout(check, 100);
        } else {
            console.error('Leaflet não foi carregado após ' + maxAttempts + ' tentativas');
            if (typeof showMessage !== 'undefined' && typeof errorMessage !== 'undefined') {
                showMessage(errorMessage, 'Erro: Biblioteca Leaflet não foi carregada. Verifique os arquivos.', true);
            }
        }
    }
    check();
}

// Referências aos elementos
const fileInput = document.getElementById('fileInput');
const csvImportInput = document.getElementById('csvImportInput');
const btnImportarArquivo = document.getElementById('btnImportarArquivo');
const btnGerarMatriz = document.getElementById('btnGerarMatriz');
const btnPlotarProjeto = document.getElementById('btnPlotarProjeto');
const btnAbrirTabela = document.getElementById('btnAbrirTabela');
const btnInverterSentido = document.getElementById('btnInverterSentido');
const btnFinalizarPolilinha = document.getElementById('btnFinalizarPolilinha');
const fileName = document.getElementById('fileName');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');
const numeroModulo = document.getElementById('numeroModulo');
const descricaoModulo = document.getElementById('descricaoModulo');
const naoIntercalarPostes = document.getElementById('naoIntercalarPostes');

// Atualiza nome do arquivo quando selecionado e habilita/desabilita botões
fileInput.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        const fileNameStr = file.name.toLowerCase();
        
        fileName.textContent = `Arquivo selecionado: ${file.name}`;
        
        // Se o arquivo for KML/HTML, habilita botão Gerar Matriz e Plotar Projeto
        if (fileNameStr.endsWith('.kml') || fileNameStr.endsWith('.kmz') || fileNameStr.endsWith('.html')) {
            btnGerarMatriz.disabled = false;
            btnPlotarProjeto.disabled = false;
            
            // Mostra o container do mapa
            const mapContainer = document.getElementById('line-map-container');
            if (mapContainer) {
                mapContainer.style.display = 'block';
            }
            
            // Inicializa o mapa se ainda não foi inicializado e carrega o KML automaticamente
            if (mapInitialized && map) {
                // Mapa já está pronto, só carrega o KML
                setTimeout(function() {
                    if (fileNameStr.endsWith('.html')) {
                        loadGeoJSONOnMap(file);
                    } else {
                        loadKMLOnMap(file);
                    }
                }, 300);
            } else {
                // Aguarda o Leaflet carregar, inicializa o mapa e depois carrega o KML
                waitForLeaflet(function() {
                    setTimeout(function() {
                        if (!mapInitialized) {
                            initMap();
                        }
                        // Aguarda o mapa estar totalmente pronto antes de carregar o KML
                        setTimeout(function() {
                        if (map && mapInitialized) {
                            if (fileNameStr.endsWith('.html')) {
                                loadGeoJSONOnMap(file);
                            } else {
                                loadKMLOnMap(file);
                            }
                            } else {
                                // Se ainda não estiver pronto, tenta novamente
                                setTimeout(function() {
                                if (fileNameStr.endsWith('.html')) {
                                    loadGeoJSONOnMap(file);
                                } else {
                                    loadKMLOnMap(file);
                                }
                                }, 500);
                            }
                        }, 500);
                    }, 300);
                });
            }
        } else {
            // CSV/Excel no fileInput: usar Importar Matriz CSV para CSV; Plotar Projeto só para KML/HTML
            btnGerarMatriz.disabled = true;
            btnPlotarProjeto.disabled = !window.arquivoCSVImportado;
        }
    } else {
        fileName.textContent = '';
        btnGerarMatriz.disabled = true;
        btnPlotarProjeto.disabled = !window.arquivoCSVImportado;
        
        checkAndActivateManualMode();
    }
});

// Função para mostrar mensagens
function showMessage(element, message, isError = false) {
    element.textContent = message;
    element.style.display = 'block';
    if (isError) {
        element.className = 'error-message';
    } else {
        element.className = 'success-message';
    }
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Função para gerar KML a partir de dados
function gerarKML(dados, nomeArquivo = 'pontos_matriz.kml') {
    let kml = `<?xml version="1.0" encoding="UTF-8"?>
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
`;

    dados.forEach((ponto, index) => {
        const lat = ponto.lat || ponto.Lat || ponto.latitude || 0;
        const lon = ponto.long || ponto.Long || ponto.longitude || ponto.lon || 0;
        const sequencia = ponto.sequencia || ponto.Sequencia || index;
        const trecho = ponto.trecho || ponto.Trecho || '';
        const numero_poste = ponto.numero_poste || ponto.Numero_Poste || ponto.num_poste || '';
        const tipo_poste = ponto.tipo_poste || ponto.Tipo_Poste || '';

        // Converte string com vírgula para número
        const latNum = typeof lat === 'string' ? parseFloat(lat.replace(',', '.')) : parseFloat(lat);
        const lonNum = typeof lon === 'string' ? parseFloat(lon.replace(',', '.')) : parseFloat(lon);

        if (isNaN(latNum) || isNaN(lonNum)) {
            console.warn(`Linha ${index + 1}: Coordenadas inválidas`, ponto);
            return;
        }

        const styleId = numero_poste && numero_poste !== '' ? 'poste_style' : 'ponto_intermediario_style';
        const nomePonto = numero_poste && numero_poste !== '' ? `Poste ${numero_poste}` : `Ponto ${sequencia}`;

        const descricao = `
            <![CDATA[
            <h3>${nomePonto}</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><td><strong>Trecho:</strong></td><td>${trecho}</td></tr>
                <tr><td><strong>Sequência:</strong></td><td>${sequencia}</td></tr>
                <tr><td><strong>Latitude:</strong></td><td>${lat}</td></tr>
                <tr><td><strong>Longitude:</strong></td><td>${lon}</td></tr>
                <tr><td><strong>Número do Poste:</strong></td><td>${numero_poste || 'N/A'}</td></tr>
                <tr><td><strong>Tipo do Poste:</strong></td><td>${tipo_poste || 'N/A'}</td></tr>
            </table>
            ]]>
            `;

        kml += `
    <Placemark>
        <name>${nomePonto}</name>
        <description>${descricao}</description>
        <styleUrl>#${styleId}</styleUrl>
        <Point>
            <coordinates>${lonNum},${latNum},0</coordinates>
        </Point>
    </Placemark>
`;
    });

    kml += `
</Document>
</kml>`;

    return kml;
}

// Desabilitado por enquanto - implementação futura (manter função gerarProjetoHTML no código)
const GERAR_HTML_PROJETO = false;

/**
 * Gera HTML standalone do projeto para envio por WhatsApp/celular.
 * GeoJSON em script type="application/json" para evitar corrupção.
 * Leaflet e mapa carregam após DOM pronto.
 * @param {object} geojson - GeoJSON com features do projeto (Point, LineString, Polygon)
 * @param {string} trecho - Nome/identificador do projeto
 * @returns {string} HTML completo
 */
function gerarProjetoHTML(geojson, trecho) {
    const dataHora = new Date().toLocaleString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
    const geojsonStr = JSON.stringify(geojson).replace(/<\/(script)/gi, '<\\/$1');
    const trechoEsc = (trecho || 'Projeto').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto ${trechoEsc} - Sistema Matriz</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, sans-serif; background: #f5f5f5; min-height: 100vh; display: flex; flex-direction: column; }
        .carimbo { flex-shrink: 0; }
        .carimbo {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 16px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        .carimbo-logo { font-weight: 700; font-size: 1.1em; }
        .carimbo-projeto { font-size: 0.95em; opacity: 0.95; }
        .carimbo-data { font-size: 0.85em; opacity: 0.9; }
        #mapa { width: 100%; flex: 1; min-height: 300px; background: #e0e0e0; }
        .leaflet-container { font-family: inherit; }
        .gps-marker { background: transparent !important; border: none !important; }
        .btn-gps, .btn-whatsapp {
            background: rgba(255,255,255,0.3); color: white; border: 1px solid rgba(255,255,255,0.6);
            padding: 6px 12px; border-radius: 6px; font-size: 0.85em; cursor: pointer;
        }
        .btn-gps:active, .btn-whatsapp:active { background: rgba(255,255,255,0.5); }
        @media (min-width: 768px) { .btn-gps { display: none !important; } }
        .banner-file { display: none; background: #e65100; color: white; padding: 10px 16px; text-align: center; font-size: 0.9em; }
        .banner-file.ativa { display: block; }
    </style>
</head>
<body>
    <div class="banner-file" id="bannerFile">⚠️ GPS n\u00e3o funciona neste arquivo. Para localiza\u00e7\u00e3o no celular: pe\u00e7a o LINK (https://...) e abra no navegador. N\u00e3o envie o arquivo \u2014 envie o link pelo WhatsApp.</div>
    <div class="carimbo">
        <span class="carimbo-logo">[ Sistema Matriz ]</span>
        <span class="carimbo-projeto">Projeto: ${trechoEsc}</span>
        <span class="carimbo-data">${dataHora}</span>
        <button class="btn-gps" id="btnGps" title="Mostrar minha localiza\u00e7\u00e3o no mapa">\u270d Minha localiza\u00e7\u00e3o</button>
        <a class="btn-whatsapp" id="btnWhatsapp" href="#" title="Enviar link por WhatsApp" style="display:none;text-decoration:none;">\u2705 Enviar por WhatsApp</a>
    </div>
    <div id="mapa"></div>
    <script type="application/json" id="geojson-data">${geojsonStr}</script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <script>
(function(){
    var geojsonEl = document.getElementById('geojson-data');
    var geojson = geojsonEl ? JSON.parse(geojsonEl.textContent || '{"type":"FeatureCollection","features":[]}') : { type: 'FeatureCollection', features: [] };
    var features = geojson.features || [];
    if (typeof L === 'undefined') {
        document.getElementById('mapa').innerHTML = '<p style="padding:20px;color:#c00;">Leaflet não carregou. Verifique a conexão com a internet e abra novamente.</p>';
        return;
    }
    var map = L.map('mapa').setView([-15.79, -47.88], 13);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; Esri', maxZoom: 19
    }).addTo(map);
    var posteLabelByIndex = {};
    for (var i = 0; i < features.length; i++) {
        var f = features[i];
        if (f.geometry && f.geometry.type === 'Point' && f.properties && f.properties.name) {
            var m = f.properties.name.match(/^\\s*(\\d+)\\s*\\|/);
            if (m) posteLabelByIndex[parseInt(m[1], 10)] = f.properties.name;
        }
    }
    function getLabel(name) {
        if (!name) return '';
        var q = name.match(/^Quadrado\\s+(\\d+)/i);
        if (q) return posteLabelByIndex[parseInt(q[1], 10)] || name;
        var b = name.match(/^Base Concreto\\s+(\\d+)/i);
        if (b) return posteLabelByIndex[parseInt(b[1], 10)] || name;
        return name;
    }
    function haversine(a, b) {
        var R = 6371000, dLat = (b[0] - a[0]) * Math.PI / 180, dLon = (b[1] - a[1]) * Math.PI / 180;
        var lat1 = a[0] * Math.PI / 180, lat2 = b[0] * Math.PI / 180;
        var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
        return 2 * R * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
    }
    function lineLen(coords) {
        var t = 0;
        for (var i = 1; i < coords.length; i++) t += haversine(coords[i - 1], coords[i]);
        return t;
    }
    var group = L.featureGroup();
    for (var j = 0; j < features.length; j++) {
        var feat = features[j];
        if (!feat.geometry) continue;
        if (feat.geometry.type === 'Point') {
            var c = feat.geometry.coordinates;
            var lat = parseFloat(c[1]), lon = parseFloat(c[0]);
            if (isNaN(lat) || isNaN(lon)) continue;
            var icon = L.divIcon({ className: '', html: '', iconSize: [1, 1] });
            var popup = (feat.properties && feat.properties.description) || (feat.properties && feat.properties.name) || 'Poste';
            L.marker([lat, lon], { icon: icon }).bindPopup(popup).addTo(group);
        } else if (feat.geometry.type === 'LineString') {
            var coords = (feat.geometry.coordinates || []).map(function(x) { return [parseFloat(x[1]), parseFloat(x[0])]; });
            if (coords.length < 2) continue;
            var ll = coords.map(function(x) { return [x[0], x[1]]; });
            var total = lineLen(ll);
            L.polyline(coords, { color: '#3388ff', weight: 4, opacity: 0.9 })
                .bindPopup('Distância: ' + total.toFixed(1).replace('.', ',') + ' m').addTo(group);
        } else if (feat.geometry.type === 'Polygon') {
            var ring = (feat.geometry.coordinates[0] || []).map(function(x) { return [parseFloat(x[1]), parseFloat(x[0])]; });
            if (ring.length < 3) continue;
            var lbl = getLabel((feat.properties && feat.properties.name) || '');
            L.polygon(ring, { color: '#e63946', fillColor: '#e63946', weight: 2, fillOpacity: 0.35 })
                .bindPopup(lbl || 'Polígono').addTo(group);
        }
    }
    group.addTo(map);
    if (group.getBounds && group.getBounds().isValid && group.getBounds().isValid()) {
        map.fitBounds(group.getBounds().pad(0.15));
    }

    var userMarker = null;
    var userAccuracy = null;
    var watchId = null;
    var firstFix = true;
    function updateLocation(pos) {
        var lat = pos.coords.latitude;
        var lon = pos.coords.longitude;
        var acc = pos.coords.accuracy || 30;
        if (userMarker) {
            userMarker.setLatLng([lat, lon]);
            if (userAccuracy) { userAccuracy.setLatLng([lat, lon]); userAccuracy.setRadius(acc); }
        } else {
            var blueIcon = L.divIcon({
                className: 'gps-marker',
                html: '<div style="width:24px;height:24px;background:#2196F3;border:3px solid #fff;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,0.4);"></div>',
                iconSize: [24, 24],
                iconAnchor: [12, 12]
            });
            userMarker = L.marker([lat, lon], { icon: blueIcon }).addTo(map).bindPopup('Voc\u00ea est\u00e1 aqui');
            userAccuracy = L.circle([lat, lon], {
                radius: acc, fillColor: '#2196F3', fillOpacity: 0.15, color: '#2196F3', weight: 1
            }).addTo(map);
        }
        if (firstFix) {
            firstFix = false;
            map.setView([lat, lon], Math.max(map.getZoom(), 16));
        }
    }
    function errLocation(e) {}
    function startGps() {
        if (!navigator.geolocation) return;
        if (watchId !== null) return;
        watchId = navigator.geolocation.watchPosition(updateLocation, errLocation, { enableHighAccuracy: true, timeout: 20000, maximumAge: 0 });
    }
    function stopGps() {
        if (watchId !== null) { navigator.geolocation.clearWatch(watchId); watchId = null; }
        firstFix = true;
        if (userMarker) { map.removeLayer(userMarker); userMarker = null; }
        if (userAccuracy) { map.removeLayer(userAccuracy); userAccuracy = null; }
    }
    var btn = document.getElementById('btnGps');
    if (btn) {
        btn.onclick = function() {
            if (watchId !== null) { stopGps(); this.textContent = '\u270d Minha localiza\u00e7\u00e3o'; return; }
            if (location.protocol === 'file:') {
                alert('GPS n\u00e3o funciona ao abrir o arquivo. Pe\u00e7a o link (https://...) - ao abrir o link, o GPS funciona.');
                return;
            }
            firstFix = true;
            this.textContent = 'Parar GPS';
            startGps();
        };
    }
    var bannerFile = document.getElementById('bannerFile');
    if (bannerFile && location.protocol === 'file:') bannerFile.classList.add('ativa');
    var btnWa = document.getElementById('btnWhatsapp');
    if (btnWa && location.protocol === 'https:') {
        btnWa.style.display = 'inline-block';
        btnWa.href = 'https://wa.me/?text=' + encodeURIComponent(location.href);
        btnWa.target = '_blank';
    }
})();
    </script>
</body>
</html>`;
}

// Função para fazer download do KML
function downloadKML(kmlContent, filename) {
    const blob = new Blob([kmlContent], { type: 'application/vnd.google-earth.kml+xml' });
    if (typeof saveAs !== 'undefined') {
        saveAs(blob, filename);
    } else {
        // Fallback para ambientes sem FileSaver.js
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Importar Matriz CSV: ao clicar, abre seletor de arquivo
btnImportarArquivo.addEventListener('click', function() {
    if (csvImportInput) {
        csvImportInput.value = '';
        csvImportInput.click();
    }
});

// Processa CSV selecionado: apenas armazena, não desenha. Desenho ocorre ao clicar em Plotar Projeto.
if (csvImportInput) {
    csvImportInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showMessage(errorMessage, 'Selecione um arquivo CSV.', true);
            return;
        }
        const reader = new FileReader();
        reader.onload = function(ev) {
            const csvContent = (ev.target.result || '').replace(/^\uFEFF/, '');
            window.arquivoCSVImportado = {
                content: csvContent,
                filename: file.name
            };
            if (fileName) fileName.textContent = 'CSV importado: ' + file.name + ' - Clique em Plotar Projeto';
            showMessage(successMessage, 'CSV importado. Clique em Plotar Projeto para desenhar e baixar os arquivos.');
            if (btnPlotarProjeto) btnPlotarProjeto.disabled = false;
            if (csvImportInput) csvImportInput.value = '';
        };
        reader.onerror = function() {
            showMessage(errorMessage, 'Erro ao ler o arquivo CSV.', true);
            if (csvImportInput) csvImportInput.value = '';
        };
        reader.readAsText(file, 'UTF-8');
    });
}

// Extrai vértices do CSV matriz (suporta formato resultado e formato transformado)
function extrairVerticesDoCSV(dados) {
    const vertices = [];
    const seenSeq = new Map();
    const first = dados[0];
    if (!first) return vertices;
    const keys = Object.keys(first);
    const trimKey = k => String(k).replace(/^\uFEFF/, '').trim();
    const latCol = keys.find(k => /^lat$/i.test(trimKey(k)) || /latitude/i.test(trimKey(k)));
    const lonCol = keys.find(k => /^long$/i.test(trimKey(k)) || /^lon$/i.test(trimKey(k)) || /longitude/i.test(trimKey(k)));
    const seqCol = keys.find(k => /sequencia|seq/i.test(trimKey(k)));
    const modCol = keys.find(k => /modalidade/i.test(trimKey(k)));
    const statusCol = keys.find(k => /^status$/i.test(trimKey(k)));
    if (!latCol || !lonCol) return vertices;
    for (let i = 0; i < dados.length; i++) {
        const row = dados[i];
        let latVal = row[latCol];
        let lonVal = row[lonCol];
        if (latVal === undefined || latVal === null || (String(latVal).trim() === '') || lonVal === undefined || lonVal === null || (String(lonVal).trim() === '')) continue;
        const statusVal = statusCol ? String(row[statusCol] || '').toLowerCase().trim() : '';
        if (modCol && row[modCol] && String(row[modCol]).toLowerCase().trim() !== 'implantar') continue;
        if (statusCol && statusVal && statusVal !== 'implantar') continue;
        const lat = parseFloat(String(latVal).trim().replace(',', '.'));
        const lon = parseFloat(String(lonVal).trim().replace(',', '.'));
        if (isNaN(lat) || isNaN(lon)) continue;
        let seq = i + 1;
        if (seqCol && row[seqCol] !== undefined && row[seqCol] !== '') {
            const parsed = parseInt(String(row[seqCol]).trim(), 10);
            if (!isNaN(parsed)) seq = parsed;
        }
        if (seenSeq.has(seq)) continue;
        seenSeq.set(seq, true);
        vertices.push({ lat, lon, number: seq, sequencia: seq });
    }
    vertices.sort((a, b) => a.sequencia - b.sequencia);
    return vertices;
}

// Plota vértices extraídos do CSV no mapa
function plotarVerticesCSVNoMapa(vertices) {
    if (!map || !mapInitialized) return;
    resetMapState();
    const allVertices = vertices.map(v => ({ lat: v.lat, lon: v.lon, number: v.number || v.sequencia }));
    allVertices.forEach(v => {
        const m = createNumberedMarker(v.lat, v.lon, v.number);
        window.currentMarkers.push(m);
    });
    createSegmentPolylines(allVertices);
    window.kmlVertices = vertices.map(v => ({ lat: v.lat, lon: v.lon, number: v.number, sequencia: v.number }));
    if (allVertices.length >= 2) {
        const latlngs = allVertices.map(v => [v.lat, v.lon]);
        const poly = L.polyline(latlngs, { color: '#3388ff', weight: 4, opacity: 0.8 }).addTo(map);
        window.currentPolylines.push(poly);
    }
    populateNaoIntercalarPostes(allVertices);
    btnInverterSentido.disabled = false;
    if (btnAbrirTabela) btnAbrirTabela.disabled = false;
    if (btnGerarMatriz) btnGerarMatriz.disabled = false;
    const bounds = allVertices.map(v => [v.lat, v.lon]);
    if (bounds.length > 0) map.fitBounds(bounds, { padding: [50, 50] });
}


// Cria e adiciona controle de localização ao mapa
function addLocationControl() {
    if (!map || typeof L === 'undefined') return;
    
    // Cria controle customizado de localização
    const LocationControl = L.Control.extend({
        onAdd: function(map) {
            // Cria container principal (barra de controles)
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            
            // Cria o botão dentro da barra
            const button = L.DomUtil.create('a', 'leaflet-control-locate', container);
            button.href = '#';
            button.title = 'Mostrar minha localização';
            button.innerHTML = '📍';
            button.style.cssText = 'font-size: 18px; line-height: 30px; text-align: center; display: block; width: 30px; height: 30px; text-decoration: none; color: #333;';
            
            // Efeito hover
            button.onmouseover = function() {
                this.style.backgroundColor = '#f4f4f4';
            };
            button.onmouseout = function() {
                this.style.backgroundColor = '';
            };
            
            // Previne o evento de arrastar o mapa quando clicar no controle
            L.DomEvent.disableClickPropagation(button);
            L.DomEvent.on(button, 'click', function(e) {
                L.DomEvent.stopPropagation(e);
                L.DomEvent.preventDefault(e);
                getCurrentLocation();
            });
            
            return container;
        },
        
        onRemove: function(map) {
            // Limpeza se necessário
        }
    });
    
    // Adiciona o controle ao mapa (canto superior esquerdo, abaixo dos controles de zoom)
    const locationControl = new LocationControl({
        position: 'topleft'
    });
    
    locationControl.addTo(map);
    console.log('Controle de localização adicionado ao mapa');
}

// Função para obter localização atual e centralizar mapa
function getCurrentLocation() {
    if (!navigator.geolocation) {
        showMessage(errorMessage, 'Geolocalização não é suportada pelo seu navegador.', true);
        return;
    }
    
    if (!map || !mapInitialized) {
        showMessage(errorMessage, 'Aguarde o mapa carregar completamente.', true);
        return;
    }
    
    // Opções para geolocalização (GPS de alta precisão)
    const options = {
        enableHighAccuracy: true, // Usa GPS quando disponível (melhor para celular)
        timeout: 15000, // Timeout de 15 segundos
        maximumAge: 0 // Não usa cache
    };
    
    // Obtém a localização atual
    navigator.geolocation.getCurrentPosition(
        // Sucesso
        function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const accuracy = position.coords.accuracy;
            
            console.log('Localização obtida:', lat, lon, 'Precisão:', accuracy, 'm');
            
            // Remove marcador e círculo anteriores se existirem
            if (userLocationMarker) {
                map.removeLayer(userLocationMarker);
                userLocationMarker = null;
            }
            if (userLocationAccuracyCircle) {
                map.removeLayer(userLocationAccuracyCircle);
                userLocationAccuracyCircle = null;
            }
            
            // Cria ícone customizado para a localização do usuário
            const userIcon = L.divIcon({
                className: 'user-location-marker',
                html: '<div style="background-color: #28a745; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>',
                iconSize: [16, 16],
                iconAnchor: [8, 8]
            });
            
            // Cria círculo de precisão
            userLocationAccuracyCircle = L.circle([lat, lon], {
                radius: accuracy,
                fillColor: '#28a745',
                fillOpacity: 0.2,
                color: '#28a745',
                weight: 1,
                opacity: 0.5
            }).addTo(map);
            
            // Adiciona marcador no mapa
            userLocationMarker = L.marker([lat, lon], { icon: userIcon })
                .addTo(map)
                .bindPopup(`<b>Sua Localização</b><br>Precisão: ${Math.round(accuracy)}m`)
                .openPopup();
            
            // Centraliza e faz zoom no mapa na posição do usuário
            // Calcula zoom baseado na precisão
            let zoomLevel = 16;
            if (accuracy > 100) zoomLevel = 14;
            else if (accuracy > 50) zoomLevel = 15;
            else if (accuracy > 20) zoomLevel = 16;
            else zoomLevel = 17;
            
            map.setView([lat, lon], zoomLevel, {
                animate: true,
                duration: 1.0
            });
            
            // Limpa o círculo de precisão após alguns segundos (opcional)
            setTimeout(function() {
                if (userLocationAccuracyCircle) {
                    map.removeLayer(userLocationAccuracyCircle);
                    userLocationAccuracyCircle = null;
                }
            }, 5000);
        },
        // Erro
        function(error) {
            let errorMessageText = 'Erro ao obter localização: ';
            
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessageText = 'Permissão negada. Por favor, permita o acesso à localização nas configurações do navegador.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessageText = 'Localização não disponível. Verifique se o GPS está ativado.';
                    break;
                case error.TIMEOUT:
                    errorMessageText = 'Tempo limite excedido. Tente novamente.';
                    break;
                default:
                    errorMessageText = 'Erro desconhecido ao obter localização.';
                    break;
            }
            
            console.error('Erro ao obter localização:', error);
            showMessage(errorMessage, errorMessageText, true);
        },
        options
    );
}

// Inicializa o mapa Leaflet
function initMap() {
    if (mapInitialized) return;
    
    const mapElement = document.getElementById('line-map');
    if (!mapElement) {
        console.error('Elemento do mapa não encontrado');
        return;
    }
    
    if (typeof L === 'undefined') {
        console.error('Leaflet não está carregado');
        return;
    }
    
    try {
        // Inicializa o mapa
        map = L.map('line-map', {
            zoomControl: true,
            touchZoom: true,
            doubleClickZoom: true,
            scrollWheelZoom: true,
            boxZoom: true,
            keyboard: true,
            dragging: true
        });

        // Adiciona tiles do Esri World Imagery (satélite) - como na imagem
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri',
            maxZoom: 19
        }).addTo(map);

        // Define uma localização padrão (Brasil - centro)
        map.setView([-15.7942, -47.8822], 13);

        // Adiciona controle de localização customizado
        addLocationControl();

        mapInitialized = true;
        console.log('Mapa inicializado com sucesso');
        
        // Configura eventos para modo manual de criação de polilinha
        setupManualModeEvents();
        
        // Ativa modo manual inicialmente (se não houver KML carregado)
        checkAndActivateManualMode();
    } catch (error) {
        console.error('Erro ao inicializar o mapa:', error);
        showMessage(errorMessage, 'Erro ao inicializar o mapa: ' + error.message, true);
    }
}

// Função para verificar e ativar modo manual (se não houver KML)
function checkAndActivateManualMode() {
    // Se não há vértices KML carregados, ativa modo manual
    if (!window.kmlVertices || window.kmlVertices.length === 0) {
        activateManualMode();
    } else {
        deactivateManualMode();
    }
}

// Função para ativar modo manual
function activateManualMode() {
    if (isManualModeActive) return;
    
    isManualModeActive = true;
    manualVertices = [];
    
    console.log('Modo manual ativado - Clique no mapa para adicionar pontos');
    
    // Desabilita doubleClickZoom para permitir duplo clique finalizar
    if (map) {
        map.doubleClickZoom.disable();
        // Muda cursor para crosshair (mira) durante modo manual
        map.getContainer().style.cursor = 'crosshair';
    }
    
    // Limpa qualquer polilinha temporária anterior
    clearTempPolyline();
    
    // Habilita o botão Finalizar (mas esconde até ter pelo menos 2 pontos)
    if (btnFinalizarPolilinha) {
        btnFinalizarPolilinha.style.display = 'none';
    }
}

// Função para desativar modo manual
function deactivateManualMode() {
    if (!isManualModeActive) return;
    
    isManualModeActive = false;
    
    console.log('Modo manual desativado');
    
    // Reabilita doubleClickZoom
    if (map) {
        map.doubleClickZoom.enable();
        // Volta cursor para o padrão do Leaflet (grab)
        map.getContainer().style.cursor = '';
    }
    
    // Remove linha temporária
    clearTempPolyline();
    
    // Remove linha manual se existir
    if (manualPolyline) {
        try {
            map.removeLayer(manualPolyline);
        } catch(e) {}
        manualPolyline = null;
    }
    
    // Esconde botão Finalizar
    if (btnFinalizarPolilinha) {
        btnFinalizarPolilinha.style.display = 'none';
    }
}

// Função para limpar linha temporária
function clearTempPolyline() {
    if (tempPolyline) {
        try {
            map.removeLayer(tempPolyline);
        } catch(e) {}
        tempPolyline = null;
    }
}

// Configura eventos do mapa para modo manual
function setupManualModeEvents() {
    if (!map) return;
    
    // Event listener para clique simples (adiciona ponto)
    map.on('click', function(e) {
        if (!isManualModeActive) return;
        
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;
        const number = manualVertices.length + 1;
        
        // Adiciona vértice
        manualVertices.push({ lat, lon, number, sequencia: number });
        
        console.log(`Ponto ${number} adicionado:`, { lat, lon });
        
        // Cria marcador
        const marker = createNumberedMarker(lat, lon, number);
        if (!window.currentMarkers) {
            window.currentMarkers = [];
        }
        window.currentMarkers.push(marker);
        
        // Atualiza polilinha manual
        updateManualPolyline();
        
        // Mostra botão Finalizar se tiver pelo menos 2 pontos
        if (btnFinalizarPolilinha && manualVertices.length >= 2) {
            btnFinalizarPolilinha.style.display = 'block';
        }
        
        // Remove linha temporária (será recriada no mousemove)
        clearTempPolyline();
    });
    
    // Event listener para duplo clique (finaliza polilinha) - funciona melhor no desktop
    // No mobile, use o botão "Finalizar Polilinha" que é mais confiável
    map.on('dblclick', function(e) {
        if (!isManualModeActive || manualVertices.length < 2) return;
        
        // Só previne default se não for touch (mobile)
        if (!e.originalEvent.touches) {
            e.originalEvent.preventDefault();
            e.originalEvent.stopPropagation();
        }
        
        finalizeManualPolyline();
    });
    
    // Event listener para movimento do mouse (desktop) - mostra linha temporária
    map.on('mousemove', function(e) {
        if (!isManualModeActive || manualVertices.length === 0) {
            clearTempPolyline();
            return;
        }
        
        // Remove linha temporária anterior
        clearTempPolyline();
        
        // Pega último vértice
        const lastVertex = manualVertices[manualVertices.length - 1];
        const mouseLat = e.latlng.lat;
        const mouseLon = e.latlng.lng;
        
        // Cria linha temporária do último ponto ao cursor (apenas desktop)
        tempPolyline = L.polyline(
            [[lastVertex.lat, lastVertex.lon], [mouseLat, mouseLon]],
            {
                color: '#3388ff',
                weight: 3,
                opacity: 0.5,
                dashArray: '5, 10'
            }
        ).addTo(map);
    });
    
    // Nota: No mobile, a linha temporária não será exibida (mousemove não funciona em touch)
    // Isso é aceitável - o importante é que o toque adiciona pontos e o botão "Finalizar" funciona
}

// Função para atualizar polilinha manual (conecta todos os pontos)
function updateManualPolyline() {
    if (manualVertices.length < 2) return;
    
    // Remove polilinha anterior se existir
    if (manualPolyline) {
        try {
            map.removeLayer(manualPolyline);
        } catch(e) {}
    }
    
    // Cria nova polilinha conectando todos os pontos
    const latlngs = manualVertices.map(v => [v.lat, v.lon]);
    manualPolyline = L.polyline(latlngs, {
        color: '#3388ff',
        weight: 3,
        opacity: 0.7
    }).addTo(map);
}

// Função para finalizar polilinha manual
function finalizeManualPolyline() {
    if (!isManualModeActive || manualVertices.length < 2) {
        showMessage(errorMessage, 'Adicione pelo menos 2 pontos antes de finalizar.', true);
        return;
    }
    
    console.log('Finalizando polilinha manual com', manualVertices.length, 'vértices');
    
    // Remove linha temporária
    clearTempPolyline();
    
    // Desativa modo manual (isso também reabilita doubleClickZoom)
    deactivateManualMode();
    
    // Salva vértices no formato esperado (igual ao KML)
    window.kmlVertices = manualVertices.map(v => ({
        lat: v.lat,
        lon: v.lon,
        number: v.number,
        sequencia: v.number
    }));
    
    // Cria segmentos para destacamento
    const allVertices = manualVertices.map(v => ({
        number: v.number,
        lat: v.lat,
        lon: v.lon
    }));
    
    // Remove a polilinha manual temporária (se existir)
    if (manualPolyline) {
        try {
            map.removeLayer(manualPolyline);
        } catch(e) {}
        manualPolyline = null;
    }
    
    // Cria a linha azul principal (igual ao KML) - conecta todos os pontos
    if (!window.currentPolylines) {
        window.currentPolylines = [];
    }
    
    const latlngs = manualVertices.map(v => [v.lat, v.lon]);
    const mainPolyline = L.polyline(latlngs, {
        color: '#3388ff',
        weight: 4,
        opacity: 0.8
    }).addTo(map);
    
    window.currentPolylines.push(mainPolyline);
    
    createSegmentPolylines(allVertices);
    
    // Popula select "Não Intercalar Postes"
    populateNaoIntercalarPostes(allVertices);
    
    // Habilita botões
    if (btnInverterSentido) {
        btnInverterSentido.disabled = false;
    }
    if (btnAbrirTabela) {
        btnAbrirTabela.disabled = false;
    }
    if (btnGerarMatriz) {
        btnGerarMatriz.disabled = false;
    }
    
    // Esconde botão Finalizar
    if (btnFinalizarPolilinha) {
        btnFinalizarPolilinha.style.display = 'none';
    }
    
    showMessage(successMessage, `✅ Polilinha finalizada com ${manualVertices.length} vértices!`);
}

// Inicializa o mapa quando a página carregar e Leaflet estiver pronto
// Função para buscar módulo na tabela-data.js
function buscarModuloPorCodigo(codigo) {
    if (!codigo || codigo.trim() === '') {
        return null;
    }
    
    // Verifica se dadosTabela está disponível
    if (typeof dadosTabela === 'undefined' || !dadosTabela || dadosTabela.length === 0) {
        console.warn('dadosTabela não está disponível');
        return null;
    }
    
    // Busca o módulo pelo código
    const modulo = dadosTabela.find(item => {
        const codigoItem = item.codigo_modulo ? String(item.codigo_modulo).trim() : '';
        const codigoBuscado = String(codigo).trim();
        return codigoItem === codigoBuscado;
    });
    
    return modulo || null;
}

// Função para atualizar descrição do módulo
function atualizarDescricaoModulo(codigo) {
    if (!descricaoModulo) return;
    
    if (!codigo || codigo.trim() === '') {
        descricaoModulo.textContent = '<- Digitar código do módulo';
        descricaoModulo.style.color = '#666';
        return;
    }
    
    const modulo = buscarModuloPorCodigo(codigo);
    if (modulo) {
        const descricao = modulo.descrição_modulo || modulo['descrição_modulo'] || '';
        descricaoModulo.textContent = descricao || 'Descrição não encontrada';
        descricaoModulo.style.color = '#333';
    } else {
        descricaoModulo.textContent = 'Módulo não encontrado';
        descricaoModulo.style.color = '#f44336';
    }
}

// Validação para campo numérico - só permite números e busca descrição
function setupNumeroModuloValidation() {
    if (numeroModulo) {
        // Permite apenas números ao digitar
        numeroModulo.addEventListener('keypress', function(e) {
            // Permite: números (48-57), backspace (8), delete (46), tab (9), setas (37-40)
            if (!(e.key >= '0' && e.key <= '9') && 
                e.key !== 'Backspace' && 
                e.key !== 'Delete' && 
                e.key !== 'Tab' && 
                !['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
                e.preventDefault();
            }
        });
        
        // Valida ao colar - remove caracteres não numéricos
        numeroModulo.addEventListener('paste', function(e) {
            e.preventDefault();
            const paste = (e.clipboardData || window.clipboardData).getData('text');
            const numbersOnly = paste.replace(/\D/g, ''); // Remove tudo que não é dígito
            this.value = numbersOnly;
            // Busca a descrição após colar
            atualizarDescricaoModulo(numbersOnly);
        });
        
        // Valida ao digitar - remove caracteres não numéricos e busca descrição
        numeroModulo.addEventListener('input', function(e) {
            this.value = this.value.replace(/\D/g, '');
            // Busca a descrição quando o usuário digita
            atualizarDescricaoModulo(this.value);
        });
        
        // Também busca quando o campo perde o foco (blur)
        numeroModulo.addEventListener('blur', function(e) {
            atualizarDescricaoModulo(this.value);
        });
    }
}

// Função para escutar mudanças no localStorage quando um módulo é selecionado na tabela
function setupModuloSelecionadoListener() {
    // Escuta mudanças no localStorage
    window.addEventListener('storage', function(e) {
        if (e.key === 'modulo_selecionado') {
            try {
                const moduloData = JSON.parse(e.newValue);
                if (moduloData && numeroModulo && descricaoModulo) {
                    numeroModulo.value = moduloData.codigo_modulo || '';
                    atualizarDescricaoModulo(moduloData.codigo_modulo);
                }
            } catch (error) {
                console.error('Erro ao processar módulo selecionado:', error);
            }
        }
    });
    
    // Também verifica periodicamente para quando a mesma janela atualiza o localStorage
    // (o evento 'storage' só dispara entre janelas diferentes)
    let lastTimestamp = null;
    setInterval(function() {
        try {
            const moduloSelecionado = localStorage.getItem('modulo_selecionado');
            if (moduloSelecionado) {
                const moduloData = JSON.parse(moduloSelecionado);
                if (moduloData && moduloData.timestamp && moduloData.timestamp !== lastTimestamp) {
                    lastTimestamp = moduloData.timestamp;
                    if (numeroModulo && descricaoModulo) {
                        numeroModulo.value = moduloData.codigo_modulo || '';
                        atualizarDescricaoModulo(moduloData.codigo_modulo);
                    }
                }
            }
        } catch (error) {
            // Ignora erros silenciosamente
        }
    }, 500); // Verifica a cada 500ms
}

window.addEventListener('load', function() {
    console.log('Página carregada');
    
    // Configura validação do campo número do módulo e busca de descrição
    setupNumeroModuloValidation();
    
    // Configura listener para módulo selecionado na tabela
    setupModuloSelecionadoListener();
    
    // Configura listener para destacar segmentos quando seleção muda
    if (naoIntercalarPostes) {
        naoIntercalarPostes.addEventListener('change', function(e) {
            highlightSelectedSegments();
        });
    }
    
    // Mapa será inicializado apenas quando um KML for importado
    // Não inicializa automaticamente aqui
});

// Função para carregar KML no mapa
function loadKMLOnMap(kmlFile) {
    if (!map || !mapInitialized) {
        showMessage(errorMessage, 'Mapa não inicializado. Aguarde um momento e tente novamente.', true);
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const kmlText = e.target.result;
            parseAndDisplayKML(kmlText);
        } catch (error) {
            showMessage(errorMessage, 'Erro ao ler arquivo KML: ' + error.message, true);
        }
    };
    reader.onerror = function() {
        showMessage(errorMessage, 'Erro ao ler o arquivo.', true);
    };
    reader.readAsText(kmlFile);
}

// Função para extrair GeoJSON inline de um HTML
function extractGeoJSONFromHtml(htmlText) {
    const match = htmlText.match(/const\s+geojson\s*=\s*(\{[\s\S]*?\});/);
    if (!match || !match[1]) {
        throw new Error('GeoJSON inline não encontrado no HTML.');
    }
    return JSON.parse(match[1]);
}

// Função para carregar HTML com GeoJSON inline no mapa
function loadGeoJSONOnMap(htmlFile) {
    if (!map || !mapInitialized) {
        showMessage(errorMessage, 'Mapa não inicializado. Aguarde um momento e tente novamente.', true);
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const htmlText = e.target.result;
            const geojson = extractGeoJSONFromHtml(htmlText);
            parseAndDisplayGeoJSON(geojson);
        } catch (error) {
            showMessage(errorMessage, 'Erro ao ler GeoJSON do HTML: ' + error.message, true);
        }
    };
    reader.onerror = function() {
        showMessage(errorMessage, 'Erro ao ler o arquivo HTML.', true);
    };
    reader.readAsText(htmlFile);
}

// Converte KML em GeoJSON simples (Point, LineString, Polygon) - suporta namespace KML
function buildGeoJsonFromKml(kmlText) {
    const parser = new DOMParser();
    const kmlDoc = parser.parseFromString(kmlText, 'text/xml');
    const parseError = kmlDoc.querySelector('parsererror');
    if (parseError) {
        throw new Error('Erro ao fazer parse do KML');
    }

    const KML_NS = 'http://www.opengis.net/kml/2.2';
    const features = [];
    const placemarks = kmlDoc.getElementsByTagNameNS
        ? kmlDoc.getElementsByTagNameNS(KML_NS, 'Placemark')
        : kmlDoc.getElementsByTagName('Placemark');

    function findCoords(parent, geomTag, innerTag) {
        const geom = parent.getElementsByTagNameNS ? parent.getElementsByTagNameNS(KML_NS, geomTag)[0] : parent.querySelector(geomTag);
        if (!geom) return null;
        const coordEl = geom.getElementsByTagNameNS ? geom.getElementsByTagNameNS(KML_NS, 'coordinates')[0] : geom.querySelector('coordinates');
        return coordEl && coordEl.textContent ? coordEl.textContent.trim() : null;
    }

    function getDesc(placemark) {
        const descEl = placemark.getElementsByTagNameNS ? placemark.getElementsByTagNameNS(KML_NS, 'description')[0] : placemark.querySelector('description');
        return descEl && descEl.textContent ? descEl.textContent.trim() : '';
    }

    for (let i = 0; i < placemarks.length; i++) {
        const placemark = placemarks[i];
        const nameEl = placemark.getElementsByTagNameNS ? placemark.getElementsByTagNameNS(KML_NS, 'name')[0] : placemark.querySelector('name');
        const name = nameEl ? nameEl.textContent.trim() : '';
        const description = getDesc(placemark);

        const pointCoord = findCoords(placemark, 'Point', 'coordinates');
        if (pointCoord) {
            const parts = pointCoord.split(',');
            if (parts.length >= 2) {
                const lon = parseFloat(parts[0]);
                const lat = parseFloat(parts[1]);
                if (!isNaN(lat) && !isNaN(lon)) {
                    features.push({
                        type: 'Feature',
                        properties: { name, description, geomType: 'Point' },
                        geometry: { type: 'Point', coordinates: [lon, lat] }
                    });
                }
            }
        }

        const lineCoord = findCoords(placemark, 'LineString', 'coordinates');
        if (lineCoord) {
            const coords = lineCoord.split(/\s+/)
                .map(c => c.split(','))
                .filter(p => p.length >= 2)
                .map(p => [parseFloat(p[0]), parseFloat(p[1])])
                .filter(c => !isNaN(c[0]) && !isNaN(c[1]));
            if (coords.length > 0) {
                features.push({
                    type: 'Feature',
                    properties: { name, description, geomType: 'LineString' },
                    geometry: { type: 'LineString', coordinates: coords }
                });
            }
        }

        const polyGeom = placemark.getElementsByTagNameNS ? placemark.getElementsByTagNameNS(KML_NS, 'Polygon')[0] : placemark.querySelector('Polygon');
        if (polyGeom) {
            const ring = polyGeom.getElementsByTagNameNS ? polyGeom.getElementsByTagNameNS(KML_NS, 'LinearRing')[0] : polyGeom.querySelector('LinearRing');
            const coordEl = ring ? (ring.getElementsByTagNameNS ? ring.getElementsByTagNameNS(KML_NS, 'coordinates')[0] : ring.querySelector('coordinates')) : null;
            if (coordEl && coordEl.textContent) {
                const coordText = coordEl.textContent.trim();
                const coords = coordText.split(/\s+/)
                    .map(c => c.split(','))
                    .filter(p => p.length >= 2)
                    .map(p => [parseFloat(p[0]), parseFloat(p[1])])
                    .filter(c => !isNaN(c[0]) && !isNaN(c[1]));
                if (coords.length > 0) {
                    features.push({
                        type: 'Feature',
                        properties: { name, description, geomType: 'Polygon' },
                        geometry: { type: 'Polygon', coordinates: [coords] }
                    });
                }
            }
        }
    }

    return { type: 'FeatureCollection', features };
}

// Plota o KML gerado no mapa com estilo simplificado
function showGeneratedKmlOnMap(kmlText) {
    if (!map || !mapInitialized) {
        return;
    }

    // Remove numeração de vértices e camadas anteriores
    resetMapState();

    let geojson;
    try {
        geojson = buildGeoJsonFromKml(kmlText);
    } catch (error) {
        console.error('Erro ao converter KML para GeoJSON:', error);
        return;
    }

    if (!window.generatedLayerGroup) {
        window.generatedLayerGroup = L.layerGroup().addTo(map);
    }
    window.generatedLayerGroup.clearLayers();

    // Mapeia labels de postes a partir de pontos com padrão "N | ..."
    const posteLabelByIndex = new Map();
    geojson.features.forEach((feature) => {
        if (feature.geometry && feature.geometry.type === 'Point') {
            const name = feature.properties?.name || '';
            const match = name.match(/^\s*(\d+)\s*\|/);
            if (match) {
                posteLabelByIndex.set(parseInt(match[1], 10), name);
            }
        }
    });

    function getLabelForPolygonName(name) {
        if (!name) return '';
        const quadMatch = name.match(/^Quadrado\s+(\d+)/i);
        if (quadMatch) {
            const idx = parseInt(quadMatch[1], 10);
            return posteLabelByIndex.get(idx) || name;
        }
        const baseMatch = name.match(/^Base Concreto\s+(\d+)/i);
        if (baseMatch) {
            const idx = parseInt(baseMatch[1], 10);
            return posteLabelByIndex.get(idx) || name;
        }
        return name;
    }

    function haversineDistanceMeters(a, b) {
        const R = 6371000;
        const toRad = (v) => (v * Math.PI) / 180;
        const dLat = toRad(b[0] - a[0]);
        const dLon = toRad(b[1] - a[1]);
        const lat1 = toRad(a[0]);
        const lat2 = toRad(b[0]);
        const sinDLat = Math.sin(dLat / 2);
        const sinDLon = Math.sin(dLon / 2);
        const h = sinDLat * sinDLat + Math.cos(lat1) * Math.cos(lat2) * sinDLon * sinDLon;
        return 2 * R * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
    }

    function lineLengthMeters(coords) {
        let total = 0;
        for (let i = 1; i < coords.length; i++) {
            total += haversineDistanceMeters(coords[i - 1], coords[i]);
        }
        return total;
    }

    function popupContentPoste(props) {
        const desc = props?.description || '';
        const name = props?.name || '';
        if (desc && desc.length > 2) return desc;
        return name || 'Poste';
    }

    const pontos = L.geoJSON(geojson, {
        filter: f => f.geometry && f.geometry.type === 'Point',
        pointToLayer: (f, latlng) => L.marker(latlng, {
            opacity: 0,
            icon: L.divIcon({ className: '', html: '', iconSize: [1, 1] })
        }),
        onEachFeature: (f, layer) => {
            const content = popupContentPoste(f.properties);
            if (content) layer.bindPopup(content);
        }
    }).addTo(window.generatedLayerGroup);

    const linhas = L.geoJSON(geojson, {
        filter: f => f.geometry && f.geometry.type === 'LineString',
        style: () => ({ color: '#3388ff', weight: 4, opacity: 0.9 }),
        onEachFeature: (f, layer) => {
            const coords = f.geometry?.coordinates || [];
            const latlngs = coords
                .map(coord => [parseFloat(coord[1]), parseFloat(coord[0])])
                .filter(coord => !isNaN(coord[0]) && !isNaN(coord[1]));
            if (latlngs.length > 1) {
                const total = lineLengthMeters(latlngs);
                layer.bindPopup(`Distância: ${total.toFixed(1).replace('.', ',')} m`);
            } else if (f.properties?.name) {
                layer.bindPopup(f.properties.name);
            }
        }
    }).addTo(window.generatedLayerGroup);

    const poligonos = L.geoJSON(geojson, {
        filter: f => f.geometry && f.geometry.type === 'Polygon',
        style: () => ({ color: '#e63946', fillColor: '#e63946', weight: 2, fillOpacity: 0.35 }),
        onEachFeature: (f, layer) => {
            const content = popupContentPoste(f.properties) || getLabelForPolygonName(f.properties?.name || '');
            if (content) layer.bindPopup(content);
        }
    }).addTo(window.generatedLayerGroup);

    const group = L.featureGroup([pontos, linhas, poligonos]);
    if (group.getBounds().isValid()) {
        map.fitBounds(group.getBounds().pad(0.15));
    }
}

// Função para criar marcador numerado
function createNumberedMarker(lat, lon, number) {
    const markerIcon = L.divIcon({
        className: 'numbered-marker',
        html: `<div class="marker-number-label">${number}</div>`,
        iconSize: [15, 15],
        iconAnchor: [8, 8],
        popupAnchor: [0, -8]
    });
    
    const marker = L.marker([lat, lon], { icon: markerIcon }).addTo(map);
    marker.bindPopup(`<strong>Vértice ${number}</strong><br>Lat: ${lat.toFixed(6)}<br>Lon: ${lon.toFixed(6)}`);
    
    // Armazena o número do vértice para facilitar atualização
    marker.vertexNumber = number;
    
    return marker;
}

// Função para atualizar número do marcador
function updateMarkerNumber(marker, newNumber) {
    marker.vertexNumber = newNumber;
    const markerIcon = L.divIcon({
        className: 'numbered-marker',
        html: `<div class="marker-number-label">${newNumber}</div>`,
        iconSize: [15, 15],
        iconAnchor: [8, 8],
        popupAnchor: [0, -8]
    });
    marker.setIcon(markerIcon);
    const latlng = marker.getLatLng();
    marker.bindPopup(`<strong>Vértice ${newNumber}</strong><br>Lat: ${latlng.lat.toFixed(6)}<br>Lon: ${latlng.lng.toFixed(6)}`);
}

// Função para criar segmentos individuais de linha entre vértices consecutivos
function createSegmentPolylines(vertices) {
    // Limpa segmentos anteriores (camada de destaque)
    if (window.segmentPolylines) {
        window.segmentPolylines.forEach((segmentData) => {
            if (segmentData.polyline) {
                try { map.removeLayer(segmentData.polyline); } catch(e) {}
            }
        });
    }
    window.segmentPolylines = new Map();
    
    if (!vertices || vertices.length < 2) {
        return;
    }
    
    // Armazena referências aos segmentos para destacamento
    // Não cria linhas agora, apenas armazena as referências
    // As linhas originais do KML já são desenhadas
    for (let i = 0; i < vertices.length - 1; i++) {
        const v1 = vertices[i];
        const v2 = vertices[i + 1];
        const segmentKey = `${v1.number}-${v2.number}`;
        
        // Armazena apenas a referência dos vértices para criar highlight quando necessário
        window.segmentPolylines.set(segmentKey, {
            v1: v1,
            v2: v2,
            polyline: null // Será criado quando selecionado
        });
    }
}

// Função para destacar segmentos selecionados
function highlightSelectedSegments() {
    if (!naoIntercalarPostes || !window.segmentPolylines) {
        return;
    }
    
    // Obtém todas as opções selecionadas
    const selectedOptions = Array.from(naoIntercalarPostes.selectedOptions);
    const selectedValues = selectedOptions.map(opt => opt.value);
    
    // Remove todos os segmentos de destaque existentes
    window.segmentPolylines.forEach((segmentData, segmentKey) => {
        if (segmentData.polyline) {
            try {
                map.removeLayer(segmentData.polyline);
            } catch(e) {}
            segmentData.polyline = null;
        }
    });
    
    // Cria linhas destacadas para os segmentos selecionados
    window.segmentPolylines.forEach((segmentData, segmentKey) => {
        if (selectedValues.includes(segmentKey)) {
            // Cria polyline destacada (vermelha) sobre a linha original
            const highlightPolyline = L.polyline(
                [[segmentData.v1.lat, segmentData.v1.lon], [segmentData.v2.lat, segmentData.v2.lon]],
                {
                    color: '#ff4444', // Vermelho para destacar
                    weight: 6,
                    opacity: 1.0,
                    zIndexOffset: 1000 // Garante que fique acima das linhas originais
                }
            ).addTo(map);
            
            // Armazena referência
            segmentData.polyline = highlightPolyline;
        }
    });
}

// Função para inverter sentido da numeração
function inverterSentido() {
    if (!window.currentMarkers || window.currentMarkers.length === 0) {
        showMessage(errorMessage, 'Nenhum vértice encontrado no mapa para inverter.', true);
        return;
    }
    
    const totalVertices = window.currentMarkers.length;
    
    if (totalVertices < 2) {
        showMessage(errorMessage, 'É necessário pelo menos 2 vértices para inverter o sentido.', true);
        return;
    }
    
    // Inverte a numeração: se tem N vértices, o vértice na posição i vira (N + 1) - i
    // Exemplo: 3 vértices (1, 2, 3) → (3+1-1=3, 3+1-2=2, 3+1-3=1) → (3, 2, 1)
    window.currentMarkers.forEach((marker, index) => {
        // index começa em 0, então número atual = index + 1
        const numeroAtual = index + 1;
        const novoNumero = totalVertices + 1 - numeroAtual;
        
        updateMarkerNumber(marker, novoNumero);
    });
    
    // Reordena o array para manter a ordem invertida
    window.currentMarkers.reverse();
    
    // Atualiza o select "Não Intercalar Postes" com a nova ordem
    const allVertices = window.currentMarkers.map((marker, index) => ({
        number: marker.vertexNumber,
        lat: marker.getLatLng().lat,
        lon: marker.getLatLng().lng
    }));
    
    // Recria os segmentos com a nova ordem
    createSegmentPolylines(allVertices);
    
    // Atualiza o select
    populateNaoIntercalarPostes(allVertices);
    
    // Aplica destacamento se houver seleções
    highlightSelectedSegments();
    
    showMessage(successMessage, `✅ Sentido invertido! ${totalVertices} vértices renumerados.`);
    console.log(`Sentido invertido: ${totalVertices} vértices`);
}

// Função para popular o select "Não Intercalar Postes"
function populateNaoIntercalarPostes(vertices) {
    if (!naoIntercalarPostes || !vertices || vertices.length < 2) {
        return;
    }
    
    // Salva seleções atuais antes de limpar
    const selectedValues = Array.from(naoIntercalarPostes.selectedOptions).map(opt => opt.value);
    
    // Limpa o select
    naoIntercalarPostes.innerHTML = '';
    
    // Cria opções no formato "X-Y" (exceto o último vértice)
    for (let i = 0; i < vertices.length - 1; i++) {
        const currentNum = vertices[i].number;
        const nextNum = vertices[i + 1].number;
        const optionText = `${currentNum}-${nextNum}`;
        const optionValue = `${currentNum}-${nextNum}`;
        
        const option = document.createElement('option');
        option.value = optionValue;
        option.textContent = optionText;
        option.dataset.startNum = String(currentNum);
        
        // Restaura seleção se estava selecionada antes
        if (selectedValues.includes(optionValue)) {
            option.selected = true;
        }
        
        naoIntercalarPostes.appendChild(option);
    }
}

// Função para limpar o estado do mapa antes de carregar novo arquivo
function resetMapState() {
    // Remove camada do KML gerado (postes, cabos, bases)
    if (window.generatedLayerGroup) {
        window.generatedLayerGroup.clearLayers();
    }
    // Remove marcadores e polylines existentes
    if (window.currentMarkers) {
        window.currentMarkers.forEach(marker => {
            try { map.removeLayer(marker); } catch(e) {}
        });
    }
    if (window.currentPolylines) {
        window.currentPolylines.forEach(polyline => {
            try { map.removeLayer(polyline); } catch(e) {}
        });
    }
    
    // Remove polilinha manual se existir
    if (manualPolyline) {
        try {
            map.removeLayer(manualPolyline);
        } catch(e) {}
        manualPolyline = null;
    }
    
    // Limpa linha temporária
    clearTempPolyline();
    
    window.currentMarkers = [];
    window.currentPolylines = [];
    window.segmentPolylines = new Map(); // Armazena segmentos individuais por par de vértices
    
    // Desativa modo manual quando arquivo é carregado
    deactivateManualMode();
    manualVertices = []; // Limpa vértices manuais
    
    // Desabilita botão de inverter sentido e botão abrir tabela quando limpar
    btnInverterSentido.disabled = true;
    if (btnAbrirTabela) {
        btnAbrirTabela.disabled = true;
    }
    
    // Limpa o select "Não Intercalar Postes"
    if (naoIntercalarPostes) {
        naoIntercalarPostes.innerHTML = '<option value="">Nenhum vértice carregado</option>';
    }
    
    // Limpa segmentos
    if (window.segmentPolylines) {
        window.segmentPolylines.forEach((segmentData) => {
            if (segmentData && segmentData.polyline) {
                try { map.removeLayer(segmentData.polyline); } catch(e) {}
            }
        });
        window.segmentPolylines.clear();
    }
}

// Função auxiliar: obtém texto de coordenadas KML (suporta namespace - evita deslocamento)
function getKmlCoordText(parent, geomTag, innerTag) {
    const KML_NS = 'http://www.opengis.net/kml/2.2';
    const geom = parent.getElementsByTagNameNS ? parent.getElementsByTagNameNS(KML_NS, geomTag)[0] : parent.querySelector(geomTag);
    if (!geom) return null;
    const coordEl = geom.getElementsByTagNameNS ? geom.getElementsByTagNameNS(KML_NS, innerTag)[0] : geom.querySelector(innerTag);
    return coordEl && coordEl.textContent ? coordEl.textContent.trim() : null;
}
function getKmlPolygonCoordText(placemark) {
    const KML_NS = 'http://www.opengis.net/kml/2.2';
    const poly = placemark.getElementsByTagNameNS ? placemark.getElementsByTagNameNS(KML_NS, 'Polygon')[0] : placemark.querySelector('Polygon');
    if (!poly) return null;
    const ring = poly.getElementsByTagNameNS ? poly.getElementsByTagNameNS(KML_NS, 'LinearRing')[0] : poly.querySelector('LinearRing');
    const coordEl = ring ? (ring.getElementsByTagNameNS ? ring.getElementsByTagNameNS(KML_NS, 'coordinates')[0] : ring.querySelector('coordinates')) : null;
    return coordEl && coordEl.textContent ? coordEl.textContent.trim() : null;
}

// Função para parsear e exibir KML no mapa
function parseAndDisplayKML(kmlText) {
    try {
        console.log('Parseando KML...');
        resetMapState();

        const parser = new DOMParser();
        const kmlDoc = parser.parseFromString(kmlText, 'text/xml');
        
        // Verifica erros de parsing
        const parseError = kmlDoc.querySelector('parsererror');
        if (parseError) {
            throw new Error('Erro ao fazer parse do KML: ' + parseError.textContent);
        }

        const KML_NS = 'http://www.opengis.net/kml/2.2';
        const placemarksRaw = kmlDoc.getElementsByTagNameNS ? kmlDoc.getElementsByTagNameNS(KML_NS, 'Placemark') : kmlDoc.querySelectorAll('Placemark');
        const placemarks = Array.from(placemarksRaw);
        let bounds = [];
        let allVertices = []; // Array para armazenar todos os vértices na ordem
        let sequence = 1; // Começa em 1
        const vertexMap = new Map(); // Mapa para rastrear vértices já numerados

        // Função auxiliar para adicionar vértice se não existir
        function addVertexIfNew(lat, lon) {
            const key = `${lat.toFixed(6)}_${lon.toFixed(6)}`;
            if (!vertexMap.has(key)) {
                vertexMap.set(key, sequence);
                allVertices.push({ lat, lon, number: sequence });
                bounds.push([lat, lon]);
                sequence++;
            }
        }

        // Primeiro, processa LineString (prioridade para manter ordem)
        // KML: longitude,latitude,altitude (lon,lat,alt)
        placemarks.forEach((placemark) => {
            const coordText = getKmlCoordText(placemark, 'LineString', 'coordinates');
            if (coordText) {
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return { lat: parseFloat(parts[1]), lon: parseFloat(parts[0]) };
                }).filter(coord => !isNaN(coord.lat) && !isNaN(coord.lon));
                coords.forEach(coord => addVertexIfNew(coord.lat, coord.lon));
            }
        });

        // Depois, processa Polygon
        placemarks.forEach((placemark) => {
            const coordText = getKmlPolygonCoordText(placemark);
            if (coordText) {
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return { lat: parseFloat(parts[1]), lon: parseFloat(parts[0]) };
                }).filter(coord => !isNaN(coord.lat) && !isNaN(coord.lon));
                coords.forEach(coord => addVertexIfNew(coord.lat, coord.lon));
            }
        });

        // Por último, processa Points isolados (KML: lon,lat,alt)
        placemarks.forEach((placemark) => {
            const coordText = getKmlCoordText(placemark, 'Point', 'coordinates');
            if (coordText) {
                const parts = coordText.split(',');
                const lon = parseFloat(parts[0]);
                const lat = parseFloat(parts[1]);
                if (!isNaN(lat) && !isNaN(lon)) addVertexIfNew(lat, lon);
            }
        });

        // Cria marcadores numerados para cada vértice
        allVertices.forEach(vertex => {
            const marker = createNumberedMarker(vertex.lat, vertex.lon, vertex.number);
            window.currentMarkers.push(marker);
        });
        
        // Cria segmentos individuais entre vértices consecutivos
        createSegmentPolylines(allVertices);
        
        // Salva vértices no formato esperado pela função gerarMatriz
        // Formato: [{lat, lon, number}, ...]
        window.kmlVertices = allVertices.map(v => ({
            lat: v.lat,
            lon: v.lon,
            number: v.number,
            sequencia: v.number
        }));
        
        // Habilita botão de inverter sentido e botão abrir tabela se houver marcadores
        if (window.currentMarkers.length > 0) {
            btnInverterSentido.disabled = false;
            if (btnAbrirTabela) {
                btnAbrirTabela.disabled = false;
            }
            // Popula o select "Não Intercalar Postes"
            populateNaoIntercalarPostes(allVertices);
        }

        // Agora desenha as linhas e polígonos originais do KML
        placemarks.forEach((placemark) => {
            const coordText = getKmlCoordText(placemark, 'LineString', 'coordinates');
            if (coordText) {
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return [parseFloat(parts[1]), parseFloat(parts[0])];
                }).filter(c => !isNaN(c[0]) && !isNaN(c[1]));
                
                if (coords.length > 0) {
                    const polyline = L.polyline(coords, {
                        color: '#3388ff',
                        weight: 4,
                        opacity: 0.8
                    }).addTo(map);
                    window.currentPolylines.push(polyline);
                }
            }

            const polyCoordText = getKmlPolygonCoordText(placemark);
            if (polyCoordText) {
                const coords = polyCoordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return [parseFloat(parts[1]), parseFloat(parts[0])];
                }).filter(c => !isNaN(c[0]) && !isNaN(c[1]));
                
                if (coords.length > 0) {
                    const polygonLayer = L.polygon(coords, {
                        color: '#3388ff',
                        fillColor: '#3388ff',
                        fillOpacity: 0.3,
                        weight: 2
                    }).addTo(map);
                    window.currentPolylines.push(polygonLayer);
                }
            }
        });

        // Ajusta o zoom para mostrar todos os elementos
        if (bounds.length > 0) {
            console.log('Ajustando zoom para ' + bounds.length + ' pontos');
            map.fitBounds(bounds, { padding: [50, 50] });
            showMessage(successMessage, `✅ KML carregado no mapa! ${allVertices.length} vértices numerados e ${window.currentPolylines.length} linhas exibidas.`);
        } else {
            console.warn('Nenhum elemento encontrado no KML');
            showMessage(errorMessage, 'Nenhum elemento encontrado no KML.', true);
        }
    } catch (error) {
        console.error('Erro ao processar KML:', error);
        showMessage(errorMessage, 'Erro ao processar KML: ' + error.message, true);
    }
}

// Função para parsear e exibir GeoJSON inline no mapa
function parseAndDisplayGeoJSON(geojson) {
    try {
        console.log('Parseando GeoJSON...');
        resetMapState();
        
        if (!geojson || !geojson.features || !Array.isArray(geojson.features)) {
            throw new Error('GeoJSON inválido.');
        }
        
        let bounds = [];
        let allVertices = [];
        let sequence = 1;
        const vertexMap = new Map();
        
        function addVertexIfNew(lat, lon) {
            const key = `${lat.toFixed(6)}_${lon.toFixed(6)}`;
            if (!vertexMap.has(key)) {
                vertexMap.set(key, sequence);
                allVertices.push({ lat, lon, number: sequence });
                bounds.push([lat, lon]);
                sequence++;
            }
        }
        
        // Processa LineString primeiro para manter a ordem
        const lineFeatures = geojson.features.filter(f => f.geometry && f.geometry.type === 'LineString');
        if (lineFeatures.length > 0) {
            const coords = lineFeatures[0].geometry.coordinates || [];
            coords.forEach(coord => {
                if (Array.isArray(coord) && coord.length >= 2) {
                    const lon = parseFloat(coord[0]);
                    const lat = parseFloat(coord[1]);
                    if (!isNaN(lat) && !isNaN(lon)) {
                        addVertexIfNew(lat, lon);
                    }
                }
            });
        }
        
        // Processa Polygon
        geojson.features.forEach(feature => {
            if (feature.geometry && feature.geometry.type === 'Polygon') {
                const rings = feature.geometry.coordinates || [];
                rings.forEach(ring => {
                    ring.forEach(coord => {
                        if (Array.isArray(coord) && coord.length >= 2) {
                            const lon = parseFloat(coord[0]);
                            const lat = parseFloat(coord[1]);
                            if (!isNaN(lat) && !isNaN(lon)) {
                                addVertexIfNew(lat, lon);
                            }
                        }
                    });
                });
            }
        });
        
        // Processa Points isolados
        geojson.features.forEach(feature => {
            if (feature.geometry && feature.geometry.type === 'Point') {
                const coord = feature.geometry.coordinates || [];
                if (Array.isArray(coord) && coord.length >= 2) {
                    const lon = parseFloat(coord[0]);
                    const lat = parseFloat(coord[1]);
                    if (!isNaN(lat) && !isNaN(lon)) {
                        addVertexIfNew(lat, lon);
                    }
                }
            }
        });
        
        // Cria marcadores numerados para cada vértice
        allVertices.forEach(vertex => {
            const marker = createNumberedMarker(vertex.lat, vertex.lon, vertex.number);
            window.currentMarkers.push(marker);
        });
        
        // Cria segmentos individuais entre vértices consecutivos
        createSegmentPolylines(allVertices);
        
        // Salva vértices no formato esperado pela função gerarMatriz
        window.kmlVertices = allVertices.map(v => ({
            lat: v.lat,
            lon: v.lon,
            number: v.number,
            sequencia: v.number
        }));
        
        // Desenha features do GeoJSON no mapa
        geojson.features.forEach(feature => {
            if (!feature.geometry) return;
            
            if (feature.geometry.type === 'LineString') {
                const coords = feature.geometry.coordinates || [];
                const latlngs = coords
                    .map(coord => [parseFloat(coord[1]), parseFloat(coord[0])])
                    .filter(coord => !isNaN(coord[0]) && !isNaN(coord[1]));
                
                if (latlngs.length > 0) {
                    const polyline = L.polyline(latlngs, {
                        color: '#3388ff',
                        weight: 4,
                        opacity: 0.8
                    }).addTo(map);
                    window.currentPolylines.push(polyline);
                }
            }
            
            if (feature.geometry.type === 'Polygon') {
                const rings = feature.geometry.coordinates || [];
                rings.forEach(ring => {
                    const latlngs = ring
                        .map(coord => [parseFloat(coord[1]), parseFloat(coord[0])])
                        .filter(coord => !isNaN(coord[0]) && !isNaN(coord[1]));
                    
                    if (latlngs.length > 0) {
                        const polygonLayer = L.polygon(latlngs, {
                            color: '#3388ff',
                            fillColor: '#3388ff',
                            fillOpacity: 0.3,
                            weight: 2
                        }).addTo(map);
                        window.currentPolylines.push(polygonLayer);
                    }
                });
            }
        });
        
        // Habilita botões e popula select
        if (window.currentMarkers.length > 0) {
            btnInverterSentido.disabled = false;
            if (btnAbrirTabela) {
                btnAbrirTabela.disabled = false;
            }
            populateNaoIntercalarPostes(allVertices);
        }
        
        if (bounds.length > 0) {
            map.fitBounds(bounds, { padding: [50, 50] });
            showMessage(successMessage, `✅ GeoJSON carregado no mapa! ${allVertices.length} vértices numerados e ${window.currentPolylines.length} linhas/polígonos exibidos.`);
        } else {
            showMessage(errorMessage, 'Nenhum elemento encontrado no GeoJSON.', true);
        }
    } catch (error) {
        console.error('Erro ao processar GeoJSON:', error);
        showMessage(errorMessage, 'Erro ao processar GeoJSON: ' + error.message, true);
    }
}

// Adiciona evento ao botão Plotar Projeto
btnPlotarProjeto.addEventListener('click', async function() {
    console.log('Botão Plotar Projeto clicado');
    
    // Fluxo 1: CSV importado - desenha no mapa e baixa CSV, KML, HTML
    if (window.arquivoCSVImportado && window.arquivoCSVImportado.content) {
        plotarProjetoComCSV();
        return;
    }
    
    // Fluxo 2: KML/HTML no fileInput - carrega no mapa
    const file = fileInput.files[0];
    if (!file) {
        showMessage(errorMessage, 'Importe um CSV ou selecione um arquivo KML/HTML primeiro.', true);
        return;
    }
    
    const fileNameStr = file.name.toLowerCase();
    if (fileNameStr.endsWith('.kml') || fileNameStr.endsWith('.kmz') || fileNameStr.endsWith('.html')) {
        if (fileNameStr.endsWith('.html')) {
            loadGeoJSONOnMap(file);
        } else {
            loadKMLOnMap(file);
        }
    } else {
        showMessage(errorMessage, 'Para Plotar Projeto: importe CSV ou selecione KML/KMZ/HTML.', true);
    }
});

// Desenha projeto no mapa e baixa CSV, KML, HTML a partir do CSV importado
async function plotarProjetoComCSV() {
    const { content: csvContent, filename: csvFilename } = window.arquivoCSVImportado;
    if (!csvContent) return;
    
    const mapContainer = document.getElementById('line-map-container');
    if (mapContainer) mapContainer.style.display = 'block';
    
    if (!mapInitialized || !map) {
        waitForLeaflet(function() {
            if (!mapInitialized) initMap();
            setTimeout(() => plotarProjetoComCSV(), 300);
        });
        return;
    }
    
    if (typeof Papa === 'undefined') {
        showMessage(errorMessage, 'Biblioteca PapaParse não carregada.', true);
        return;
    }
    
    const firstLine = csvContent.split(/\r?\n/)[0] || '';
    const delimiter = firstLine.indexOf(';') >= 0 ? ';' : ',';
    
    let dados;
    try {
        const result = Papa.parse(csvContent, { header: true, skipEmptyLines: true, delimiter });
        dados = result.data;
    } catch (err) {
        showMessage(errorMessage, 'Erro ao processar CSV: ' + err.message, true);
        return;
    }
    if (!dados || dados.length === 0) {
        showMessage(errorMessage, 'Arquivo CSV vazio ou inválido.', true);
        return;
    }
    
    const vertices = extrairVerticesDoCSV(dados);
    if (vertices.length === 0) {
        showMessage(errorMessage, 'Não foi possível extrair vértices do CSV. Verifique as colunas lat, long.', true);
        return;
    }
    
    window.ultimoArquivoCSVImportado = csvFilename;
    showMessage(successMessage, 'Processando... Aguarde.');
    btnPlotarProjeto.disabled = true;
    btnPlotarProjeto.textContent = 'Baixando...';
    
    try {
        const trecho = csvFilename.replace(/\.csv$/i, '').replace(/\s+/g, '_');
        const csvBase64 = btoa(unescape(encodeURIComponent(csvContent)));
        
        const isProduction = window.location.protocol.startsWith('http') &&
            window.location.hostname !== 'localhost' &&
            window.location.hostname !== '127.0.0.1';
        let API_URL = isProduction ? `${window.location.origin}/api/plotar-projeto-csv/` : null;
        
        if (!isProduction) {
            const PORTS = [8001, 8000, 8002, 8003, 8004];
            for (const port of PORTS) {
                try {
                    const ctrl = new AbortController();
                    const tid = setTimeout(() => ctrl.abort(), 5000);
                    const r = await fetch(`http://localhost:${port}/api/test/`, { signal: ctrl.signal });
                    clearTimeout(tid);
                    if (r.ok) {
                        API_URL = `http://localhost:${port}/api/plotar-projeto-csv/`;
                        break;
                    }
                } catch (e) { continue; }
            }
        }
        
        if (!API_URL) {
            showMessage(errorMessage, 'Servidor não encontrado. Execute: backend\\api\\start_server.bat', true);
            return;
        }
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ csv_content: csvBase64, trecho })
        });
        
        if (!response.ok) {
            const err = await response.json().catch(() => ({ message: response.statusText }));
            throw new Error(err.message || 'Erro no servidor');
        }
        
        const result = await response.json();
        
        const kmlDecoded = result.kml_content && result.kml_filename ? atob(result.kml_content) : null;
        if (kmlDecoded) showGeneratedKmlOnMap(kmlDecoded);

        downloadFile(new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' }), csvFilename, 'text/csv;charset=utf-8');
        if (kmlDecoded && result.kml_filename) {
            setTimeout(function() {
                downloadFile(new Blob([kmlDecoded], { type: 'application/vnd.google-earth.kml+xml' }), result.kml_filename, 'application/vnd.google-earth.kml+xml');
            }, 350);
        }
        if (GERAR_HTML_PROJETO && kmlDecoded && result.kml_filename) {
            setTimeout(async function() {
                try {
                    const geojson = buildGeoJsonFromKml(kmlDecoded);
                    const trechoNome = (result.kml_filename || '').replace('_quadrados_bissetriz.kml', '') || 'projeto';
                    const htmlContent = gerarProjetoHTML(geojson, trechoNome);
                    downloadFile(new Blob([htmlContent], { type: 'text/html;charset=utf-8' }), trechoNome + '_projeto.html', 'text/html;charset=utf-8');
                    const shareUrl = await compartilharProjetoLink(htmlContent, API_URL);
                    if (shareUrl && shareUrl.startsWith('https')) {
                        try {
                            await navigator.clipboard.writeText(shareUrl);
                            showMessage(successMessage, 'Link copiado! Envie pelo WhatsApp - ao abrir o link, o GPS da bolinha azul funciona.');
                        } catch (_) {
                            showMessage(successMessage, 'Para GPS no celular, envie este link: ' + shareUrl);
                        }
                    }
                } catch (e) {
                    console.error('Erro ao gerar HTML:', e);
                }
            }, 700);
        }

        showMessage(successMessage, 'Projeto desenhado e arquivos baixados (CSV, KML).');
    } catch (err) {
        showMessage(errorMessage, 'Erro: ' + (err.message || 'não foi possível baixar KML.'), true);
    } finally {
        if (btnPlotarProjeto) {
            btnPlotarProjeto.disabled = false;
            btnPlotarProjeto.textContent = 'Plotar Projeto';
        }
    }
}

// Adiciona evento ao botão Inverter Sentido
if (btnInverterSentido) {
    btnInverterSentido.addEventListener('click', function() {
        console.log('Botão Inverter Sentido clicado');
        inverterSentido();
    });
}

// Adiciona evento ao botão Abrir Tabela
if (btnAbrirTabela) {
    btnAbrirTabela.addEventListener('click', function() {
        console.log('Botão Abrir Tabela clicado');
        // Abre a tabela em nova aba
        window.open('tabela.html', '_blank');
    });
}

// Adiciona evento ao botão Finalizar Polilinha
if (btnFinalizarPolilinha) {
    btnFinalizarPolilinha.addEventListener('click', function() {
        console.log('Botão Finalizar Polilinha clicado');
        finalizeManualPolyline();
    });
}

/**
 * Gera link compartilhável do projeto (HTTPS). GPS funciona no celular ao abrir o link.
 * @param {string} htmlContent - HTML do projeto
 * @param {string} apiBaseUrl - URL base da API (ex: https://site.com/api/)
 * @returns {Promise<string|null>} URL ou null
 */
async function compartilharProjetoLink(htmlContent, apiBaseUrl) {
    if (!apiBaseUrl || !htmlContent) return null;
    const shareUrl = apiBaseUrl.replace(/\/api\/[^/]+\/?$/, '/api/compartilhar-projeto/');
    try {
        const htmlB64 = btoa(unescape(encodeURIComponent(htmlContent)));
        const r = await fetch(shareUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ html_content: htmlB64 })
        });
        if (!r.ok) return null;
        const data = await r.json();
        if (data.success && data.url) return data.url;
        return null;
    } catch (e) {
        return null;
    }
}

// Função para fazer download de arquivo
function downloadFile(blob, filename, mimeType) {
    if (typeof saveAs !== 'undefined') {
        saveAs(blob, filename);
    } else {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    }
}

// Função para coletar dados do formulário e chamar a API Python
async function gerarMatriz() {
    console.log('Botão Gerar Matriz clicado');
    
    // Coleta dados do formulário
    const numeroModuloValue = numeroModulo ? numeroModulo.value.trim() : '';
    if (!numeroModuloValue) {
        showMessage(errorMessage, 'Por favor, digite o número do módulo.', true);
        return;
    }
    
    // Busca dados do módulo na tabela
    const moduloData = buscarModuloPorCodigo(numeroModuloValue);
    if (!moduloData) {
        showMessage(errorMessage, 'Módulo não encontrado na tabela. Verifique o número do módulo.', true);
        return;
    }
    
    // Verifica se há vértices carregados (KML ou manual)
    if (!window.kmlVertices || window.kmlVertices.length === 0) {
        showMessage(errorMessage, 'Por favor, carregue um KML, importe um CSV ou crie uma polilinha manualmente no mapa.', true);
        return;
    }
    
    // Coleta vértices (KML, CSV ou manual)
    const vertices = window.kmlVertices.map(v => [v.lat, v.lon, v.number || v.sequencia || v.number]);
    
    // Coleta trecho do arquivo KML (usa nome do arquivo ou padrão)
    const file = fileInput ? fileInput.files[0] : null;
    const csvName = window.ultimoArquivoCSVImportado || '';
    const trecho = file ? file.name.replace(/\.[^/.]+$/, '') : (csvName ? csvName.replace(/\.[^/.]+$/, '') : 'T001');
    
    // Coleta "Vão Frouxo" - converte "sim"/"não" para "SIM"/"NÃO"
    const vaoFrouxoElement = document.getElementById('vaoFrouxo');
    let looseGap = 'NÃO';
    if (vaoFrouxoElement) {
        const valor = vaoFrouxoElement.value.toLowerCase();
        looseGap = (valor === 'sim') ? 'SIM' : 'NÃO';
    }
    
    // Coleta "Poste da derivação" - sempre garante um valor padrão
    const posteDerivacaoElement = document.getElementById('posteDerivacao');
    let tipoPoste = 'Existente'; // Valor padrão
    if (posteDerivacaoElement && posteDerivacaoElement.value && posteDerivacaoElement.value.trim() !== '') {
        tipoPoste = posteDerivacaoElement.value.trim();
    }
    
    // Coleta "Não Intercalar Postes" - converte de "X-Y" para lista de sequências originais
    const listaNaoIntercalar = [];
    const naoIntercalarPostes = document.getElementById('naoIntercalarPostes');
    if (naoIntercalarPostes && naoIntercalarPostes.selectedOptions) {
        Array.from(naoIntercalarPostes.selectedOptions).forEach(option => {
            if (option.value && option.value.includes('-')) {
                // Extrai o número inicial do formato "X-Y"
                const startNum = parseInt(option.value.split('-')[0]);
                if (!isNaN(startNum)) {
                    listaNaoIntercalar.push(startNum);
                }
            }
        });
    }
    
    // Dados do módulo da tabela
    const moduleData = {
        codigo_modulo: moduloData.codigo_modulo || numeroModuloValue,
        codigo_abaco: moduloData.codigo_abaco || numeroModuloValue, // Fallback para codigo_modulo se não houver codigo_abaco
        descrição_modulo: moduloData.descrição_modulo || moduloData['descrição_modulo'] || '',
        distribuidora_estado: moduloData.distribuidora_estado || '',
        tipo_obra: moduloData.tipo_obra || '',
        tensão: moduloData.tensão || moduloData['tensão'] || '',
        local: moduloData.local || '',
        fases: moduloData.fases || '',
        neutro: moduloData.neutro || '',
        cabo: moduloData.cabo || '',
        vao_medio: moduloData.vao_medio || 80,
        vao_max: moduloData.vao_max || '',
        tramo_max: moduloData.tramo_max || '',
        custo_med_poste: moduloData.custo_med_poste || '',
        '%custo_poste_tang': moduloData['%custo_poste_tang'] || '',
        '%custo_poste_enc': moduloData['%custo_poste_enc'] || ''
    };
    
    // Parâmetros para a função gerar_matriz
    const params = {
        trecho: trecho,
        module_name: moduleData.codigo_abaco || numeroModuloValue, // Usa codigo_abaco ao invés de codigo_modulo
        module_data: moduleData,
        loose_gap: looseGap,
        section_size: moduleData.tramo_max || 300,
        gap_size: moduleData.vao_medio || 80,
        num_poste_inicial: '00000000',
        tipo_poste: tipoPoste,
        lista_nao_intercalar: listaNaoIntercalar,
        vertices: vertices
    };
    
    console.log('Parâmetros coletados:', params);
    
    // Desabilita o botão durante o processamento
    if (btnGerarMatriz) {
        btnGerarMatriz.disabled = true;
        btnGerarMatriz.textContent = 'Gerando Matriz...';
    }
    
    try {
        // Detecta se está em produção (HTTP/HTTPS em domínio não local)
        const isProduction = window.location.protocol.startsWith('http') &&
                            window.location.hostname !== 'localhost' &&
                            window.location.hostname !== '127.0.0.1';
        
        let API_URL = null;
        
        if (isProduction) {
            // Em produção, usa o mesmo domínio
            API_URL = `${window.location.origin}/api/gerar-matriz/`;
            console.log(`🌐 Modo PRODUÇÃO - Usando: ${API_URL}`);
        } else {
            // Em desenvolvimento, procura servidor local nas portas 8000-8004
            // Prioriza 8001 que é a porta padrão quando PORT é definido
            const PORTS = [8001, 8000, 8002, 8003, 8004];
            
            console.log('🔧 Modo DESENVOLVIMENTO - Procurando servidor nas portas 8001, 8000-8004...');
            for (const port of PORTS) {
                const testUrl = `http://localhost:${port}/api/test/`;
                console.log(`   Testando porta ${port}...`);
                try {
                    const controller = new AbortController();
                    // Aumenta timeout para 5 segundos para dar mais tempo
                    const timeoutId = setTimeout(() => controller.abort(), 5000);
                    
                    const testResponse = await fetch(testUrl, { 
                        method: 'GET',
                        signal: controller.signal,
                        headers: {
                            'Accept': 'application/json'
                        }
                    });
                    clearTimeout(timeoutId);
                    
                    if (testResponse.ok) {
                        const testData = await testResponse.json();
                        API_URL = `http://localhost:${port}/api/gerar-matriz/`;
                        console.log(`✅ Servidor encontrado na porta ${port}:`, testData);
                        break;
                    }
                } catch (e) {
                    if (e.name !== 'AbortError') {
                        console.log(`   ❌ Porta ${port} não disponível: ${e.message}`);
                    } else {
                        console.log(`   ⏱️ Porta ${port} timeout (servidor não respondeu em 5s)`);
                    }
                    continue;
                }
            }
            
            if (!API_URL) {
                throw new Error('Servidor Flask não encontrado nas portas 8001, 8000-8004.\n\n' +
                    '📋 Para resolver:\n' +
                    '1. Execute: python backend/api/server_flask.py\n' +
                    '2. Ou execute: backend\\api\\start_server.bat\n' +
                    '3. Aguarde ver a mensagem: "API disponível em..."\n' +
                    '4. Mantenha o terminal aberto e tente novamente\n\n' +
                    '💡 Dica: Você pode acessar o frontend diretamente pelo Flask em:\n' +
                    '   http://localhost:8001/ (em vez de usar servidor HTTP separado)');
            }
        }
        
        console.log('Fazendo requisição para:', API_URL);
        console.log('Parâmetros enviados:', JSON.stringify(params, null, 2));
        
        // Faz a requisição POST
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        
        console.log('Resposta recebida - Status:', response.status, response.statusText);
        
        if (!response.ok) {
            let errorText = '';
            try {
                const errorData = await response.json();
                errorText = errorData.message || JSON.stringify(errorData);
                console.error('Erro da API:', errorData);
            } catch (e) {
                errorText = await response.text();
                console.error('Erro da API (texto):', errorText);
            }
            throw new Error(`Erro HTTP ${response.status}: ${errorText}`);
        }
        
        const result = await response.json();
        console.log('Resultado recebido:', result);
        
        if (result.success) {
            showMessage(successMessage, `✅ ${result.message || 'Matriz gerada com sucesso!'}`);
            
            // Faz download dos arquivos CSV e KML gerados pelo backend
            const kmlDecoded = result.kml_content && result.kml_filename ? atob(result.kml_content) : null;
            if (kmlDecoded) showGeneratedKmlOnMap(kmlDecoded);

            if (result.csv_content && result.csv_filename) {
                try {
                    const csvBlob = new Blob(['\uFEFF' + atob(result.csv_content)], { type: 'text/csv;charset=utf-8;' });
                    downloadFile(csvBlob, result.csv_filename, 'text/csv;charset=utf-8;');
                } catch (e) {
                    console.error('❌ Erro ao baixar CSV:', e);
                }
            }
            if (kmlDecoded && result.kml_filename) {
                setTimeout(function() {
                    try {
                        downloadFile(new Blob([kmlDecoded], { type: 'application/vnd.google-earth.kml+xml' }), result.kml_filename, 'application/vnd.google-earth.kml+xml');
                    } catch (e) {
                        console.error('❌ Erro ao baixar KML:', e);
                    }
                }, 350);
            }
            if (GERAR_HTML_PROJETO && kmlDecoded && result.kml_filename) {
                setTimeout(async function() {
                    try {
                        const geojson = buildGeoJsonFromKml(kmlDecoded);
                        const trechoNome = (result.kml_filename || '').replace('_quadrados_bissetriz.kml', '') || 'projeto';
                        const htmlContent = gerarProjetoHTML(geojson, trechoNome);
                        downloadFile(new Blob([htmlContent], { type: 'text/html;charset=utf-8' }), trechoNome + '_projeto.html', 'text/html;charset=utf-8');
                        const shareUrl = await compartilharProjetoLink(htmlContent, API_URL);
                        if (shareUrl && shareUrl.startsWith('https')) {
                            try {
                                await navigator.clipboard.writeText(shareUrl);
                                showMessage(successMessage, 'Link copiado! Envie pelo WhatsApp - ao abrir o link, o GPS da bolinha azul funciona.');
                            } catch (_) {
                                showMessage(successMessage, 'Para GPS no celular, envie este link: ' + shareUrl);
                            }
                        }
                    } catch (e) {
                        console.error('❌ Erro ao baixar HTML:', e);
                    }
                }, 700);
            }
            
        } else {
            throw new Error(result.message || 'Erro desconhecido ao gerar matriz');
        }
        
    } catch (error) {
        console.error('Erro ao gerar matriz:', error);
        console.error('Stack trace:', error.stack);
        
        // Tenta obter detalhes do erro da resposta se houver
        let errorDetails = '';
        if (error.response) {
            try {
                const errorData = await error.response.json();
                console.error('Detalhes do erro do servidor:', errorData);
                
                if (errorData.error_file) {
                    errorDetails += `\n\n📍 Local do erro:\n`;
                    errorDetails += `   Arquivo: ${errorData.error_file}\n`;
                    errorDetails += `   Linha: ${errorData.error_line}\n`;
                    errorDetails += `   Função: ${errorData.error_function || 'N/A'}\n`;
                }
                
                if (errorData.traceback) {
                    console.error('Stack trace completo do servidor:', errorData.traceback);
                }
            } catch (e) {
                // Ignora se não conseguir parsear JSON
            }
        }
        
        // Mostra mensagem de erro mais detalhada
        let errorMsg = `❌ Erro ao gerar matriz: ${error.message}`;
        if (error.response) {
            try {
                const errorData = await error.response.clone().json();
                if (errorData.message) {
                    errorMsg = `❌ ${errorData.message}`;
                }
                if (errorData.error_file) {
                    errorMsg += `\n\n📍 Erro em:\n   ${errorData.error_file}:${errorData.error_line}`;
                    if (errorData.error_function) {
                        errorMsg += ` (${errorData.error_function})`;
                    }
                }
            } catch (e) {
                // Usa mensagem padrão se não conseguir parsear
            }
        }
        
        if (error.message.includes('Failed to fetch') || error.message.includes('ERR_EMPTY_RESPONSE')) {
            errorMsg = `❌ Servidor não está respondendo!\n\n` +
                       `📋 Para resolver:\n` +
                       `1. Execute: python backend/api/server_flask.py\n` +
                       `2. Ou clique duas vezes em: backend\\api\\start_server.bat\n` +
                       `3. Aguarde ver a mensagem: "API disponível em..."\n` +
                       `4. Mantenha o terminal aberto e tente novamente`;
        }
        
        // Mostra mensagem de erro (usa <br> para quebras de linha)
        errorMessage.innerHTML = errorMsg.replace(/\n/g, '<br>');
        errorMessage.style.display = 'block';
        errorMessage.className = 'error-message';
        
        // Log completo no console para depuração
        console.group('🔍 Detalhes completos do erro:');
        console.error('Erro:', error);
        console.error('Stack trace:', error.stack);
        if (error.response) {
            error.response.clone().json().then(errorData => {
                console.error('Resposta do servidor:', errorData);
                if (errorData.traceback) {
                    console.error('Stack trace do servidor:', errorData.traceback);
                }
            }).catch(() => {});
        }
        console.groupEnd();
    } finally {
        // Reabilita o botão
        if (btnGerarMatriz) {
            btnGerarMatriz.disabled = false;
            btnGerarMatriz.textContent = 'Gerar Matriz';
        }
    }
}

// Adiciona evento ao botão Gerar Matriz
if (btnGerarMatriz) {
    btnGerarMatriz.addEventListener('click', gerarMatriz);
}

// Função para resetar completamente a aplicação
function resetApplication() {
    console.log('Resetando aplicação...');
    
    // Limpa o mapa - remove todas as camadas
    if (map && mapInitialized) {
        // Remove todos os markers
        if (window.currentMarkers) {
            window.currentMarkers.forEach(marker => {
                try { map.removeLayer(marker); } catch(e) {}
            });
            window.currentMarkers = [];
        }
        
        // Remove todas as polylines
        if (window.currentPolylines) {
            window.currentPolylines.forEach(polyline => {
                try { map.removeLayer(polyline); } catch(e) {}
            });
            window.currentPolylines = [];
        }
        
        // Remove segmentos
        if (window.segmentPolylines) {
            window.segmentPolylines.forEach(polyline => {
                try { map.removeLayer(polyline); } catch(e) {}
            });
            window.segmentPolylines = new Map();
        }
        
        // Remove marcador de localização do usuário
        if (userLocationMarker) {
            try { map.removeLayer(userLocationMarker); } catch(e) {}
            userLocationMarker = null;
        }
        
        if (userLocationAccuracyCircle) {
            try { map.removeLayer(userLocationAccuracyCircle); } catch(e) {}
            userLocationAccuracyCircle = null;
        }
        
        // Remove polilinha manual
        if (manualPolyline) {
            try { map.removeLayer(manualPolyline); } catch(e) {}
            manualPolyline = null;
        }
        
        // Limpa linha temporária
        clearTempPolyline();
        
        // Volta para a visualização padrão
        map.setView([-15.7942, -47.8822], 13);
        
        // Reseta cursor para o padrão do Leaflet
        map.getContainer().style.cursor = '';
    }
    
    // Limpa variáveis globais
    pontosManuais = [];
    isManualModeActive = false;
    manualVertices = [];
    tempPolyline = null;
    window.kmlVertices = [];
    window.ultimoArquivoCSVImportado = '';
    window.arquivoCSVImportado = null;
    
    // Desativa modo manual
    deactivateManualMode();
    
    // Limpa campos do formulário
    if (fileInput) fileInput.value = '';
    if (csvImportInput) csvImportInput.value = '';
    
    if (fileName) {
        fileName.textContent = '';
    }
    
    if (numeroModulo) {
        numeroModulo.value = '';
    }
    
    if (descricaoModulo) {
        descricaoModulo.textContent = '<- Digitar código do módulo';
    }
    
    if (naoIntercalarPostes) {
        naoIntercalarPostes.innerHTML = '<option value="">Nenhum vértice carregado</option>';
    }
    
    // Reseta estado dos botões
    if (btnImportarArquivo) {
        btnImportarArquivo.disabled = false;
    }
    
    if (btnGerarMatriz) {
        btnGerarMatriz.disabled = true;
    }
    
    if (btnPlotarProjeto) {
        btnPlotarProjeto.disabled = true;
    }
    
    if (btnInverterSentido) {
        btnInverterSentido.disabled = true;
    }
    
    if (btnAbrirTabela) {
        btnAbrirTabela.disabled = true;
    }
    
    if (btnFinalizarPolilinha) {
        btnFinalizarPolilinha.style.display = 'none';
    }
    
    // Limpa mensagens
    if (successMessage) {
        successMessage.style.display = 'none';
        successMessage.textContent = '';
    }
    
    if (errorMessage) {
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    }
    
    // Reativa modo manual se não houver KML
    if (map && mapInitialized) {
        checkAndActivateManualMode();
    }
    
    console.log('Aplicação resetada com sucesso');
}

// Adiciona evento de clique no logo para resetar
const logoReset = document.getElementById('logoReset');
if (logoReset) {
    logoReset.addEventListener('click', function() {
        resetApplication();
    });
    
    // Adiciona efeito visual ao passar o mouse
    logoReset.addEventListener('mouseenter', function() {
        this.style.opacity = '0.8';
        this.style.transform = 'scale(1.05)';
        this.style.transition = 'all 0.2s';
    });
    
    logoReset.addEventListener('mouseleave', function() {
        this.style.opacity = '1';
        this.style.transform = 'scale(1)';
    });
}

// Inicializa o mapa automaticamente quando a página carregar
waitForLeaflet(function() {
    console.log('Página carregada, inicializando mapa automaticamente...');
    setTimeout(function() {
        if (!mapInitialized) {
            initMap();
            console.log('Mapa inicializado automaticamente');
        }
    }, 300);
});


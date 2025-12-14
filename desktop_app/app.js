// Sistema de Importação KML - Código Principal
// Versão preparada para desktop app

// Estado global para pontos manuais
let pontosManuais = [];
let map = null;
let mapInitialized = false;

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
const btnImportarArquivo = document.getElementById('btnImportarArquivo');
const btnGerarMatriz = document.getElementById('btnGerarMatriz');
const btnPlotarProjeto = document.getElementById('btnPlotarProjeto');
const btnGerarKMLManual = document.getElementById('btnGerarKMLManual');
const btnAdicionarPonto = document.getElementById('btnAdicionarPonto');
const fileName = document.getElementById('fileName');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');

// Atualiza nome do arquivo quando selecionado e habilita/desabilita botões
fileInput.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        const fileNameStr = file.name.toLowerCase();
        
        fileName.textContent = `Arquivo selecionado: ${file.name}`;
        
        // Se o arquivo for KML, desabilita botão CSV e habilita botão Gerar Matriz, habilita Plotar Projeto
        if (fileNameStr.endsWith('.kml') || fileNameStr.endsWith('.kmz')) {
            btnImportarArquivo.disabled = true;
            btnGerarMatriz.disabled = false;
            btnPlotarProjeto.disabled = false;
            
            // Desenha automaticamente o KML no mapa
            if (mapInitialized && map) {
                setTimeout(function() {
                    loadKMLOnMap(file);
                }, 300);
            } else {
                // Aguarda o mapa inicializar e depois desenha
                waitForLeaflet(function() {
                    setTimeout(function() {
                        if (!mapInitialized) {
                            initMap();
                        }
                        setTimeout(function() {
                            loadKMLOnMap(file);
                        }, 500);
                    }, 300);
                });
            }
        } else {
            // Se for CSV ou Excel, habilita botão CSV e desabilita botão Gerar Matriz, habilita Plotar Projeto
            btnImportarArquivo.disabled = false;
            btnGerarMatriz.disabled = true;
            btnPlotarProjeto.disabled = false;
        }
    } else {
        fileName.textContent = '';
        btnImportarArquivo.disabled = true;
        btnGerarMatriz.disabled = true;
        btnPlotarProjeto.disabled = false;
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

// Importar KML do arquivo
btnImportarArquivo.addEventListener('click', async function() {
    const file = fileInput.files[0];
    if (!file) {
        showMessage(errorMessage, 'Por favor, selecione um arquivo primeiro.', true);
        btnImportarArquivo.disabled = true;
        return;
    }
    
    // Desabilita o botão durante o processamento
    btnImportarArquivo.disabled = true;

    try {
        let dados = [];

        if (file.name.endsWith('.csv')) {
            // Processa CSV
            if (typeof Papa === 'undefined') {
                showMessage(errorMessage, 'Biblioteca PapaParse não carregada. Verifique os arquivos da aplicação.', true);
                btnImportarArquivo.disabled = false;
                return;
            }
            
            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: function(results) {
                    try {
                        dados = results.data;
                        if (dados.length === 0) {
                            showMessage(errorMessage, 'Arquivo CSV vazio ou formato inválido.', true);
                            // Reabilita o botão em caso de erro
                            btnImportarArquivo.disabled = false;
                            return;
                        }
                        const kmlContent = gerarKML(dados, file.name.replace('.csv', '.kml'));
                        downloadKML(kmlContent, file.name.replace('.csv', '.kml'));
                        showMessage(successMessage, `✅ KML gerado com sucesso! ${dados.length} pontos processados.`);
                        // Desabilita o botão após gerar KML com sucesso (garantir que permaneça desabilitado)
                        btnImportarArquivo.disabled = true;
                        // Força desabilitar novamente após um pequeno delay para garantir
                        setTimeout(function() {
                            btnImportarArquivo.disabled = true;
                            fileInput.value = ''; // Limpa o input para forçar nova seleção
                        }, 500);
                    } catch (e) {
                        showMessage(errorMessage, 'Erro ao processar: ' + e.message, true);
                        btnImportarArquivo.disabled = false;
                    }
                },
                error: function(error) {
                    showMessage(errorMessage, 'Erro ao processar CSV: ' + error.message, true);
                    // Reabilita o botão em caso de erro
                    btnImportarArquivo.disabled = false;
                }
            });
        } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
            // Processa Excel
            if (typeof XLSX === 'undefined') {
                showMessage(errorMessage, 'Biblioteca XLSX não carregada. Verifique os arquivos da aplicação.', true);
                btnImportarArquivo.disabled = false;
                return;
            }
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                    dados = XLSX.utils.sheet_to_json(firstSheet);
                    
                    if (dados.length === 0) {
                        showMessage(errorMessage, 'Arquivo Excel vazio ou formato inválido.', true);
                        // Reabilita o botão em caso de erro
                        btnImportarArquivo.disabled = false;
                        return;
                    }
                    
                    const kmlContent = gerarKML(dados, file.name.replace(/\.(xlsx|xls)$/, '.kml'));
                    downloadKML(kmlContent, file.name.replace(/\.(xlsx|xls)$/, '.kml'));
                    showMessage(successMessage, `✅ KML gerado com sucesso! ${dados.length} pontos processados.`);
                    // Desabilita o botão após gerar KML com sucesso (garantir que permaneça desabilitado)
                    btnImportarArquivo.disabled = true;
                    // Força desabilitar novamente após um pequeno delay para garantir
                    setTimeout(function() {
                        btnImportarArquivo.disabled = true;
                        fileInput.value = ''; // Limpa o input para forçar nova seleção
                    }, 500);
                        } catch (error) {
                            showMessage(errorMessage, 'Erro ao processar Excel: ' + error.message, true);
                            // Reabilita o botão em caso de erro
                            btnImportarArquivo.disabled = false;
                        }
            };
            reader.readAsArrayBuffer(file);
        } else {
            showMessage(errorMessage, 'Formato de arquivo não suportado. Use CSV ou Excel.', true);
            // Reabilita o botão em caso de erro
            btnImportarArquivo.disabled = false;
        }
    } catch (error) {
        showMessage(errorMessage, 'Erro ao processar arquivo: ' + error.message, true);
        // Reabilita o botão em caso de erro
        btnImportarArquivo.disabled = false;
    }
});

// Adicionar ponto manual
btnAdicionarPonto.addEventListener('click', function() {
    const lat = document.getElementById('latitude').value;
    const lon = document.getElementById('longitude').value;
    const sequencia = document.getElementById('sequencia').value || pontosManuais.length + 1;
    const trecho = document.getElementById('trecho').value;
    const numeroPoste = document.getElementById('numeroPoste').value;
    const tipoPoste = document.getElementById('tipoPoste').value;

    if (!lat || !lon) {
        showMessage(errorMessage, 'Por favor, preencha latitude e longitude.', true);
        return;
    }

    const ponto = {
        lat: lat,
        long: lon,
        sequencia: sequencia,
        trecho: trecho,
        numero_poste: numeroPoste,
        tipo_poste: tipoPoste
    };

    pontosManuais.push(ponto);
    btnGerarKMLManual.disabled = false;

    // Limpa campos
    document.getElementById('latitude').value = '';
    document.getElementById('longitude').value = '';
    document.getElementById('sequencia').value = pontosManuais.length + 1;
    document.getElementById('numeroPoste').value = '';
    document.getElementById('tipoPoste').value = '';

    showMessage(successMessage, `✅ Ponto ${sequencia} adicionado! Total: ${pontosManuais.length} pontos.`);
});

// Gerar KML manual
btnGerarKMLManual.addEventListener('click', function() {
    if (pontosManuais.length === 0) {
        showMessage(errorMessage, 'Adicione pelo menos um ponto antes de gerar o KML.', true);
        return;
    }

    const nomeArquivo = document.getElementById('nomeArquivo').value || 'pontos_matriz.kml';
    const kmlContent = gerarKML(pontosManuais, nomeArquivo);
    downloadKML(kmlContent, nomeArquivo);
    showMessage(successMessage, `✅ KML gerado com sucesso! ${pontosManuais.length} pontos exportados.`);
});

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

        // Tenta obter localização do usuário
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    map.setView([position.coords.latitude, position.coords.longitude], 13);
                },
                function() {
                    // Mantém a localização padrão se não conseguir obter
                    console.log('Não foi possível obter a localização do usuário');
                }
            );
        }

        mapInitialized = true;
        console.log('Mapa inicializado com sucesso');
    } catch (error) {
        console.error('Erro ao inicializar o mapa:', error);
        showMessage(errorMessage, 'Erro ao inicializar o mapa: ' + error.message, true);
    }
}

// Inicializa o mapa quando a página carregar e Leaflet estiver pronto
window.addEventListener('load', function() {
    console.log('Página carregada, aguardando Leaflet...');
    waitForLeaflet(function() {
        console.log('Inicializando mapa...');
        setTimeout(initMap, 200); // Pequeno delay para garantir que tudo está pronto
    });
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

// Função para parsear e exibir KML no mapa
function parseAndDisplayKML(kmlText) {
    try {
        console.log('Parseando KML...');
        
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
        
        window.currentMarkers = [];
        window.currentPolylines = [];

        const parser = new DOMParser();
        const kmlDoc = parser.parseFromString(kmlText, 'text/xml');
        
        // Verifica erros de parsing
        const parseError = kmlDoc.querySelector('parsererror');
        if (parseError) {
            throw new Error('Erro ao fazer parse do KML: ' + parseError.textContent);
        }

        const placemarks = kmlDoc.querySelectorAll('Placemark');
        let bounds = [];
        let sequence = 0;

        placemarks.forEach((placemark) => {
            // Processa Point
            const point = placemark.querySelector('Point coordinates');
            if (point) {
                const coords = point.textContent.trim().split(',');
                const lon = parseFloat(coords[0]);
                const lat = parseFloat(coords[1]);
                
                if (!isNaN(lat) && !isNaN(lon)) {
                    const marker = L.marker([lat, lon]).addTo(map);
                    marker.bindPopup(`<strong>Ponto ${sequence + 1}</strong><br>Lat: ${lat.toFixed(6)}<br>Lon: ${lon.toFixed(6)}`);
                    window.currentMarkers.push(marker);
                    bounds.push([lat, lon]);
                    sequence++;
                }
            }

            // Processa LineString
            const lineString = placemark.querySelector('LineString coordinates');
            if (lineString) {
                const coordText = lineString.textContent.trim();
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return [parseFloat(parts[1]), parseFloat(parts[0])];
                }).filter(coord => !isNaN(coord[0]) && !isNaN(coord[1]));
                
                if (coords.length > 0) {
                    const polyline = L.polyline(coords, {
                        color: '#3388ff',
                        weight: 4,
                        opacity: 0.8
                    }).addTo(map);
                    window.currentPolylines.push(polyline);
                    bounds = bounds.concat(coords);
                }
            }

            // Processa Polygon
            const polygon = placemark.querySelector('Polygon outerBoundaryIs LinearRing coordinates');
            if (polygon) {
                const coordText = polygon.textContent.trim();
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return [parseFloat(parts[1]), parseFloat(parts[0])];
                }).filter(coord => !isNaN(coord[0]) && !isNaN(coord[1]));
                
                if (coords.length > 0) {
                    const polygonLayer = L.polygon(coords, {
                        color: '#3388ff',
                        fillColor: '#3388ff',
                        fillOpacity: 0.3,
                        weight: 2
                    }).addTo(map);
                    window.currentPolylines.push(polygonLayer);
                    bounds = bounds.concat(coords);
                }
            }
        });

        // Ajusta o zoom para mostrar todos os elementos
        if (bounds.length > 0) {
            console.log('Ajustando zoom para ' + bounds.length + ' pontos');
            map.fitBounds(bounds, { padding: [50, 50] });
            showMessage(successMessage, `✅ KML carregado no mapa! ${sequence} pontos e ${window.currentPolylines.length} linhas exibidas.`);
        } else {
            console.warn('Nenhum elemento encontrado no KML');
            showMessage(errorMessage, 'Nenhum elemento encontrado no KML.', true);
        }
    } catch (error) {
        console.error('Erro ao processar KML:', error);
        showMessage(errorMessage, 'Erro ao processar KML: ' + error.message, true);
    }
}

// Adiciona evento ao botão Plotar Projeto
btnPlotarProjeto.addEventListener('click', function() {
    console.log('Botão Plotar Projeto clicado');
    const file = fileInput.files[0];
    if (!file) {
        showMessage(errorMessage, 'Por favor, selecione um arquivo primeiro.', true);
        return;
    }
    
    const fileNameStr = file.name.toLowerCase();
    console.log('Arquivo selecionado:', file.name);
    
    if (fileNameStr.endsWith('.kml') || fileNameStr.endsWith('.kmz')) {
        console.log('Carregando KML no mapa...');
        loadKMLOnMap(file);
    } else {
        showMessage(errorMessage, 'Este botão é apenas para arquivos KML/KMZ.', true);
    }
});


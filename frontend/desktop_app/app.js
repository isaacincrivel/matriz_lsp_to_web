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
const btnAbrirTabela = document.getElementById('btnAbrirTabela');
const btnInverterSentido = document.getElementById('btnInverterSentido');
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
        
        // Se o arquivo for KML, desabilita botão CSV e habilita botão Gerar Matriz, habilita Plotar Projeto
        if (fileNameStr.endsWith('.kml') || fileNameStr.endsWith('.kmz')) {
            btnImportarArquivo.disabled = true;
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
                    loadKMLOnMap(file);
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
                                loadKMLOnMap(file);
                            } else {
                                // Se ainda não estiver pronto, tenta novamente
                                setTimeout(function() {
                                    loadKMLOnMap(file);
                                }, 500);
                            }
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

// Event listeners removidos - funcionalidade de entrada manual removida

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

        mapInitialized = true;
        console.log('Mapa inicializado com sucesso');
    } catch (error) {
        console.error('Erro ao inicializar o mapa:', error);
        showMessage(errorMessage, 'Erro ao inicializar o mapa: ' + error.message, true);
    }
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

// Função para criar marcador numerado
function createNumberedMarker(lat, lon, number) {
    const markerIcon = L.divIcon({
        className: 'numbered-marker',
        html: `<div class="marker-number-label">${number}</div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
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
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
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
        window.segmentPolylines = new Map(); // Armazena segmentos individuais por par de vértices (ex: "1-2", "2-3")
        
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

        const parser = new DOMParser();
        const kmlDoc = parser.parseFromString(kmlText, 'text/xml');
        
        // Verifica erros de parsing
        const parseError = kmlDoc.querySelector('parsererror');
        if (parseError) {
            throw new Error('Erro ao fazer parse do KML: ' + parseError.textContent);
        }

        const placemarks = kmlDoc.querySelectorAll('Placemark');
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
        placemarks.forEach((placemark) => {
            const lineString = placemark.querySelector('LineString coordinates');
            if (lineString) {
                const coordText = lineString.textContent.trim();
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return { lat: parseFloat(parts[1]), lon: parseFloat(parts[0]) };
                }).filter(coord => !isNaN(coord.lat) && !isNaN(coord.lon));
                
                coords.forEach(coord => {
                    addVertexIfNew(coord.lat, coord.lon);
                });
            }
        });

        // Depois, processa Polygon
        placemarks.forEach((placemark) => {
            const polygon = placemark.querySelector('Polygon outerBoundaryIs LinearRing coordinates');
            if (polygon) {
                const coordText = polygon.textContent.trim();
                const coords = coordText.split(/\s+/).map(coord => {
                    const parts = coord.split(',');
                    return { lat: parseFloat(parts[1]), lon: parseFloat(parts[0]) };
                }).filter(coord => !isNaN(coord.lat) && !isNaN(coord.lon));
                
                coords.forEach(coord => {
                    addVertexIfNew(coord.lat, coord.lon);
                });
            }
        });

        // Por último, processa Points isolados
        placemarks.forEach((placemark) => {
            const point = placemark.querySelector('Point coordinates');
            if (point) {
                const coords = point.textContent.trim().split(',');
                const lon = parseFloat(coords[0]);
                const lat = parseFloat(coords[1]);
                
                if (!isNaN(lat) && !isNaN(lon)) {
                    addVertexIfNew(lat, lon);
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


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
        
        // Se não há arquivo, reativa modo manual se não houver vértices
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
        window.segmentPolylines = new Map(); // Armazena segmentos individuais por par de vértices (ex: "1-2", "2-3")
        
        // Desativa modo manual quando KML é carregado
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

// Adiciona evento ao botão Finalizar Polilinha
if (btnFinalizarPolilinha) {
    btnFinalizarPolilinha.addEventListener('click', function() {
        console.log('Botão Finalizar Polilinha clicado');
        finalizeManualPolyline();
    });
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
        showMessage(errorMessage, 'Por favor, carregue um arquivo KML ou crie uma polilinha manualmente no mapa.', true);
        return;
    }
    
    // Coleta vértices do KML (formato [[lat, lon, sequencia], ...])
    const vertices = window.kmlVertices.map(v => [v.lat, v.lon, v.number || v.sequencia || v.number]);
    
    // Coleta trecho do arquivo KML (usa nome do arquivo ou padrão)
    const file = fileInput ? fileInput.files[0] : null;
    const trecho = file ? file.name.replace(/\.[^/.]+$/, '') : 'T001';
    
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
        module_name: numeroModuloValue,
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
            if (result.csv_content && result.csv_filename) {
                console.log(`Iniciando download CSV: ${result.csv_filename}`);
                try {
                    const csvDecoded = atob(result.csv_content);
                    const csvBlob = new Blob(['\uFEFF' + csvDecoded], { type: 'text/csv;charset=utf-8;' });
                    downloadFile(csvBlob, result.csv_filename, 'text/csv;charset=utf-8;');
                    console.log(`✅ CSV baixado: ${result.csv_filename}`);
                } catch (e) {
                    console.error('❌ Erro ao baixar CSV:', e);
                    showMessage(errorMessage, `Erro ao baixar CSV: ${e.message}`, true);
                }
            }
            
            // Apenas faz download do KML (não plota no mapa automaticamente)
            // O usuário deve importar manualmente o arquivo se quiser visualizar no mapa
            if (result.kml_content && result.kml_filename) {
                try {
                    const kmlDecoded = atob(result.kml_content);
                    console.log(`KML decodificado: ${kmlDecoded.length} caracteres`);
                    
                    // Faz download do KML (sem atualizar o mapa)
                    setTimeout(() => {
                        try {
                            console.log(`Iniciando download KML: ${result.kml_filename}`);
                            const kmlBlob = new Blob([kmlDecoded], { type: 'application/vnd.google-earth.kml+xml' });
                            downloadFile(kmlBlob, result.kml_filename, 'application/vnd.google-earth.kml+xml');
                            console.log(`✅ KML baixado: ${result.kml_filename}`);
                            console.log(`ℹ️ Para visualizar no mapa, importe o arquivo manualmente`);
                        } catch (e) {
                            console.error('❌ Erro ao baixar KML:', e);
                            showMessage(errorMessage, `Erro ao baixar KML: ${e.message}`, true);
                        }
                    }, 800);
                    
                } catch (e) {
                    console.error('❌ Erro ao processar KML:', e);
                    showMessage(errorMessage, `Erro ao processar KML: ${e.message}`, true);
                }
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


// Configuração e inicialização do AG Grid

// Definir colunas da tabela
const columnDefs = [
    { field: 'sequencia', headerName: 'Sequência', width: 100, filter: 'agNumberColumnFilter', editable: true, sortable: true },
    { field: 'posteDerivacao', headerName: 'Poste Derivação', width: 150, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'estado', headerName: 'Estado', width: 120, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'tensao', headerName: 'Tensão', width: 110, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'local', headerName: 'Local', width: 100, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'tipoRede', headerName: 'Tipo de Rede', width: 180, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'quantidadeFases', headerName: 'Quantidade Fases', width: 180, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'cabo', headerName: 'Cabo', width: 130, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'numeroModulo', headerName: 'Nº Módulo', width: 120, filter: 'agNumberColumnFilter', editable: true, sortable: true },
    { field: 'descricaoModulo', headerName: 'Descrição Módulo', width: 160, filter: 'agTextColumnFilter', editable: true, sortable: true },
    { field: 'numeroPoste', headerName: 'Nº Poste', width: 130, filter: 'agNumberColumnFilter', editable: true, sortable: true },
    { field: 'tipoPoste', headerName: 'Tipo Poste', width: 130, filter: 'agSetColumnFilter', editable: true, sortable: true },
    { field: 'latitude', headerName: 'Latitude', width: 130, filter: 'agNumberColumnFilter', editable: true, sortable: true },
    { field: 'longitude', headerName: 'Longitude', width: 130, filter: 'agNumberColumnFilter', editable: true, sortable: true },
    { field: 'observacoes', headerName: 'Observações', width: 250, filter: 'agTextColumnFilter', editable: true, sortable: true }
];

// Configuração do grid
const gridOptions = {
    columnDefs: columnDefs,
    defaultColDef: {
        resizable: true,
        sortable: true,
        filter: true,
        floatingFilter: true, // Mostra filtro estilo Excel
        editable: true,
        enableCellChangeFlash: true // Destaca células alteradas
    },
    rowData: dadosTabela,
    enableRangeSelection: true,
    enableCharts: false,
    animateRows: true,
    pagination: true,
    paginationPageSize: 50,
    suppressRowClickSelection: false,
    enableCellTextSelection: true,
    ensureDomOrder: true,
    onGridReady: function(params) {
        // Atualizar contador de linhas
        atualizarContador();
        
        // Ajustar tamanho das colunas automaticamente
        params.api.sizeColumnsToFit();
        
        // Event listener para atualizar contador quando filtrar
        params.api.addEventListener('filterChanged', atualizarContador);
        params.api.addEventListener('rowDataUpdated', atualizarContador);
    },
    onCellValueChanged: function(params) {
        console.log('Célula alterada:', params.data);
        // Aqui você pode salvar as alterações em LocalStorage ou IndexedDB
        salvarDados();
    }
};

// Inicializar o grid quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    const gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);
});

// Função para atualizar contador de linhas
function atualizarContador() {
    const totalRows = gridOptions.api.getDisplayedRowCount();
    document.getElementById('totalRows').textContent = totalRows;
}

// Função para salvar dados no LocalStorage
function salvarDados() {
    const dados = [];
    gridOptions.api.forEachNode(function(node) {
        dados.push(node.data);
    });
    localStorage.setItem('tabela_dados', JSON.stringify(dados));
    console.log('Dados salvos no LocalStorage');
}

// Função para exportar CSV
function exportarCSV() {
    gridOptions.api.exportDataAsCsv({
        fileName: 'dados_matriz.csv',
        processCellCallback: function(params) {
            return params.value != null ? params.value : '';
        }
    });
}

// Função para exportar JSON
function exportarJSON() {
    const dados = [];
    gridOptions.api.forEachNode(function(node) {
        dados.push(node.data);
    });
    
    const jsonStr = JSON.stringify(dados, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'dados_matriz.json';
    link.click();
    URL.revokeObjectURL(url);
}

// Carregar dados do LocalStorage se existirem
function carregarDados() {
    const dadosSalvos = localStorage.getItem('tabela_dados');
    if (dadosSalvos) {
        try {
            const dados = JSON.parse(dadosSalvos);
            gridOptions.api.setRowData(dados);
            atualizarContador();
            console.log('Dados carregados do LocalStorage');
            return true; // Retorna true se carregou dados
        } catch (e) {
            console.error('Erro ao carregar dados:', e);
        }
    }
    return false; // Retorna false se não carregou dados
}

// Função para usar dados fictícios como fallback
function usarDadosFicticios() {
    if (dadosTabela && dadosTabela.length > 0) {
        gridOptions.api.setRowData(dadosTabela);
        atualizarContador();
        console.log('Usando dados fictícios de exemplo');
    }
}

// Funções relacionadas a CSV removidas - use apenas os dados em tabela-data.js ou LocalStorage

// Tentar carregar dados quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const carregouDados = carregarDados();
        // Se não carregou dados do LocalStorage, usa dados fictícios
        if (!carregouDados && dadosTabela && dadosTabela.length > 0) {
            gridOptions.api.setRowData(dadosTabela);
            atualizarContador();
            console.log('Usando dados fictícios de exemplo');
        }
    }, 500);
});


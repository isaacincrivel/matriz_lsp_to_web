// csv-generator.js - Geração de CSV no formato compatível com matriz_teste.csv

class CSVGenerator {
    constructor() {
        // Colunas do CSV baseado no formato matriz_teste.csv
        this.columns = [
            'sequencia',
            'status',
            'lat',
            'long',
            'num_poste',
            'tipo_poste',
            'estru_mt_nv1',
            'estru_mt_nv2',
            'estru_mt_nv3',
            'est_bt_nv1',
            'est_bt_nv2',
            'estai_ancora',
            'base_reforcada',
            'base_concreto',
            'aterr_neutro',
            'chave',
            'trafo',
            'equipamento',
            'faixa',
            'cort_arvores_isol',
            'adiconal_1',
            'qdt_adic_1',
            'adiconal_2',
            'qdt_adic_2',
            'adiconal_3',
            'qdt_adic_3',
            'adiconal_4',
            'qdt_adic_4',
            'adiconal_5',
            'qdt_adic_5',
            'adiconal_6',
            'qdt_adic_6',
            'adiconal_7',
            'rotacao_poste',
            'modulo',
            'municipio'
        ];
    }

    // Gera CSV a partir dos dados dos postes
    generateCSV() {
        if (!window.appState || window.appState.postes.length === 0) {
            throw new Error('Nenhum poste para gerar CSV');
        }

        const postes = window.appState.postes;
        const rows = [];

        // Ordena postes por sequência
        const sortedPostes = [...postes].sort((a, b) => (a.sequencia || 0) - (b.sequencia || 0));

        // Para cada poste, cria linhas para cada status
        sortedPostes.forEach((poste) => {
            const sequencia = poste.sequencia;
            const lat = this.formatNumber(poste.lat);
            const lon = this.formatNumber(poste.lon);

            // Status: Implantar
            if (this.hasData(poste.status, 'Implantar')) {
                rows.push(this.createRow(sequencia, 'Implantar', lat, lon, poste.status.Implantar));
            }

            // Status: Existente
            if (this.hasData(poste.status, 'Existente')) {
                rows.push(this.createRow(sequencia, 'Existente', '', '', poste.status.Existente));
            }

            // Status: Retirar
            if (this.hasData(poste.status, 'Retirar')) {
                rows.push(this.createRow(sequencia, 'Retirar', '', '', poste.status.Retirar));
            }

            // Status: deslocar
            if (this.hasData(poste.status, 'deslocar')) {
                rows.push(this.createRow(sequencia, 'deslocar', '', '', poste.status.deslocar));
            }
        });

        // Cria CSV com separador ; e decimal ,
        const csvContent = this.createCSVContent(rows);
        return csvContent;
    }

    // Verifica se há dados para um status
    hasData(posteStatus, statusName) {
        if (!posteStatus || !posteStatus[statusName]) {
            return false;
        }
        
        const statusData = posteStatus[statusName];
        // Verifica se há pelo menos um campo preenchido
        return Object.values(statusData).some(value => 
            value !== null && value !== undefined && value !== '' && String(value).trim() !== ''
        );
    }

    // Cria uma linha do CSV
    createRow(sequencia, status, lat, lon, statusData) {
        const row = {};
        
        // Preenche todas as colunas com vazio
        this.columns.forEach(col => {
            row[col] = '';
        });

        // Preenche dados básicos
        row.sequencia = sequencia;
        row.status = status;
        row.lat = lat;
        row.long = lon;

        // Preenche dados do status
        if (statusData) {
            Object.keys(statusData).forEach(key => {
                if (this.columns.includes(key) && statusData[key]) {
                    row[key] = this.formatValue(statusData[key]);
                }
            });
        }

        return row;
    }

    // Formata valor para CSV (substitui . por , em números)
    formatValue(value) {
        if (value === null || value === undefined) {
            return '';
        }
        
        const strValue = String(value).trim();
        if (strValue === '') {
            return '';
        }
        
        // Se for número, formata com vírgula
        if (!isNaN(strValue) && strValue !== '') {
            return parseFloat(strValue).toString().replace('.', ',');
        }
        
        return strValue;
    }

    // Formata número de coordenada
    formatNumber(num) {
        if (num === null || num === undefined || num === '') {
            return '';
        }
        const numStr = parseFloat(num).toString();
        return numStr.replace('.', ',');
    }

    // Cria conteúdo CSV
    createCSVContent(rows) {
        // Header
        let csv = this.columns.join(';') + '\n';

        // Rows
        rows.forEach(row => {
            const values = this.columns.map(col => {
                const value = row[col] || '';
                // Escapa valores que contêm ; ou quebras de linha
                if (String(value).includes(';') || String(value).includes('\n')) {
                    return `"${String(value).replace(/"/g, '""')}"`;
                }
                return value;
            });
            csv += values.join(';') + '\n';
        });

        return csv;
    }

    // Faz download do CSV
    downloadCSV(filename = 'matriz_teste.csv') {
        try {
            const csvContent = this.generateCSV();
            // Adiciona BOM para UTF-8 (importante para Excel)
            const blob = new Blob(['\ufeff' + csvContent], { 
                type: 'text/csv;charset=utf-8;' 
            });
            saveAs(blob, filename);
            return true;
        } catch (error) {
            console.error('Erro ao gerar CSV:', error);
            throw error;
        }
    }
}

// Exporta para uso global
window.CSVGenerator = CSVGenerator;


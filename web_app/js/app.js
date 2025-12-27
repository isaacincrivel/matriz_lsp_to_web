// app.js - Aplicação principal
const API_URL = "http://127.0.0.1:8001/api/gerar-matriz/";

class App {
    constructor() {
        this.postes = [];
        this.mapController = null;
        this.kmlHandler = null;
        this.csvGenerator = null;
        this.formHandler = null;
        this.addingPoste = false;
        
        this.init();
    }

    init() {
        // Inicializa componentes
        this.mapController = new MapController();
        this.kmlHandler = new KMLHandler(this.mapController);
        this.csvGenerator = new CSVGenerator();
        this.formHandler = new FormHandler();

        // Event listeners
        this.setupEventListeners();

        // Carrega dados salvos (se houver)
        this.loadFromStorage();

        // Torna app acessível globalmente
        window.appState = this;
    }

    setupEventListeners() {
        // Botão importar KML
        const btnImport = document.getElementById('btn-upload');
        if (btnImport) {
            btnImport.addEventListener('click', () => {
                document.getElementById('kml-upload').click();
            });
        }

        // Input de arquivo KML
        const fileInput = document.getElementById('kml-upload');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.importKML(file);
                }
                // Limpa input para permitir selecionar o mesmo arquivo novamente
                e.target.value = '';
            });
        }

        // Botão exportar KML
        const btnExportKML = document.getElementById('btn-export-kml');
        if (btnExportKML) {
            btnExportKML.addEventListener('click', () => {
                this.exportKML();
            });
        }

        // Botão gerar CSV
        const btnExportCSV = document.getElementById('btn-export-csv');
        if (btnExportCSV) {
            btnExportCSV.addEventListener('click', () => {
                this.exportCSV();
            });
        }

        // Botão adicionar poste
        const btnAddPoste = document.getElementById('btn-add-poste');
        if (btnAddPoste) {
            btnAddPoste.addEventListener('click', () => {
                this.addPoste();
            });
        }

        // Botão menu (mobile)
        const btnMenuFab = document.getElementById('btn-menu-fab');
        if (btnMenuFab) {
            btnMenuFab.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Botão fechar sidebar
        const btnCloseSidebar = document.getElementById('btn-close-sidebar');
        if (btnCloseSidebar) {
            btnCloseSidebar.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Atualiza lista de postes quando houver mudanças
        this.updatePostesList();
    }

    // Importa KML
    async importKML(file) {
        try {
            await this.kmlHandler.importKML(file);
            this.showToast('KML importado com sucesso!', 'success');
            this.updatePostesList();
            this.saveToStorage();
        } catch (error) {
            this.showToast('Erro ao importar KML: ' + error.message, 'error');
            console.error(error);
        }
    }

    // Exporta KML
    exportKML() {
        try {
            this.kmlHandler.downloadKML();
            this.showToast('KML exportado com sucesso!', 'success');
        } catch (error) {
            this.showToast('Erro ao exportar KML: ' + error.message, 'error');
            console.error(error);
        }
    }

    // Exporta CSV
    exportCSV() {
        try {
            this.csvGenerator.downloadCSV();
            this.showToast('CSV gerado com sucesso!', 'success');
        } catch (error) {
            this.showToast('Erro ao gerar CSV: ' + error.message, 'error');
            console.error(error);
        }
    }

    // Adiciona novo poste
    addPoste() {
        // Se houver coordenadas do clique no mapa, usa elas
        // Caso contrário, abre formulário vazio
        this.addingPoste = true;
        this.formHandler.openForm();
        this.showToast('Clique no mapa para posicionar o poste, ou preencha as coordenadas manualmente', 'success');
    }



    // Toggle sidebar
    toggleSidebar() {
        const sidebar = document.getElementById('postes-sidebar');
        if (sidebar) {
            sidebar.classList.toggle('open');
        }
    }

    // Adiciona poste ao estado
    addPoste(posteData) {
        // Verifica se já existe poste com essa sequência
        const existing = this.postes.find(p => p.sequencia === posteData.sequencia);
        if (existing) {
            // Atualiza existente
            Object.assign(existing, posteData);
        } else {
            // Adiciona novo
            this.postes.push(posteData);
        }
        this.updatePostesList();
        this.saveToStorage();
    }

    // Atualiza poste existente
    updatePoste(sequence, updates) {
        const poste = this.postes.find(p => p.sequencia === sequence);
        if (poste) {
            Object.assign(poste, updates);
            // Atualiza marcador no mapa
            const marker = this.mapController.getMarkerBySequence(sequence);
            if (marker) {
                marker.data = poste;
            }
            this.updatePostesList();
            this.saveToStorage();
        }
    }

    // Remove poste
    removePoste(sequence) {
        this.postes = this.postes.filter(p => p.sequencia !== sequence);
        this.updatePostesList();
        this.saveToStorage();
    }

    // Obtém próxima sequência
    getNextSequence() {
        if (this.postes.length === 0) {
            return 0;
        }
        const maxSeq = Math.max(...this.postes.map(p => p.sequencia || 0));
        return maxSeq + 1;
    }

    // Atualiza lista de postes na sidebar
    updatePostesList() {
        const listContainer = document.getElementById('postes-list');
        if (!listContainer) return;
        
        if (this.postes.length === 0) {
            listContainer.innerHTML = '<p class="empty-message">Nenhum poste cadastrado ainda.</p>';
            return;
        }

        // Ordena por sequência
        const sortedPostes = [...this.postes].sort((a, b) => (a.sequencia || 0) - (b.sequencia || 0));

        listContainer.innerHTML = sortedPostes.map(poste => {
            const statusCount = poste.status ? Object.keys(poste.status).length : 0;
            return `
                <div class="poste-item" data-sequence="${poste.sequencia}">
                    <div class="poste-item-header">
                        <span class="poste-item-title">Poste #${poste.sequencia}</span>
                        <div class="poste-item-actions">
                            <button class="btn-edit" data-sequence="${poste.sequencia}" title="Editar">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn-delete" data-sequence="${poste.sequencia}" title="Excluir">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                    <div class="poste-item-info">
                        ${poste.lat ? `Lat: ${parseFloat(poste.lat).toFixed(6)}` : ''}<br>
                        ${poste.lon ? `Lon: ${parseFloat(poste.lon).toFixed(6)}` : ''}<br>
                        <small>${statusCount} status cadastrado(s)</small>
                    </div>
                </div>
            `;
        }).join('');

        // Event listeners para botões de editar/excluir
        listContainer.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const sequence = parseInt(e.target.closest('.btn-edit').dataset.sequence);
                const poste = this.postes.find(p => p.sequencia === sequence);
                if (poste) {
                    this.formHandler.openForm(poste, sequence);
                }
            });
        });

        listContainer.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const sequence = parseInt(e.target.closest('.btn-delete').dataset.sequence);
                if (confirm(`Deseja excluir o poste #${sequence}?`)) {
                    this.removePoste(sequence);
                    if (this.mapController) {
                        this.mapController.deletePoste(sequence);
                    }
                }
            });
        });

        // Event listener para clicar no item
        listContainer.querySelectorAll('.poste-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.poste-item-actions')) {
                    const sequence = parseInt(item.dataset.sequence);
                    const poste = this.postes.find(p => p.sequencia === sequence);
                    if (poste && this.mapController) {
                        const marker = this.mapController.getMarkerBySequence(sequence);
                        if (marker) {
                            this.mapController.map.setView(marker.getLatLng(), 18);
                            marker.openPopup();
                        }
                    }
                }
            });
        });
    }

    // Salva dados no localStorage
    saveToStorage() {
        try {
            localStorage.setItem('caminhamento_rede', JSON.stringify(this.postes));
        } catch (error) {
            console.error('Erro ao salvar no localStorage:', error);
        }
    }

    // Carrega dados do localStorage
    loadFromStorage() {
        try {
            const saved = localStorage.getItem('caminhamento_rede');
            if (saved) {
                this.postes = JSON.parse(saved);
                this.updatePostesList();
                
                // Recria marcadores no mapa
                this.postes.forEach(poste => {
                    if (poste.lat && poste.lon && this.mapController) {
                        this.mapController.addMarker(
                            parseFloat(poste.lat),
                            parseFloat(poste.lon),
                            poste.sequencia
                        );
                    }
                });
                
                // Ajusta zoom
                if (this.postes.length > 0) {
                    setTimeout(() => {
                        this.mapController.fitBounds();
                    }, 500);
                }
            }
        } catch (error) {
            console.error('Erro ao carregar do localStorage:', error);
        }
    }

    // Mostra toast notification
    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Inicializa aplicação quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});


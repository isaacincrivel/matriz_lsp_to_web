// form-handler.js - Manipulação de formulários

class FormHandler {
    constructor() {
        this.modal = document.getElementById('modal-poste');
        this.form = document.getElementById('form-poste');
        this.currentSequence = null;
        this.currentStatus = 'Implantar';
        
        this.init();
    }

    init() {
        // Event listeners para tabs de status
        const statusTabs = document.querySelectorAll('.status-tab');
        statusTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchStatus(e.target.dataset.status);
            });
        });

        // Event listeners do formulário
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Botões de fechar
        document.getElementById('btn-close-modal').addEventListener('click', () => this.close());
        document.getElementById('btn-cancel-poste').addEventListener('click', () => this.close());

        // Fecha modal ao clicar fora
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });
    }

    // Abre formulário para editar/criar poste
    openForm(posteData = null, sequence = null) {
        this.currentSequence = sequence;
        this.currentStatus = 'Implantar';
        
        // Atualiza título do modal
        const title = document.getElementById('modal-title');
        if (sequence !== null) {
            title.textContent = `Editar Poste #${sequence}`;
        } else {
            title.textContent = 'Adicionar Poste';
        }

        // Preenche formulário se houver dados
        if (posteData) {
            this.fillForm(posteData);
        } else {
            this.clearForm();
        }

        // Ativa tab Implantar
        this.switchStatus('Implantar');

        // Mostra modal
        this.modal.classList.add('active');
    }

    // Preenche formulário com dados
    fillForm(posteData) {
        // Preenche coordenadas
        document.getElementById('poste-lat').value = posteData.lat || '';
        document.getElementById('poste-lon').value = posteData.lon || '';
        document.getElementById('poste-sequencia').value = posteData.sequencia || '';

        // Preenche dados de cada status
        if (posteData.status) {
            Object.keys(posteData.status).forEach(statusName => {
                const statusData = posteData.status[statusName];
                Object.keys(statusData).forEach(field => {
                    const input = document.getElementById(`${field}_${statusName.toLowerCase()}`);
                    if (input) {
                        input.value = statusData[field] || '';
                    }
                });
            });
        }
    }

    // Limpa formulário
    clearForm() {
        this.form.reset();
        document.getElementById('poste-id').value = '';
        document.getElementById('poste-lat').value = '';
        document.getElementById('poste-lon').value = '';
        document.getElementById('poste-sequencia').value = '';
    }

    // Troca de tab de status
    switchStatus(statusName) {
        this.currentStatus = statusName;

        // Atualiza tabs
        document.querySelectorAll('.status-tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.status === statusName) {
                tab.classList.add('active');
            }
        });

        // Atualiza painéis
        document.querySelectorAll('.status-panel').forEach(panel => {
            panel.classList.remove('active');
            if (panel.dataset.status === statusName) {
                panel.classList.add('active');
            }
        });
    }

    // Manipula submit do formulário
    handleSubmit(e) {
        e.preventDefault();

        // Coleta dados do formulário
        const formData = this.collectFormData();

        // Valida dados
        if (!this.validateForm(formData)) {
            this.showToast('Preencha pelo menos um campo para o status atual', 'error');
            return;
        }

        // Salva dados
        if (window.appState) {
            if (this.currentSequence !== null) {
                // Atualiza poste existente
                window.appState.updatePoste(this.currentSequence, formData);
            } else {
                // Cria novo poste
                const sequence = window.appState.getNextSequence();
                formData.sequencia = sequence;
                
                // Se não tiver coordenadas, tenta obter do mapa
                if (!formData.lat || !formData.lon) {
                    if (window.mapController && window.mapController.map) {
                        const center = window.mapController.map.getCenter();
                        formData.lat = center.lat;
                        formData.lon = center.lng;
                    }
                }
                
                window.appState.addPoste(formData);
                
                // Adiciona marcador no mapa se não existir
                if (window.mapController && formData.lat && formData.lon) {
                    window.mapController.addMarker(
                        parseFloat(formData.lat),
                        parseFloat(formData.lon),
                        sequence
                    );
                }
            }
        }

        this.showToast('Poste salvo com sucesso!', 'success');
        this.close();
    }

    // Coleta dados do formulário
    collectFormData() {
        const data = {
            lat: document.getElementById('poste-lat').value,
            lon: document.getElementById('poste-lon').value,
            sequencia: document.getElementById('poste-sequencia').value || this.currentSequence,
            status: {}
        };

        // Coleta dados de cada status
        const statuses = ['Implantar', 'Existente', 'Retirar', 'deslocar'];
        
        statuses.forEach(statusName => {
            const statusData = {};
            const panel = document.querySelector(`.status-panel[data-status="${statusName}"]`);
            
            if (panel) {
                const inputs = panel.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    const name = input.name;
                    if (name && name.endsWith(`_${statusName.toLowerCase()}`)) {
                        const fieldName = name.replace(`_${statusName.toLowerCase()}`, '');
                        const value = input.value.trim();
                        if (value) {
                            statusData[fieldName] = value;
                        }
                    }
                });
            }

            // Só adiciona se houver dados
            if (Object.keys(statusData).length > 0) {
                data.status[statusName] = statusData;
            }
        });

        return data;
    }

    // Valida formulário
    validateForm(formData) {
        // Verifica se há pelo menos um status com dados
        if (!formData.status || Object.keys(formData.status).length === 0) {
            return false;
        }

        // Verifica se o status atual tem dados
        if (!formData.status[this.currentStatus]) {
            return false;
        }

        return true;
    }

    // Fecha modal
    close() {
        this.modal.classList.remove('active');
        this.currentSequence = null;
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

// Exporta para uso global
window.FormHandler = FormHandler;


# 🗺️ Sistema Matriz CSV to KML

Sistema completo para processamento de matrizes CSV e geração/visualização de arquivos KML com interface web e desktop.

## 📁 Estrutura do Projeto

```
matriz_csv_to_kml/
├── backend/              # Backend Python
│   ├── core/            # Módulos principais (cálculos, processamento)
│   ├── exportacao/      # Exportação KML/CSV
│   ├── elementos/       # Elementos KML específicos
│   ├── abacos/          # Tabelas e cálculos de ábacos
│   └── django/          # Views Django (opcional)
│
├── frontend/            # Aplicações Frontend
│   ├── desktop_app/     # Aplicação Desktop (principal) ⭐
│   └── standalone/      # Versões standalone
│
├── data/                # Dados
│   ├── input/           # Arquivos de entrada
│   └── output/          # Resultados gerados
│
├── backup/              # Backups
├── docs/                # Documentação
└── scripts/             # Scripts utilitários
```

## 🚀 Início Rápido

### Frontend (Aplicação Desktop)

1. Navegue até: `frontend/desktop_app/`
2. Abra `index.html` no navegador
   - Ou use servidor local: `python -m http.server 8000`
   - Acesse: `http://localhost:8000/`

### Backend Python

```python
from backend.core.matriz_csv_to_kml import gerar_matriz
# Use as funções conforme necessário
```

## 📚 Documentação

- [Estrutura de Organização](ESTRUTURA_ORGANIZACAO.md)
- [Guia de Depuração](frontend/desktop_app/DEBUG.md)
- [Importar KML](docs/README_IMPORTAR_KML.md)

## 🔧 Tecnologias

- **Backend**: Python, Pandas
- **Frontend**: HTML, CSS, JavaScript, Leaflet
- **Formato**: CSV, Excel, KML

## 📝 Licença

Projeto privado/proprietário.


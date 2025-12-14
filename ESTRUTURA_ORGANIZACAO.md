# 📁 Estrutura Proposta de Organização do Projeto

## 🎯 Estrutura Sugerida

```
matriz_csv_to_kml/
│
├── 📂 backend/                    # Backend Python - Lógica de Negócio
│   ├── 📂 core/                   # Módulos principais
│   │   ├── calculo_geografico.py  # Cálculos geográficos
│   │   ├── processamento_vertices.py
│   │   ├── transformacao_csv.py
│   │   └── matriz_csv_to_kml.py   # Função principal
│   │
│   ├── 📂 exportacao/             # Exportação de dados
│   │   ├── exportacao.py          # Exportar KML
│   │   └── kml.py                 # Utilitários KML
│   │
│   ├── 📂 elementos/              # Elementos KML específicos
│   │   ├── kml_elementos.py
│   │   ├── colocar_encabecamento_rede.py
│   │   ├── colocar_poste_estrutura.py
│   │   └── marcar_vertices_angulo_deflexao.py
│   │
│   ├── 📂 abacos/                 # Tabelas e ábacos
│   │   ├── abaco_mosaico.py
│   │   └── TABELA ABACOS.xlsx
│   │
│   └── 📂 django/                 # Views Django (se necessário)
│       ├── views_kml.py
│       └── views_matriz.py
│
├── 📂 frontend/                   # Aplicações Frontend
│   ├── 📂 desktop_app/            # Aplicação Desktop (principal)
│   │   ├── index.html
│   │   ├── app.js
│   │   ├── libs/
│   │   ├── README.md
│   │   └── DEBUG.md
│   │
│   ├── 📂 web_app/                # Aplicação Web (coleta campo)
│   │   ├── index.html
│   │   ├── css/
│   │   ├── js/
│   │   └── README.md
│   │
│   └── 📂 standalone/             # Versões standalone
│       └── importar_kml.html
│
├── 📂 data/                       # Dados e Arquivos de Entrada
│   ├── 📂 input/                  # Arquivos de entrada (exemplos)
│   │   ├── matriz_teste.csv
│   │   ├── matriz_teste_transformada.csv
│   │   └── matriz_teste_transformada_final.csv
│   │
│   └── 📂 output/                 # Resultados gerados
│       └── resultados/            # (mantém pasta existente)
│
├── 📂 backup/                     # Backups e Versões Antigas
│   └── BKP/                       # (move conteúdo de BKP/)
│
├── 📂 docs/                       # Documentação
│   ├── ANALISE_ADAPTACAO_SISTEMA.md
│   ├── README_IMPORTAR_KML.md
│   └── ESTRUTURA_ORGANIZACAO.md   # Este arquivo
│
├── 📂 scripts/                    # Scripts utilitários
│   └── download-libs.ps1          # (mover de desktop_app)
│
├── .gitignore
└── README.md                      # README principal do projeto

```

## 🔄 Mudanças Propostas

### 1. Backend Python
- Todos os módulos Python em `backend/`
- Organizados por funcionalidade (core, exportacao, elementos, abacos)

### 2. Frontend
- Todas as aplicações web em `frontend/`
- Separadas por tipo (desktop_app, web_app, standalone)

### 3. Dados
- Arquivos de entrada em `data/input/`
- Resultados em `data/output/`

### 4. Backup
- Backups em `backup/`

### 5. Documentação
- Toda documentação em `docs/`

## ✅ Vantagens

1. ✅ Separação clara de responsabilidades
2. ✅ Fácil encontrar arquivos
3. ✅ Manutenção simplificada
4. ✅ Estrutura profissional
5. ✅ Pronto para crescimento


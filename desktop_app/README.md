# 📦 Desktop App - Sistema de Importação KML

## 📋 Preparação para Build

Esta pasta contém os arquivos preparados para criar um aplicativo desktop.

### Estrutura de Arquivos

```
desktop_app/
├── index.html          # Interface HTML principal
├── app.js              # Código JavaScript da aplicação
├── libs/               # Bibliotecas JavaScript (serão baixadas)
│   ├── papaparse.min.js
│   ├── FileSaver.min.js
│   └── xlsx.full.min.js
└── README.md           # Este arquivo
```

## 🔧 Download das Bibliotecas

Para preparar o app desktop, você precisa baixar as bibliotecas JavaScript:

### Opção 1: Download Manual

1. **PapaParse** (v5.4.1):
   - URL: https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js
   - Salvar em: `libs/papaparse.min.js`

2. **FileSaver.js** (v2.0.5):
   - URL: https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js
   - Salvar em: `libs/FileSaver.min.js`

3. **XLSX.js** (v0.18.5):
   - URL: https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js
   - Salvar em: `libs/xlsx.full.min.js`

### Opção 2: Script de Download (PowerShell)

Execute o script `download-libs.ps1` se fornecido.

## 🚀 Próximos Passos

Após baixar as bibliotecas, você pode:

1. **Testar localmente**: Abra `index.html` no navegador
2. **Criar app Electron**: Usar Electron para criar executável .exe
3. **Criar app PyQt**: Usar Python + PyQt para criar executável
4. **Ofuscar código**: Minificar/ofuscar JavaScript antes do build

## 🔒 Proteção de Código

Para proteger o código:

1. **Minificar JS**: Use ferramentas como UglifyJS ou Terser
2. **Ofuscar JS**: Use javascript-obfuscator
3. **Empacotar**: Use ASAR (Electron) ou PyInstaller (Python)

## 📝 Notas

- O código está separado em `app.js` para facilitar minificação/ofuscação
- As bibliotecas estão em arquivos separados para permitir atualização independente
- Para máxima proteção, considere embutir tudo inline no HTML durante o build


# 🚀 Sistema de Importação KML - Guia de Uso

## 📋 Descrição

Sistema simples e direto para importar/gerar arquivos KML a partir de dados CSV/Excel ou entrada manual.

## 🎯 Como Usar

### Opção 1: Abrir a Página HTML

1. Abra o arquivo `importar_kml.html` no seu navegador
2. Não é necessário instalar nada - funciona direto no navegador!

### Opção 2: Usar com Servidor Local (Recomendado)

Para evitar problemas de CORS, use um servidor local simples:

**Python 3:**
```bash
python -m http.server 8000
```

**Node.js (com http-server):**
```bash
npx http-server
```

Depois acesse: `http://localhost:8000/importar_kml.html`

## ✨ Funcionalidades

### 📁 Importação de Arquivo

1. Clique em "Clique para selecionar ou arraste o arquivo aqui"
2. Selecione um arquivo **CSV** ou **Excel** (.xlsx, .xls)
3. Clique em "Importar KML do Arquivo"
4. O arquivo KML será baixado automaticamente!

### ✏️ Entrada Manual

1. Preencha os campos:
   - **Nome do Arquivo KML**: Nome do arquivo que será gerado
   - **Latitude**: Coordenada de latitude (Ex: -17.041935)
   - **Longitude**: Coordenada de longitude (Ex: -49.224541)
   - **Sequência**: Número sequencial do ponto
   - **Trecho**: Identificação do trecho (Ex: T001)
   - **Número do Poste**: Opcional
   - **Tipo de Poste**: Opcional (Ex: N3, DT10/300)

2. Clique em "➕ Adicionar Ponto" para adicionar mais pontos
3. Clique em "📥 Gerar e Baixar KML" quando terminar

## 📊 Formato do CSV/Excel

O arquivo deve conter as seguintes colunas (nomes podem variar):

| Coluna | Obrigatório | Exemplo |
|--------|-------------|---------|
| lat / latitude | ✅ Sim | -17.041935 |
| long / lon / longitude | ✅ Sim | -49.224541 |
| sequencia | ❌ Não | 1 |
| trecho | ❌ Não | T001 |
| numero_poste / num_poste | ❌ Não | 46464546 |
| tipo_poste | ❌ Não | N3 |

### Exemplo de CSV:

```csv
lat,long,sequencia,trecho,numero_poste,tipo_poste
-17.041935,-49.224541,1,T001,46464546,N3
-17.042000,-49.224600,2,T001,,DT10/300
-17.042100,-49.224700,3,T001,,
```

**Nota:** O sistema aceita vírgula (`,`) ou ponto e vírgula (`;`) como separador.

## 🎨 Características

- ✅ Interface simples e intuitiva
- ✅ Funciona totalmente no navegador (sem servidor necessário)
- ✅ Suporta CSV e Excel
- ✅ Entrada manual de dados
- ✅ Download automático do KML gerado
- ✅ Visualização de mensagens de sucesso/erro
- ✅ Design moderno e responsivo

## 📱 Compatibilidade

- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Navegadores móveis

## 🔧 Requisitos

Nenhum! O sistema funciona completamente no navegador e carrega todas as bibliotecas necessárias automaticamente:
- PapaParse (para CSV)
- XLSX.js (para Excel)
- FileSaver.js (para download)

## 💡 Dicas

1. **CSV com vírgula decimal**: O sistema aceita tanto `.` quanto `,` como separador decimal
2. **Nomes de colunas**: O sistema reconhece variações como `lat`/`Lat`/`latitude`
3. **Múltiplos pontos**: Adicione quantos pontos quiser na entrada manual
4. **Postes vs Pontos**: Pontos com `numero_poste` aparecem como "Poste" no KML, outros como "Ponto"

## 🐛 Problemas Comuns

**Erro ao processar CSV:**
- Verifique se o arquivo não está vazio
- Confirme que as colunas `lat` e `long` existem
- Tente abrir o arquivo em um editor de texto para verificar o formato

**KML não é gerado:**
- Certifique-se de que pelo menos um ponto foi adicionado
- Verifique se as coordenadas são válidas (números)

**Arquivo não baixa:**
- Verifique as configurações de bloqueio de pop-ups do navegador
- Alguns navegadores podem pedir permissão para baixar

## 📞 Suporte

Para problemas ou dúvidas, verifique:
1. O console do navegador (F12) para mensagens de erro
2. O formato do arquivo CSV/Excel
3. Se todas as colunas obrigatórias estão presentes


# 🔗 Funções Relacionadas ao `dados_gerar_matriz.json`

Este documento explica todas as funções que se relacionam com o arquivo `dados_gerar_matriz.json`.

---

## 📄 Estrutura do Arquivo JSON

O arquivo `dados_gerar_matriz.json` contém todos os parâmetros necessários para chamar a função `gerar_matriz`:

```json
{
  "trecho": "TESTEXXyx.kml",
  "module_name": "10105",
  "module_data": { ... },
  "loose_gap": "NÃO",
  "section_size": 80,
  "gap_size": 700,
  "num_poste_inicial": "00000000",
  "tipo_poste": "",
  "lista_nao_intercalar": [7],
  "vertices": [[lat, lon, sequencia], ...]
}
```

---

## 🔧 Funções que LÊM o arquivo JSON

### 1. **`executar_gerar_matriz.py` → `main()`**

**Localização:** `backend/core/executar_gerar_matriz.py`

**Função:** Lê o arquivo `dados_gerar_matriz.json` e executa `gerar_matriz()` com os dados do arquivo.

**Como usar:**
```bash
python backend/core/executar_gerar_matriz.py dados_gerar_matriz.json
```

**O que faz:**
1. Abre e lê o arquivo JSON
2. Extrai todos os parâmetros (trecho, module_name, module_data, etc.)
3. Valida os parâmetros obrigatórios (module_name, vertices)
4. Chama a função `gerar_matriz()` com os parâmetros
5. Salva o resultado em `temp_matriz_resultado.json`

**Código relevante:**
```python
# Linha 24-26: Lê o arquivo JSON
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)

# Linha 67-78: Chama gerar_matriz
matriz = gerar_matriz(
    trecho=trecho,
    module_name=module_name,
    module_data=module_data,
    loose_gap=loose_gap,
    section_size=section_size,
    gap_size=gap_size,
    num_poste_inicial=num_poste_inicial,
    tipo_poste=tipo_poste,
    lista_nao_intercalar=lista_nao_intercalar,
    vertices_kml=vertices
)
```

---

## 📝 Funções que GERAM/ESCREVEM o arquivo JSON

### 2. **`app.js` → `gerarMatriz()`** (Frontend - JavaScript)

**Localização:** `frontend/desktop_app/app.js` (função foi removida, mas estava lá)

**Função:** Coletava dados do formulário HTML e gerava o arquivo JSON quando havia erro de rede.

**O que fazia:**
- Coletava parâmetros do formulário HTML
- Em caso de erro de conexão com a API, salvava os dados em `dados_gerar_matriz.json`
- Permitia depuração/execução manual posterior

**Nota:** Esta função foi removida recentemente do código. Mas era responsável por criar o arquivo quando havia problemas de comunicação com o servidor.

---

## 🎯 Função Principal que USA os dados do JSON

### 3. **`matriz_csv_to_kml.py` → `gerar_matriz()`**

**Localização:** `backend/core/matriz_csv_to_kml.py` (linha 21)

**Assinatura:**
```python
def gerar_matriz(trecho, module_name, module_data, loose_gap, section_size, 
                 gap_size, num_poste_inicial, tipo_poste, lista_nao_intercalar, 
                 vertices_kml=None):
```

**Função:** Esta é a função principal que processa todos os parâmetros e gera a matriz final.

**Parâmetros recebidos (do JSON):**
- `trecho`: Código do trecho (ex: "TESTEXXyx.kml")
- `module_name`: Nome do módulo (ex: "10105")
- `module_data`: Dicionário com dados do módulo (código, descrição, tensão, etc.)
- `loose_gap`: "SIM" ou "NÃO" para vão frouxo
- `section_size`: Vão médio (ex: 80)
- `gap_size`: Tramo máximo (ex: 700)
- `num_poste_inicial`: Número do poste inicial (sempre "00000000")
- `tipo_poste`: "Implantar" ou "Existente"
- `lista_nao_intercalar`: Lista de índices onde não intercalar postes
- `vertices_kml`: Lista de vértices [[lat, lon, sequencia], ...]

**O que faz:**
1. Processa os vértices do KML
2. Aplica vão frouxo (se necessário)
3. Divide o vão em tramos menores
4. Marca vértices com ângulo de deflexão
5. Aplica encabeçamento automático
6. Intercala postes entre vértices
7. Coloca postes e estruturas em cada vértice
8. Retorna um DataFrame pandas com a matriz completa

---

## 🧪 Funções de TESTE que usam dados similares

### 4. **`matriz_csv_to_kml.py` → `testar_gerar_matriz()`**

**Localização:** `backend/core/matriz_csv_to_kml.py` (linha 408)

**Função:** Função de teste que simula dados de entrada (similar ao JSON).

**O que faz:**
- Usa dados fixos (hardcoded) similares ao JSON
- Permite depuração linha por linha usando `pdb.set_trace()`
- Não lê o arquivo JSON diretamente, mas usa os mesmos valores

**Dados simulados (linha 458-476):**
```python
module_name = "10105"
module_data = {
    "codigo_modulo": "10105",
    "descrição_modulo": "Construção - 13,8kV - Rural - MONOF - Cabo 1/0CAA - Pecuária",
    ...
}
```

---

## 🌐 Funções de API que RECEBEM dados do JSON

### 5. **`views_matriz_direct.py` → `gerar_matriz_direct()`** (Django)

**Localização:** `backend/django/views_matriz_direct.py` (linha 16)

**Função:** Endpoint de API Django que recebe JSON via POST e chama `gerar_matriz()`.

**O que faz:**
- Recebe requisição POST com JSON no corpo
- Extrai parâmetros do JSON
- Chama `gerar_matriz()` com os parâmetros
- Retorna resultado em JSON

**Parâmetros esperados (mesmos do JSON):**
- trecho, module_name, module_data, loose_gap, section_size, gap_size, etc.

---

### 6. **`views_matriz.py` → `gerar_matriz_view()`** (Django - versão antiga)

**Localização:** `backend/django/views_matriz.py` (linha 113)

**Função:** Endpoint de API Django alternativo (versão mais antiga).

**Diferença:** Usa estrutura de parâmetros ligeiramente diferente.

---

## 📊 Funções Internas chamadas por `gerar_matriz()`

Quando `gerar_matriz()` é chamada com os dados do JSON, ela internamente chama:

### 7. **`get_loose_gap()`** 
**Localização:** `backend/core/processamento_vertices.py`
- Processa vão frouxo baseado em `loose_gap`

### 8. **`dividir_tramo()`**
**Localização:** `backend/core/processamento_vertices.py`
- Divide tramos baseado em `section_size`

### 9. **`marcar_vertices_angulo_deflexao()`**
**Localização:** `backend/elementos/marcar_vertices_angulo_deflexao.py`
- Marca vértices com ângulo de deflexão baseado em `gap_size` e `module_name`

### 10. **`colocar_encabecamento_rede()`**
**Localização:** `backend/elementos/colocar_encabecamento_rede.py`
- Aplica encabeçamento automático

### 11. **`intercalar_vertices()`**
**Localização:** `backend/core/processamento_vertices.py`
- Intercala postes baseado em `lista_nao_intercalar` e `gap_size`

### 12. **`colocar_poste_estrutura()`**
**Localização:** `backend/elementos/colocar_poste_estrutura.py`
- Coloca postes e estruturas baseado em `loose_gap`, `tipo_poste` e `module_name`

---

## 🔄 Fluxo Completo

```
┌─────────────────────────────────────┐
│  dados_gerar_matriz.json            │
│  (arquivo JSON com parâmetros)      │
└──────────────┬──────────────────────┘
               │
               │ lê
               ▼
┌─────────────────────────────────────┐
│  executar_gerar_matriz.py           │
│  → main()                           │
│  → extrai parâmetros do JSON        │
└──────────────┬──────────────────────┘
               │
               │ chama
               ▼
┌─────────────────────────────────────┐
│  matriz_csv_to_kml.py               │
│  → gerar_matriz()                   │
│  → processa todos os dados          │
└──────────────┬──────────────────────┘
               │
               │ chama internamente
               ▼
┌─────────────────────────────────────┐
│  Funções auxiliares:                │
│  - get_loose_gap()                  │
│  - dividir_tramo()                  │
│  - marcar_vertices_angulo_deflexao()│
│  - intercalar_vertices()            │
│  - colocar_poste_estrutura()        │
└──────────────┬──────────────────────┘
               │
               │ retorna
               ▼
┌─────────────────────────────────────┐
│  DataFrame pandas com matriz final  │
└─────────────────────────────────────┘
```

---

## 💡 Como Usar o Arquivo JSON

### Para depuração/teste:
```bash
# 1. Certifique-se de que o arquivo dados_gerar_matriz.json existe
# 2. Execute:
python backend/core/executar_gerar_matriz.py dados_gerar_matriz.json

# 3. O resultado será salvo em temp_matriz_resultado.json
```

### Para depuração linha por linha:
```python
# 1. Abra backend/core/matriz_csv_to_kml.py
# 2. Descomente a linha ~39: import pdb; pdb.set_trace()
# 3. Execute:
python backend/core/executar_gerar_matriz.py dados_gerar_matriz.json
# 4. Use comandos do PDB: n (next), s (step), c (continue), q (quit)
```

---

## 📋 Resumo das Funções

| Função | Localização | Tipo | Descrição |
|--------|-------------|------|-----------|
| `main()` | `executar_gerar_matriz.py` | Leitor | Lê JSON e chama gerar_matriz |
| `gerar_matriz()` | `matriz_csv_to_kml.py` | Principal | Processa todos os dados |
| `testar_gerar_matriz()` | `matriz_csv_to_kml.py` | Teste | Função de teste com dados fixos |
| `gerar_matriz_direct()` | `views_matriz_direct.py` | API | Endpoint Django que recebe JSON |
| `gerar_matriz_view()` | `views_matriz.py` | API | Endpoint Django alternativo |
| `get_loose_gap()` | `processamento_vertices.py` | Auxiliar | Processa vão frouxo |
| `dividir_tramo()` | `processamento_vertices.py` | Auxiliar | Divide tramos |
| `marcar_vertices_angulo_deflexao()` | `marcar_vertices_angulo_deflexao.py` | Auxiliar | Marca ângulos de deflexão |
| `intercalar_vertices()` | `processamento_vertices.py` | Auxiliar | Intercala postes |
| `colocar_poste_estrutura()` | `colocar_poste_estrutura.py` | Auxiliar | Coloca postes e estruturas |

---

## 🔍 Verificação

Para verificar quais funções ainda referenciam o arquivo:
```bash
# Procura por referências ao arquivo
grep -r "dados_gerar_matriz" .

# Ou use o find do Windows PowerShell
Get-ChildItem -Recurse -Include *.py,*.js | Select-String "dados_gerar_matriz"
```


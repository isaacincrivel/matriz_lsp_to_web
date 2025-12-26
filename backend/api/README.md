# 🌐 API Flask - Sistema Matriz

API REST para gerar matrizes CSV/KML usando o backend Python.

## 🚀 Como Iniciar o Servidor

### Windows
```bash
# Opção 1: Execute o script batch
backend\api\start_server.bat

# Opção 2: Execute diretamente
python backend\api\server_flask.py
```

### Linux/Mac
```bash
# Opção 1: Execute o script shell
chmod +x backend/api/start_server.sh
./backend/api/start_server.sh

# Opção 2: Execute diretamente
python3 backend/api/server_flask.py
```

O servidor vai procurar uma porta disponível entre 8000-8009.

## 📡 Endpoints

### GET `/api/test/`
Testa se o servidor está funcionando.

**Resposta:**
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

### POST `/api/gerar-matriz/`
Gera matriz CSV/KML a partir dos parâmetros fornecidos.

**Body (JSON):**
```json
{
  "trecho": "T001",
  "module_name": "10105",
  "module_data": {
    "codigo_modulo": "10105",
    "descrição_modulo": "...",
    "vao_medio": 80,
    "tramo_max": 700,
    ...
  },
  "loose_gap": "NÃO",
  "section_size": 80,
  "gap_size": 700,
  "num_poste_inicial": "00000000",
  "tipo_poste": "Existente",
  "lista_nao_intercalar": [7],
  "vertices": [[lat, lon, sequencia], ...]
}
```

**Resposta (sucesso):**
```json
{
  "success": true,
  "message": "Matriz gerada com sucesso! X registros.",
  "data": [...],  // Array com dados da matriz
  "csv_content": "...",  // Base64
  "csv_filename": "T001_matriz_resultado.csv",
  "kml_content": "...",  // Base64
  "kml_filename": "T001_quadrados_bissetriz.kml",
  "total_records": 50
}
```

**Resposta (erro):**
```json
{
  "success": false,
  "message": "Erro ao gerar matriz: ...",
  "traceback": "..."
}
```

## 📋 Dependências

```bash
pip install flask flask-cors pandas
```

## 🔧 Configuração

O servidor automaticamente:
- Procura porta disponível entre 8000-8009
- Habilita CORS para requisições do frontend
- Retorna arquivos CSV e KML em base64

## 🌐 Frontend

O frontend em `frontend/desktop_app/` automaticamente detecta a porta do servidor ao fazer requisições.


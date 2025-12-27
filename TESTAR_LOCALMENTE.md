# 🧪 Como Testar a Aplicação Localmente

## 📋 Pré-requisitos

- Python 3.11 instalado
- Navegador web (Chrome, Firefox, Edge, etc.)

---

## 🚀 Passo 1: Instalar Dependências

### Windows (PowerShell ou CMD):

```powershell
# Navegue até a pasta do projeto
cd C:\matriz_csv_to_kml

# Instale as dependências
pip install -r requirements.txt
```

**Ou instale manualmente:**
```powershell
pip install flask flask-cors pandas gunicorn lxml openpyxl
```

### Linux/Mac:

```bash
cd /caminho/para/matriz_csv_to_kml
pip3 install -r requirements.txt
```

---

## 🚀 Passo 2: Iniciar o Backend (Servidor Flask)

### Opção A: Usando Script (Windows) ✅ RECOMENDADO

1. **Clique duas vezes em:**
   ```
   backend\api\start_server.bat
   ```

2. **Ou execute no PowerShell:**
   ```powershell
   .\backend\api\start_server.bat
   ```

### Opção B: Executar Diretamente (Windows)

```powershell
cd C:\matriz_csv_to_kml
python backend\api\server_flask.py
```

### Opção C: Linux/Mac

```bash
cd /caminho/para/matriz_csv_to_kml
chmod +x backend/api/start_server.sh
./backend/api/start_server.sh
```

**Ou:**
```bash
python3 backend/api/server_flask.py
```

---

## ✅ Verificar se o Backend Está Funcionando

Após iniciar, você deve ver:

```
================================================================================
🚀 Servidor Flask iniciando...
================================================================================
🔧 Modo: DESENVOLVIMENTO
📡 API disponível em: http://0.0.0.0:8000/api/gerar-matriz/
🧪 Teste: http://0.0.0.0:8000/api/test/
================================================================================
Pressione Ctrl+C para parar o servidor
================================================================================
```

### Testar no Navegador:

Abra o navegador e acesse:
```
http://localhost:8000/api/test/
```

**Deve retornar:**
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

**Se funcionar, o backend está OK! ✅**

---

## 🌐 Passo 3: Abrir o Frontend

### Opção A: Abrir Diretamente no Navegador

1. **Navegue até:**
   ```
   frontend\desktop_app\index.html
   ```

2. **Clique duas vezes** ou **arraste para o navegador**

3. A aplicação deve abrir!

### Opção B: Usar Servidor HTTP Local (Recomendado)

**Por que usar servidor HTTP?**
- Evita problemas de CORS
- Simula ambiente de produção

#### Windows (PowerShell):

```powershell
cd C:\matriz_csv_to_kml\frontend\desktop_app
python -m http.server 3000
```

Acesse: `http://localhost:3000`

#### Linux/Mac:

```bash
cd frontend/desktop_app
python3 -m http.server 3000
```

---

## 🔧 Passo 4: Verificar Conexão Frontend → Backend

O frontend (`app.js`) **detecta automaticamente** o backend nas portas 8000-8004.

**Se o backend estiver rodando na porta 8000, o frontend vai encontrar automaticamente!**

### Como Verificar:

1. Abra o **Console do Navegador** (F12)
2. Procure por mensagens como:
   ```
   ✅ Servidor encontrado na porta 8000
   ```
   ou
   ```
   ✅ Modo PRODUÇÃO - Usando: http://localhost:8000/api/gerar-matriz/
   ```

---

## 🧪 Passo 5: Testar Funcionalidade Completa

### 1. Testar Importação de KML/CSV

1. No frontend, clique em **"Escolher arquivo"**
2. Selecione um arquivo KML ou CSV
3. Clique em **"Importar Arquivo"**
4. Verifique se aparece no mapa

### 2. Testar Geração de Matriz

1. Preencha os campos do formulário
2. Clique em **"Gerar Matriz"**
3. Verifique o console do navegador (F12) para ver:
   - Se encontrou o servidor
   - Se fez a requisição para a API
   - Se recebeu resposta

### 3. Verificar Logs do Backend

No terminal onde o Flask está rodando, você verá:
```
[API] Gerando matriz para trecho: T001, módulo: 10105
[API] Vértices recebidos: 10
[API] ✅ Matriz gerada com 50 registros
```

---

## 🐛 Troubleshooting

### Problema: "Nenhuma porta disponível entre 8000-8009"

**Solução:**
- Feche outros programas que usam essas portas
- Ou defina uma porta específica:
  ```powershell
  $env:PORT=8000
  python backend\api\server_flask.py
  ```

### Problema: Frontend não encontra o backend

**Solução:**
1. Verifique se o backend está rodando (veja terminal)
2. Teste no navegador: `http://localhost:8000/api/test/`
3. Abra o console do navegador (F12) e veja os logs
4. O frontend procura nas portas 8000-8004 automaticamente

### Problema: Erro de CORS

**Solução:**
- Use um servidor HTTP para o frontend (Opção B do Passo 3)
- O Flask já tem CORS habilitado para desenvolvimento

### Problema: "ModuleNotFoundError: No module named 'backend'"

**Solução:**
- Certifique-se de estar na pasta raiz do projeto
- Execute: `python backend\api\server_flask.py` (não `python backend/api/server_flask.py` de dentro da pasta backend)

---

## 📝 Resumo Rápido

### 1. Instalar dependências:
```powershell
pip install -r requirements.txt
```

### 2. Iniciar backend:
```powershell
.\backend\api\start_server.bat
```

### 3. Abrir frontend:
- Opção A: Clique duas vezes em `frontend\desktop_app\index.html`
- Opção B: `cd frontend\desktop_app && python -m http.server 3000`

### 4. Testar:
- Backend: `http://localhost:8000/api/test/`
- Frontend: `http://localhost:3000` (se usou servidor HTTP)

---

## ✅ Checklist de Teste

- [ ] Backend iniciou sem erros
- [ ] `http://localhost:8000/api/test/` retorna JSON
- [ ] Frontend abriu no navegador
- [ ] Console do navegador mostra "Servidor encontrado"
- [ ] Consegue importar arquivo KML/CSV
- [ ] Consegue gerar matriz
- [ ] Download de CSV/KML funciona

---

**Agora você pode testar tudo localmente antes de fazer deploy! 🚀**


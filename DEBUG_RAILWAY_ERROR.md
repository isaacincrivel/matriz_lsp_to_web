# 🔍 Debug: Erro no Railway

## ❓ Qual Erro Está Acontecendo?

Para diagnosticar, preciso saber:

1. **Tipo de erro:**
   - Build falha?
   - Container crasha após iniciar?
   - API não responde?

2. **Onde aparece:**
   - Railway → Deployments → Build Logs?
   - Railway → Deployments → View Logs (runtime)?

3. **Mensagem de erro:**
   - Copie a mensagem exata do erro

---

## 🔍 Verificação Rápida - Problemas Comuns

### ✅ 1. Dockerfile Está Correto?

**Verificar:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD gunicorn backend.api.server_flask:app --bind 0.0.0.0:5000 --workers 2 --timeout 120
```

**Status:** ✅ Verificado - Está correto

---

### ✅ 2. Builder Está Configurado?

**Railway → Service → Settings → Build:**
- Builder: `Dockerfile`
- Dockerfile path: `Dockerfile`

**Ação:** Verificar no Dashboard

---

### ✅ 3. Porta Está Correta?

**Dockerfile:** `--bind 0.0.0.0:5000`
**Railway Networking:** Target Port = `5000`

**Status:** ✅ Verificado - Está correto

---

### ✅ 4. Variável app Existe?

**Arquivo:** `backend/api/server_flask.py`
**Linha 22:** `app = Flask(__name__)`

**Status:** ✅ Verificado - Existe

---

### ✅ 5. Dependências Estão Instaladas?

**requirements.txt:**
- flask>=2.3.0
- flask-cors>=4.0.0
- pandas>=2.0.0
- gunicorn>=21.2.0
- lxml>=4.9.0
- openpyxl>=3.1.0

**Status:** ✅ Verificado - Todas presentes

---

## 🎯 Problemas Específicos e Soluções

### Problema 1: Build Falha

**Sintomas:**
- Build Logs mostram erro
- Não chega ao runtime

**Possíveis causas:**
- Falha ao instalar dependências (lxml, pandas)
- Erro no Dockerfile

**Solução:**
Verificar Build Logs e procurar por:
- `Failed building wheel for lxml`
- `ModuleNotFoundError`
- `ImportError`

---

### Problema 2: Container Crasha Após Iniciar

**Sintomas:**
- Build completa
- Container inicia
- Depois aparece: `Exited with code 1`

**Possíveis causas:**
- Gunicorn não encontra `app`
- Erro ao importar módulos
- Porta incorreta

**Solução:**
Verificar Runtime Logs (View Logs) e procurar por:
- `ModuleNotFoundError`
- `ImportError`
- `Failed to find application object 'app'`

---

### Problema 3: API Não Responde

**Sintomas:**
- Container rodando
- Mas `/api/test/` não responde

**Possíveis causas:**
- Porta incorreta
- Public Networking desligado
- Rota não registrada

**Solução:**
- Verificar Target Port = 5000
- Verificar Public Networking = ENABLED
- Testar URL: `https://www.matrizsistema.com.br/api/test/`

---

### Problema 4: Erro "Railpack"

**Sintomas:**
- Logs mostram "Railpack" ou "Nixpacks"
- Não usa Dockerfile

**Solução:**
- Railway → Settings → Build → Builder = `Dockerfile`
- Salvar manualmente
- Fazer novo deploy

---

## 📋 Informações Necessárias para Debug

**Para diagnosticar, preciso:**

1. **Últimas 30-50 linhas do Build Logs:**
   - Railway → Deployments → Último Deployment → Build Logs
   - Copiar últimas linhas

2. **Últimas 30-50 linhas do Runtime Logs:**
   - Railway → Deployments → Último Deployment → View Logs
   - Copiar últimas linhas

3. **Status do Deploy:**
   - SUCCESS ou FAILED?

4. **O que acontece ao acessar:**
   - `https://www.matrizsistema.com.br/api/test/`
   - Qual erro aparece?

---

## 🔧 Checklist de Verificação

### No Railway Dashboard:

- [ ] **Builder está como Dockerfile?**
  - Settings → Build → Builder = `Dockerfile`

- [ ] **Start Command está vazio?**
  - Settings → Deploy → Start Command = vazio

- [ ] **Target Port está como 5000?**
  - Networking → Public Networking → Target Port = `5000`

- [ ] **Public Networking está ENABLED?**
  - Networking → Public Networking = ENABLED

- [ ] **Build completou?**
  - Deployments → Último Deployment → Status = SUCCESS?

- [ ] **Container está rodando?**
  - Deployments → View Logs → Procurar "Listening at"

---

## 🎯 Próximos Passos

1. **Verificar Build Logs:**
   - Railway → Deployments → Build Logs
   - Copiar últimas 30-50 linhas

2. **Verificar Runtime Logs:**
   - Railway → Deployments → View Logs
   - Copiar últimas 30-50 linhas

3. **Testar URL:**
   - Acessar: `https://www.matrizsistema.com.br/api/test/`
   - Ver o que aparece

4. **Enviar informações:**
   - Status do deploy
   - Últimas linhas dos logs
   - Erro específico que aparece

---

**Preciso das informações acima para diagnosticar o erro específico!**


# 🚀 Deploy Rápido - Sistema Matriz

## Opção Mais Rápida: Railway ou Render

### ⚡ Railway (Recomendado)

1. **Acesse:** https://railway.app
2. **Crie conta** (pode usar GitHub)
3. **"New Project" → "Deploy from GitHub repo"**
4. **Selecione seu repositório**
5. **Railway detecta Python automaticamente**
6. **Configure:**
   - **Start Command:** `gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT`
   - **Healthcheck:** `/api/test/`

7. **Domínio:**
   - Railway gera um domínio grátis: `seu-app.up.railway.app`
   - Para domínio customizado: Settings → Networking → Custom Domain

### ⚡ Render

1. **Acesse:** https://render.com
2. **"New" → "Web Service"**
3. **Conecte repositório GitHub**
4. **Configure:**
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT`

5. **Domínio:**
   - Render gera: `seu-app.onrender.com`
   - Custom domain em Settings

---

## ✅ Arquivos Necessários (já criados)

✅ `requirements.txt` - Dependências Python
✅ `Procfile` - Comando para Heroku
✅ `runtime.txt` - Versão do Python
✅ `backend/api/server_flask.py` - Já configurado para produção

---

## 🔧 Atualizar Frontend para Produção

Edite `frontend/desktop_app/app.js`:

**Opção 1: Detectar automaticamente (recomendado)**
```javascript
// Substitua a parte que procura servidor:
const API_BASE_URL = window.location.origin + '/api';

// Ou configure manualmente:
// const API_BASE_URL = 'https://seu-app.up.railway.app/api';
```

**Opção 2: Modificar a busca de porta**

Procure esta parte no `app.js`:
```javascript
const PORTS = [8000, 8001, 8002, 8003, 8004];
```

E adicione antes:
```javascript
// Detecta se está em produção (usando HTTPS ou domínio customizado)
const isProduction = window.location.protocol === 'https:' || 
                     window.location.hostname !== 'localhost' && 
                     window.location.hostname !== '127.0.0.1';

if (isProduction) {
    // Em produção, usa o mesmo domínio
    API_URL = `${window.location.origin}/api/gerar-matriz/`;
} else {
    // Em desenvolvimento, procura porta local
    // ... código existente ...
}
```

---

## 📝 Passo a Passo Completo (Railway)

### 1. Preparar Repositório

```bash
# No seu projeto local
git add requirements.txt Procfile runtime.txt
git commit -m "Preparar para deploy"
git push origin main
```

### 2. Deploy no Railway

1. Acesse https://railway.app
2. Login com GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecione seu repositório
5. Railway vai detectar Python e instalar dependências

### 3. Configurar Variáveis (se necessário)

No Railway Dashboard → Variables:
- `PYTHONPATH` = `/app` (pode ser necessário)
- `FLASK_ENV` = `production`

### 4. Obter URL

Railway gera automaticamente: `https://seu-app.up.railway.app`

### 5. Testar

Acesse: `https://seu-app.up.railway.app/api/test/`

Deve retornar:
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando"
}
```

### 6. Atualizar Frontend

Se você vai servir o frontend separadamente, atualize o `app.js`:

```javascript
const API_BASE_URL = 'https://seu-app.up.railway.app/api';
```

Ou se o frontend está no mesmo servidor, use:
```javascript
const API_BASE_URL = window.location.origin + '/api';
```

---

## 🌐 Configurar Domínio Personalizado

### No Railway:

1. Settings → Networking
2. "Custom Domain"
3. Adicione seu domínio: `www.seudominio.com.br`
4. Railway mostrará as configurações DNS:
   - Tipo: CNAME
   - Nome: www
   - Valor: seu-app.up.railway.app

### No Provedor de DNS (ex: Registro.br, GoDaddy):

1. Acesse painel de DNS
2. Adicione registro CNAME:
   - Nome: www
   - Valor: seu-app.up.railway.app
   - TTL: 3600

3. Para domínio raiz (sem www):
   - Alguns provedores suportam ALIAS/ANAME
   - Ou use redirecionamento 301

Aguarde propagação DNS (pode levar até 48h, geralmente < 1h).

---

## 🎯 Próximos Passos

1. ✅ Escolha Railway ou Render
2. ✅ Faça deploy seguindo os passos acima
3. ✅ Teste a API: `/api/test/`
4. ✅ Configure domínio customizado
5. ✅ Atualize frontend para usar URL de produção
6. ✅ Teste completo do sistema

**Tempo estimado:** 10-15 minutos para deploy básico!

---

## 🐛 Troubleshooting

### Erro: "Module not found"
- Verifique se `requirements.txt` tem todas as dependências
- Veja os logs do Railway para erros de instalação

### Erro: "Application error"
- Verifique os logs no Railway Dashboard
- Confirme que o comando start está correto

### CORS bloqueando requisições
- Atualize CORS no `server_flask.py` para permitir seu domínio
- Ou use `CORS(app)` temporariamente para testar

### Frontend não encontra API
- Verifique se a URL no `app.js` está correta
- Confirme que o servidor está respondendo em `/api/test/`


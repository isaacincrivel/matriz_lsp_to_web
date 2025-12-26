# 🔧 Fix: Error creating build plan with Railpack

## Problema
Railway mostra: "Error creating build plan with Railpack"

## ✅ Solução Aplicada

### 1. Simplificação do nixpacks.toml
Removida a fase `[phases.build]` que pode estar causando conflito.

### 2. Start Command Explícito
Adicionado `startCommand` no `railway.json` para garantir.

### 3. No Railway Dashboard

**IMPORTANTE:** Siga estes passos na ordem:

1. **Settings → Build & Deploy**
2. **Configure manualmente:**
   - **Builder:** `NIXPACKS`
   - **Build Command:** *(deixe vazio)*
   - **Start Command:** `gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **Clear Build Cache** (obrigatório!)
   - Settings → Build & Deploy → **Clear Build Cache**

4. **Novo Deploy**
   - Deployments → **Redeploy**

## 🔍 Se Ainda Não Funcionar

### Verifique os Logs do Build:
1. Deployments → Último deploy
2. Procure por:
   - Mensagens sobre `requirements.txt`
   - Erros de sintaxe do `nixpacks.toml`
   - Erros de detecção de linguagem

### Alternativa: Usar Dockerfile

Se o Nixpacks continuar falhando, podemos criar um Dockerfile. Mas tente primeiro:

### Verificar Arquivos no GitHub:
Acesse seu repositório e confirme que na **raiz** existem:
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `nixpacks.toml`
- ✅ `railway.json`

## 🎯 Próximos Passos

1. Limpe o cache no Railway
2. Configure Start Command manualmente
3. Faça novo deploy
4. Verifique os logs

Se persistir, me envie os logs completos do build!


# 🔧 Fix: Error creating build plan with Railpack

## Problema
Railway mostra: "Railpack could not determine how to build the app" ou "Script start.sh not found"

## ✅ Solução - Opção 1: Usar Dockerfile (RECOMENDADO AGORA)

**Criado `Dockerfile` como solução mais confiável.**

### No Railway Dashboard:

1. **Settings → Build & Deploy**
2. **Configure:**
   - **Builder:** `DOCKERFILE` (ou `Docker`)
   - **Dockerfile Path:** `Dockerfile` (ou deixe vazio se estiver na raiz)
   - **Start Command:** *(deixe vazio - usa CMD do Dockerfile)*

3. **Clear Build Cache**
   - Settings → Build & Deploy → **Clear Build Cache**

4. **Novo Deploy**
   - Deployments → **Redeploy**

## ✅ Solução - Opção 2: Usar Nixpacks (se Dockerfile não funcionar)

1. **Settings → Build & Deploy**
2. **Configure:**
   - **Builder:** `NIXPACKS`
   - **Build Command:** *(deixe vazio)*
   - **Start Command:** `gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **Clear Build Cache**
4. **Novo Deploy**

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


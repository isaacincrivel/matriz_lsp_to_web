# 🔧 Correção do Deploy no Railway

## Problema
O Railway não está detectando automaticamente que este é um projeto Python Flask, pois encontra arquivos Python antigos na raiz do repositório.

## ✅ Solução Implementada

### Arquivos Criados
- ✅ `build.sh` - Script de build explícito para Railway
- ✅ `start.sh` - Script de start explícito para Railway
- ✅ `nixpacks.toml` - Configuração do builder Nixpacks
- ✅ `railway.json` - Configuração do Railway
- ✅ `.railwayignore` - Ignora arquivos Python da raiz durante o build

### 1. Configuração Automática

Os arquivos acima foram commitados e enviados. O Railway deve detectar automaticamente:

- **Build Command:** `bash build.sh` (via `railway.json`)
- **Start Command:** `bash start.sh` (via `railway.json`)

### 2. Se o Railway não detectar automaticamente

No Railway Dashboard:

1. **Settings → Build & Deploy**
2. **Configure manualmente:**

   **Builder:** `Nixpacks`
   
   **Build Command:**
   ```
   bash build.sh
   ```
   
   **Start Command:**
   ```
   bash start.sh
   ```

### 3. Limpar Cache (Importante!)

**SEMPRE faça isso após mudanças:**
1. **Settings → Build & Deploy**
2. Clique em **"Clear Build Cache"**
3. Faça um novo deploy

### 4. Variáveis de Ambiente

No Railway Dashboard → Variables:
- `PORT` - será configurado automaticamente pelo Railway
- `ALLOWED_ORIGINS` (opcional) - domínios permitidos para CORS

### 5. Verificar logs

Se o erro persistir, verifique os logs no Railway:
- **Deployments** → Clique no deploy → **Ver logs completos**
- Procure por erros específicos

## 📋 Checklist

- [ ] `requirements.txt` está na raiz
- [ ] `Procfile` está na raiz
- [ ] `runtime.txt` está na raiz (Python 3.9)
- [ ] `railway.json` existe
- [ ] `nixpacks.toml` existe
- [ ] Build Command configurado no Railway
- [ ] Start Command configurado no Railway
- [ ] Sem arquivos Python duplicados na raiz

## 🔍 Troubleshooting

**Erro: "Could not determine how to build"**
→ Verifique se `requirements.txt` está na raiz do repositório

**Erro: "Module not found"**
→ Verifique se todas as dependências estão em `requirements.txt`

**Erro: "Port already in use"**
→ Use `$PORT` no comando de start (já está no Procfile)

**Erro: "Command not found: gunicorn"**
→ Adicione `gunicorn` no `requirements.txt` (já está)


# 🔧 Forçar Dockerfile no Railway Dashboard

## ⚠️ Problema

O Railway ainda mostra `"builder": "RAILPACK"` mesmo após atualizar o `railway.json`.

**Isso significa:** O Railway Dashboard está usando uma configuração diferente do arquivo do repositório.

---

## ✅ Solução: Atualizar Manualmente no Dashboard

O `railway.json` do repositório pode não estar sendo sincronizado automaticamente com o Dashboard. Você precisa atualizar manualmente.

---

## 🎯 Passo a Passo

### PASSO 1: Abrir Configurações do Service

1. **Acesse:** https://railway.app
2. **Seu Projeto** → **Environment**
3. **Selecione o Service** (`matriz_csv_to_kml`)
4. **Settings** (ícone de engrenagem ⚙️)

---

### PASSO 2: Configurar Build

1. **Settings** → **Build**

2. **Verificar e configurar:**
   - **Builder:** Mude para `Dockerfile` (se estiver como `Railpack`)
   - **Dockerfile Path:** `Dockerfile`
   - **Build Command:** Deixe **VAZIO**
   - **Custom Start Command:** Deixe **VAZIO**

3. **CLIQUE EM "SAVE" ou "UPDATE"** ← **CRÍTICO!**

---

### PASSO 3: Verificar Root Directory (Opcional)

1. **Settings** → **General**
2. **Root Directory:**
   - Deve estar como `.` (ponto) ou **VAZIO**
   - Se estiver como `backend` ou `backend/api`, mude para `.`
3. **CLIQUE EM "SAVE"**

---

### PASSO 4: Fazer Novo Deploy

1. **Deployments** → **Deploy** ou **Redeploy**
2. Ou faça um commit vazio:
   ```bash
   git commit --allow-empty -m "Force Railway to use Dockerfile"
   git push
   ```

---

## 🔍 Verificação

Após configurar, os **Build Logs** devem mostrar:

```
Detected Dockerfile
Building image with BuildKit...
Step 1/6 : FROM python:3.11-slim
...
```

**NÃO deve mostrar:**
- ❌ "Railpack"
- ❌ "Script start.sh not found"
- ❌ "Railpack could not determine how to build"

---

## ⚠️ Por Que Isso Acontece?

O Railway pode ter duas configurações:

1. **railway.json** (no repositório) - pode não estar sendo usado
2. **Configuração do Dashboard** - esta é a que realmente importa

**O Dashboard sempre tem prioridade!**

---

## ✅ Resumo

**Ação necessária:**
1. Railway Dashboard → Service → Settings → Build
2. Mudar Builder para `Dockerfile`
3. Salvar
4. Fazer novo deploy
5. Verificar logs

**O arquivo railway.json local está correto, mas o Dashboard precisa ser atualizado manualmente!**


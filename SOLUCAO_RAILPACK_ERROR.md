# 🔧 Solução: Erro Railpack no Railway

## ❌ Problema

Railway continua tentando usar Railpack:
```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

---

## ✅ Ações Realizadas

### 1. Atualizado railway.json

**Mudanças:**
- Adicionado `dockerfilePath: "Dockerfile"` explicitamente
- Adicionado `startCommand: ""` vazio para evitar conflito

### 2. Renomeados Arquivos que Podem Causar Conflito

- `start.sh` → `start.sh.backup` (renomeado)
- `build.sh` → `build.sh.backup` (renomeado)

**Por quê:**
- Railway pode procurar por `start.sh` quando detecta Railpack
- Renomear evita que Railway tente usá-los

---

## 🎯 AÇÃO CRÍTICA: Configurar Manualmente no Dashboard

**O Railway Dashboard PRECISA ser configurado manualmente!**

### Passo a Passo:

1. **Abrir Railway Dashboard:**
   - Acesse: https://railway.app
   - Selecione seu projeto

2. **Selecionar o Service correto:**
   - Railway → Environment → Selecione o service `matriz_csv_to_kml`

3. **Configurar Build:**
   - Railway → Service → **Settings** → **Build**
   - **Builder:** Mude para `Dockerfile` (se estiver como "Railpack" ou "Nixpacks")
   - **Dockerfile Path:** `Dockerfile`
   - **Build Command:** Deixe VAZIO
   - **Clique em "Save" ou "Update"**

4. **Configurar Deploy:**
   - Railway → Service → **Settings** → **Deploy**
   - **Start Command:** Deixe VAZIO (limpe se tiver algo)
   - **Custom Start Command:** Deixe VAZIO
   - **Clique em "Save" ou "Update"**

5. **Limpar Build Cache:**
   - Railway → Service → **Settings** → **Build**
   - Procure por "Clear Build Cache" ou "Delete Cache"
   - Clique para limpar

6. **Fazer Novo Deploy:**
   - Railway → **Deployments**
   - Clique em "Deploy" ou "Redeploy"
   - Ou faça novo commit (git push)

---

## 🔍 Verificação

### Após Configurar, Verifique os Logs:

**Build Logs devem mostrar:**
```
Detected Dockerfile
Building image using BuildKit...
Step 1/6 : FROM python:3.11-slim
```

**NÃO deve mostrar:**
- ❌ "Railpack"
- ❌ "Nixpacks"
- ❌ "Script start.sh not found"

---

## ⚠️ Se Ainda Não Funcionar

### Opção 1: Deletar e Recriar o Service

1. Railway → Service → Settings → **Delete Service**
2. Criar novo service
3. Conectar ao mesmo repositório
4. Configurar Builder = Dockerfile desde o início

### Opção 2: Verificar Múltiplos Serviços

1. Railway → Environment
2. Veja se há múltiplos services
3. Se houver, delete os que não usa
4. Ou configure cada um para usar Dockerfile

---

## ✅ Resumo

**Arquivos alterados:**
- ✅ `railway.json` - Atualizado com dockerfilePath explícito
- ✅ `start.sh` - Renomeado para `start.sh.backup`
- ✅ `build.sh` - Renomeado para `build.sh.backup`

**Ação necessária:**
- ⚠️ **CONFIGURAR MANUALMENTE NO RAILWAY DASHBOARD**
- ⚠️ Builder = Dockerfile
- ⚠️ Start Command = vazio
- ⚠️ Limpar build cache

---

**O problema está no Railway Dashboard! Configure manualmente o Builder como Dockerfile.**


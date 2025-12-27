# 🚨 CONFIGURAÇÃO MANUAL OBRIGATÓRIA - Railway Dashboard

## ⚠️ O PROBLEMA

O Railway **AINDA está usando Railpack** mesmo após as correções. Isso significa que **você precisa mudar manualmente no Dashboard**.

## 📸 O que você está vendo:

```
Build > Build image: FAILED
Error creating build plan with Railpack
```

Isso confirma que o Railway está usando **NIXPACKS/RAILPACK** ao invés de **DOCKERFILE**.

---

## ✅ SOLUÇÃO: Configurar no Dashboard

### Passo 1: Acesse Settings
1. No Railway Dashboard
2. Clique no seu projeto/serviço
3. Vá em **Settings** (ícone de engrenagem)

### Passo 2: Build & Deploy
1. No menu lateral, clique em **"Build & Deploy"**
2. Você verá uma seção **"Build"**

### Passo 3: Mudar o Builder ⚠️ CRÍTICO
1. Encontre o campo **"Builder"** ou **"Build Command"**
2. Você verá opções como:
   - `NIXPACKS` (selecionado atualmente ❌)
   - `DOCKERFILE` 
   - `DOCKER`
   - Outras opções...

3. **MUDE PARA:** `DOCKERFILE` ou `DOCKER`

### Passo 4: Dockerfile Path (se aparecer)
1. Campo **"Dockerfile Path"** ou **"Dockerfile"**
2. Deixe **VAZIO** ou coloque: `Dockerfile`
3. Não coloque caminho relativo se estiver na raiz

### Passo 5: Limpar Build/Start Commands
1. **Build Command:** Deixe **VAZIO**
2. **Start Command:** Deixe **VAZIO** (o Dockerfile já tem CMD)

### Passo 6: Limpar Cache
1. Procure por **"Clear Build Cache"** ou **"Clear Cache"**
2. Clique e aguarde a confirmação

### Passo 7: Salvar e Deploy
1. Clique em **"Save"** ou **"Update"**
2. Vá em **Deployments**
3. Clique em **"Redeploy"** ou **"Deploy"**

---

## 🔍 Onde encontrar no Dashboard?

### Opção A: Settings → Build & Deploy
```
Dashboard → Seu Projeto → Settings → Build & Deploy
  └─ Builder: [mudar para DOCKERFILE]
  └─ Dockerfile Path: [vazio ou Dockerfile]
  └─ Build Command: [VAZIO]
  └─ Start Command: [VAZIO]
```

### Opção B: Service Settings
Alguns projetos têm configuração em:
```
Dashboard → Service → Settings → Build
```

### Opção C: Via Railway CLI (alternativa)
Se o Dashboard não funcionar, pode tentar via CLI:
```bash
railway link
railway variables set RAILWAY_BUILDER=DOCKERFILE
```

---

## ✅ Como saber que funcionou?

### Logs devem mostrar:
```
Step 1/6 : FROM python:3.11-slim
Step 2/6 : WORKDIR /app
Step 3/6 : RUN apt-get update...
...
Successfully built [hash]
```

### NÃO deve aparecer:
- ❌ "Railpack" ou "Nixpacks"
- ❌ "Error creating build plan with Railpack"
- ❌ "Script start.sh not found"

---

## 🆘 Se não encontrar a opção Builder

### Verifique:
1. **Tipo de Serviço:** Certifique-se que é um serviço de deploy (não banco de dados)
2. **Plano:** Algumas configurações só aparecem em planos pagos
3. **Versão do Railway:** Interface pode variar

### Alternativa: Criar novo serviço
Se não conseguir mudar, pode ser necessário:
1. Criar um **novo serviço** no mesmo projeto
2. Conectar ao mesmo repositório GitHub
3. Configurar **DOCKERFILE desde o início**

---

## 📝 Checklist Visual

No Dashboard, você deve ver:

```
Settings → Build & Deploy

Builder: [DOCKERFILE ▼]  ← MUDAR AQUI
Dockerfile Path: [        ]  ← VAZIO ou Dockerfile
Build Command: [          ]  ← VAZIO
Start Command: [          ]  ← VAZIO

[Clear Build Cache]  ← CLICAR
[Save/Update]        ← SALVAR
```

---

## 🎯 IMPORTANTE

**O `railway.json` sozinho NÃO é suficiente!**
Você **PRECISA** configurar manualmente no Dashboard do Railway.

O `railway.json` ajuda, mas o Railway prioriza a configuração do Dashboard quando há conflito.

---

**Após fazer essas mudanças, faça um novo deploy e me avise o resultado!**


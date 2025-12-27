# 🔧 Forçar Railway a Usar Dockerfile

## ❌ Problema

Railway ainda está tentando usar Railpack ao invés do Dockerfile:
```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

---

## ✅ Solução: Forçar Dockerfile Explicitamente

### 1. Atualizar railway.json

O Railway precisa de configuração mais explícita para usar Dockerfile.

---

### 2. Verificar Arquivos que Podem Causar Conflito

Arquivos que podem fazer Railway usar Railpack:
- ❌ `Procfile` (já renomeado para `Procfile.backup` ✅)
- ❌ `nixpacks.toml`
- ❌ `Railway.toml`
- ❌ Configuração no Dashboard forçando Railpack

---

## 🎯 Ações Necessárias

### No Railway Dashboard (CRÍTICO):

1. **Railway → Service → Settings → Build:**
   - **Builder:** Mude manualmente para `Dockerfile`
   - **Dockerfile Path:** `Dockerfile`
   - **Build Command:** Deixe VAZIO
   - **Salvar**

2. **Railway → Service → Settings → Deploy:**
   - **Start Command:** Deixe VAZIO
   - **Custom Start Command:** Deixe VAZIO
   - **Salvar**

3. **Se houver múltiplos serviços:**
   - Verifique CADA serviço
   - Todos devem usar Dockerfile

4. **Limpar build cache:**
   - Railway → Deployments → Settings → Clear Build Cache
   - Ou deletar e recriar o service

---

## 🔧 Solução Alternativa: Usar Variável de Ambiente

Se Railway continuar usando Railpack, podemos forçar via variável de ambiente.

---

**O problema está no Railway Dashboard, não no código! Você precisa configurar manualmente o Builder como Dockerfile.**


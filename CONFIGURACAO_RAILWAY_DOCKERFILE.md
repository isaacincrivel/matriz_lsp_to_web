# 🐳 Configuração Railway - Usando Dockerfile

## ✅ Decisão: Manter Dockerfile

Escolhemos usar **Dockerfile** ao invés de Procfile/Nixpacks para ter mais controle sobre o build.

---

## 📋 Configuração Atual

### Arquivos:

- ✅ **`Dockerfile`** - Usado para build
- ✅ **`railway.json`** - Configurado para `builder: DOCKERFILE`
- ✅ **`Procfile.backup`** - Renomeado (não usado, mas mantido como backup)
- ✅ **`requirements.txt`** - Na raiz (necessário)
- ✅ **`runtime.txt`** - Especifica Python 3.11

---

## 🔧 Railway Dashboard - Configuração Necessária

### Settings → Build:

1. **Builder:** `DOCKERFILE` ✅
2. **Dockerfile Path:** `Dockerfile` (ou vazio para auto-detecção)
3. **Build Command:** *(vazio)*
4. **Start Command:** *(vazio - Dockerfile já tem CMD)*

---

## 📊 Dockerfile

**Comando de start:**
```dockerfile
CMD gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Vantagens:**
- ✅ Instala `gcc` (necessário para algumas dependências Python)
- ✅ Build completo e isolado
- ✅ Mais controle sobre ambiente
- ✅ Reproduzível

---

## 🚀 Logs Esperados no Railway

### Build bem-sucedido:
```
Step 1/6 : FROM python:3.11-slim
Step 2/6 : WORKDIR /app
Step 3/6 : RUN apt-get update...
Step 4/6 : COPY requirements.txt .
Step 5/6 : RUN pip install...
Step 6/6 : COPY . .
Successfully built [hash]
```

### Deploy bem-sucedido:
```
Starting container...
Starting gunicorn...
Listening on 0.0.0.0:$PORT
```

---

## ⚠️ Importante

### Não deve aparecer:
- ❌ "Railpack" ou "Nixpacks"
- ❌ "Script start.sh not found"
- ❌ "Railpack could not determine how to build"

### Se aparecer:
1. Verificar Railway Dashboard → Settings → Build → Builder = `DOCKERFILE`
2. Garantir que está salvo
3. Fazer novo deploy

---

## 🔄 Se Precisar Voltar para Procfile

1. Renomear: `Procfile.backup` → `Procfile`
2. Railway Dashboard → Settings → Build → Builder = `NIXPACKS`
3. Remover/renomear `Dockerfile`

---

**Configuração concluída! Railway vai usar Dockerfile para build e deploy.**


# 📁 Configurar Root Directory no Railway

## ✅ Resposta Rápida

**Root Directory deve estar VAZIO ou `./` (raiz do repositório)**

---

## 🔍 Por quê?

### Estrutura do Projeto:
```
matriz_csv_to_kml/          ← RAIZ (Root Directory)
├── Dockerfile              ← Está aqui
├── Procfile
├── requirements.txt
├── railway.json
├── backend/
│   ├── api/
│   │   └── server_flask.py ← O arquivo que o gunicorn precisa encontrar
│   ├── core/
│   └── ...
└── frontend/
```

### Comando no Dockerfile:
```dockerfile
CMD gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

Este comando procura `backend.api.server_flask` a partir do diretório de trabalho (`/app`).

---

## ⚙️ Configuração no Railway

### Settings → Build → Root Directory:

**✅ CORRETO:**
- Deixe **VAZIO** (recomendado)
- Ou coloque: `./`
- Ou coloque: `.` (sem barra)

**❌ INCORRETO:**
- `backend` → O Railway vai procurar o Dockerfile em `backend/` (não existe)
- `backend/api` → O Railway vai procurar o Dockerfile em `backend/api/` (não existe)
- Qualquer outro caminho que não seja a raiz

---

## 🔍 Como Verificar?

### 1. No Railway Dashboard:
- Settings → Build → Root Directory
- Deve estar **vazio** ou mostrar apenas `./`

### 2. Verificar o Dockerfile:
O Dockerfile começa com:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
```

Isso espera que o contexto de build seja a **raiz** do repositório, onde estão:
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `backend/` (diretório completo)
- ✅ `Procfile`

---

## 🎯 Checklist

No Railway Dashboard → Settings → Build:

- [ ] **Root Directory:** Vazio ou `./`
- [ ] **Builder:** `DOCKERFILE`
- [ ] **Dockerfile Path:** Vazio ou `Dockerfile` (se houver esse campo)
- [ ] **Build Command:** Vazio
- [ ] **Start Command:** Vazio

---

## 🚨 Se Root Directory Estiver Errado

### Sintomas:
- Build falha: "Dockerfile not found"
- Build funciona mas app não inicia: "ModuleNotFoundError: No module named 'backend'"
- Gunicorn não encontra o módulo: "Failed to find application object 'app'"

### Solução:
1. Vá em Settings → Build → Root Directory
2. Deixe **VAZIO** (apague qualquer valor)
3. Salve
4. Clear Build Cache
5. Faça novo deploy

---

## 📝 Resumo

| Configuração | Valor |
|--------------|-------|
| **Root Directory** | `(vazio)` ou `./` |
| **Builder** | `DOCKERFILE` |
| **Dockerfile Path** | `(vazio)` ou `Dockerfile` |

**O Root Directory DEVE apontar para onde está o Dockerfile (raiz do repositório).**


# 🔧 Troubleshooting: API Não Funciona

## ❌ Problema

`https://www.matrizsistema.com.br/api/test/` não está respondendo.

---

## 🔍 Checklist de Diagnóstico

### 1. Verificar Status do Container

**Railway → Deployments → Último Deployment**

**Verificar:**
- ✅ Status: SUCCESS ou FAILED?
- ✅ Quando foi o último deploy?
- ✅ Build completou?

**Se FAILED:**
- Ver logs completos do build
- Procurar por erros Python
- Verificar se dependências instalaram

---

### 2. Ver Logs do Deploy

**Railway → Deployments → View Logs (do último deployment)**

**Procurar por:**

✅ **Logs de sucesso:**
```
Successfully built [hash]
Starting gunicorn...
Listening at: http://0.0.0.0:5000
```

❌ **Logs de erro:**
```
Exited with code 1
ModuleNotFoundError: ...
ImportError: ...
```

**Me envie as últimas 30-50 linhas do log!**

---

### 3. Verificar Build Logs

**Railway → Deployments → Build Logs**

**Deve mostrar:**
```
Step 1/6 : FROM python:3.11-slim
Step 2/6 : WORKDIR /app
Step 3/6 : RUN apt-get update...
Step 4/6 : COPY requirements.txt .
Step 5/6 : RUN pip install...
Step 6/6 : COPY . .
Successfully built [hash]
```

**Se falhar:**
- Ver em qual step falhou
- Ver mensagem de erro

---

### 4. Verificar HTTP Logs

**Railway → HTTP Logs / Requests**

**Verificar:**
- ✅ Requisições chegam ao servidor?
- ✅ Qual status code retorna? (404, 500, timeout?)
- ✅ Há erros registrados?

---

### 5. Testar URLs

**Testar no navegador:**

1. `https://www.matrizsistema.com.br/`
   - Deve dar: 404 (OK) ou algum erro específico

2. `https://www.matrizsistema.com.br/api/`
   - Deve dar: 404 (OK) ou erro específico

3. `https://www.matrizsistema.com.br/api/test/`
   - Deve retornar JSON ou erro específico

**O que aparece exatamente?**
- Timeout?
- 404 Not Found?
- 502 Bad Gateway?
- 503 Service Unavailable?
- Cloudflare error?
- Página em branco?

---

### 6. Verificar DNS

**Testar se domínio resolve:**
```bash
nslookup www.matrizsistema.com.br
```

**Ou no navegador:**
- Acesse: `https://www.matrizsistema.com.br`
- Veja se carrega algo (mesmo que erro)

---

### 7. Verificar Porta

**No Railway → Networking:**

**Verificar:**
- ✅ Target Port: `5000`
- ✅ Container deve estar escutando na porta que Railway fornece via `$PORT`

**Problema comum:**
- Railway fornece `PORT=5000`
- Container deve escutar em `0.0.0.0:5000`
- ✅ Dockerfile já tem isso correto

---

## 🎯 Problemas Mais Comuns

### Problema 1: Container não está rodando

**Sintomas:**
- Timeout ao acessar URL
- 502 Bad Gateway
- Cloudflare error

**Solução:**
1. Ver logs do deploy
2. Verificar se build completou
3. Verificar se container iniciou

---

### Problema 2: Container crashou após iniciar

**Sintomas:**
- Build completa
- Container inicia
- Depois crasha (Exited with code 1)

**Solução:**
1. Ver últimas linhas do log
2. Verificar erros Python
3. Verificar se todas dependências instalaram

---

### Problema 3: Porta errada

**Sintomas:**
- Container rodando
- Mas requisições não chegam

**Solução:**
- Verificar Target Port no Networking
- Verificar se `$PORT` está sendo usado corretamente
- ✅ Dockerfile já está correto

---

### Problema 4: Rota não existe

**Sintomas:**
- 404 Not Found
- Container rodando

**Solução:**
- Verificar se rota está registrada no Flask
- ✅ Código já tem rota correta

---

### Problema 5: DNS não propagou

**Sintomas:**
- Domínio não resolve
- Timeout

**Solução:**
- Verificar configuração DNS no Registro.br
- Aguardar propagação (até 24h)

---

## 📋 Informações Necessárias

**Para diagnosticar, preciso:**

1. ✅ **Status do último deploy:** SUCCESS ou FAILED?
2. ✅ **Últimas 30-50 linhas dos logs** (Deploy Logs)
3. ✅ **O que aparece no navegador** ao acessar:
   - `https://www.matrizsistema.com.br/api/test/`
   - Erro específico? Timeout? Página em branco?
4. ✅ **HTTP Logs:** Requisições chegam ao servidor?
5. ✅ **Build Logs:** Build completou com sucesso?

---

## 🔍 Próximos Passos

### Passo 1: Verificar Logs

1. Railway → Deployments
2. Clique no último deployment
3. View Logs
4. Copie as últimas 30-50 linhas

### Passo 2: Verificar Status

1. Railway → Deployments
2. Ver status do último deploy
3. SUCCESS ou FAILED?

### Passo 3: Testar URL

1. Acesse: `https://www.matrizsistema.com.br/api/test/`
2. Veja o que aparece
3. Pressione F12 → Network tab
4. Veja status code da requisição

---

**Envie essas informações para eu diagnosticar melhor!** 🔍


# 🧪 Como Testar Domínio no Railway

## 🎯 Domínio do Projeto

**Domínio customizado:** `www.matrizsistema.com.br`

---

## ✅ Testes Disponíveis

### 1. Teste Básico: Endpoint de Teste

**URL:**
```
https://www.matrizsistema.com.br/api/test/
```

**O que deve retornar:**
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

**Como testar:**
1. Abra no navegador: `https://www.matrizsistema.com.br/api/test/`
2. Ou use curl:
   ```bash
   curl https://www.matrizsistema.com.br/api/test/
   ```

---

### 2. Teste Rota Raiz

**URL:**
```
https://www.matrizsistema.com.br/
```

**O que deve retornar:**
- ❌ 404 Not Found (esperado - não há rota na raiz)
- ✅ Se retornar 404 → Flask está rodando!

---

### 3. Teste Rota API

**URL:**
```
https://www.matrizsistema.com.br/api/
```

**O que deve retornar:**
- ❌ 404 Not Found (esperado - não há rota `/api/`)
- ✅ Se retornar 404 → Flask está rodando!

---

## 🔍 Verificações no Railway Dashboard

### 1. Verificar Status do Container

**Railway → Deployments → View Logs**

**Deve mostrar:**
```
Starting gunicorn...
Listening at: http://0.0.0.0:5000
```

**Se aparecer:**
- ✅ Container está rodando
- ❌ Se não aparecer → Container pode ter crashado

---

### 2. Verificar Public Networking

**Railway → Service → Networking → Public Networking**

**Deve estar:**
- ✅ **Public Networking:** ENABLED
- ✅ **Domínio:** `www.matrizsistema.com.br`
- ✅ **Status:** Active (verde)

---

### 3. Verificar Target Port

**Railway → Service → Networking → Public Networking**

**Deve estar:**
- ✅ **Target Port:** `5000`

---

### 4. Verificar HTTP Logs

**Railway → HTTP Logs**

**O que verificar:**
- ✅ Requisições chegando ao servidor?
- ✅ Status codes (200, 404, 500, etc.)
- ✅ Erros registrados?

---

## 🧪 Testes com Ferramentas

### Teste 1: Navegador

1. Abra: `https://www.matrizsistema.com.br/api/test/`
2. **Resultado esperado:**
   - ✅ JSON com status "ok"
   - ❌ Timeout → Domínio não está funcionando
   - ❌ Erro de certificado SSL → Certificado não ativo
   - ❌ 502/503 → Container não está rodando

---

### Teste 2: cURL (Terminal)

**Windows (PowerShell):**
```powershell
curl https://www.matrizsistema.com.br/api/test/
```

**Linux/Mac:**
```bash
curl https://www.matrizsistema.com.br/api/test/
```

**Resultado esperado:**
```json
{"status":"ok","message":"Servidor Flask está funcionando","version":"1.0"}
```

---

### Teste 3: Postman/Insomnia

1. **Método:** GET
2. **URL:** `https://www.matrizsistema.com.br/api/test/`
3. **Resultado esperado:** JSON com status 200

---

### Teste 4: Testar Certificado SSL

**Verificar se certificado está ativo:**
```bash
openssl s_client -connect www.matrizsistema.com.br:443 -servername www.matrizsistema.com.br
```

**Ou use site online:**
- https://www.ssllabs.com/ssltest/analyze.html?d=www.matrizsistema.com.br

---

## 🔍 Problemas Comuns e Soluções

### Problema 1: Timeout / Não Responde

**Causa:**
- Container não está rodando
- Public Networking está desligado
- DNS não propagou

**Solução:**
1. Verificar logs do Railway
2. Verificar se container está rodando
3. Verificar Public Networking = ENABLED

---

### Problema 2: Erro de Certificado SSL

**Causa:**
- Certificado SSL ainda não foi emitido
- DNS não propagou

**Solução:**
- Aguardar Railway emitir certificado (até 24h)
- Verificar status do certificado no Dashboard

---

### Problema 3: 502 Bad Gateway / 503 Service Unavailable

**Causa:**
- Container não está rodando
- Container crashou
- Porta errada

**Solução:**
1. Verificar logs do Railway
2. Verificar se container iniciou
3. Verificar Target Port = 5000

---

### Problema 4: 404 Not Found

**Causa:**
- Rota não existe
- Caminho errado

**Solução:**
- Verificar URL: `/api/test/` (com barra final)
- Verificar se rota está registrada no Flask

---

## 📋 Checklist de Teste

### Verificações Básicas:

- [ ] Container está rodando? (View Logs)
- [ ] Public Networking está ENABLED?
- [ ] Target Port = 5000?
- [ ] Domínio mostra status "Active"?

### Testes de Acesso:

- [ ] `https://www.matrizsistema.com.br/api/test/` retorna JSON?
- [ ] Certificado SSL está ativo? (sem erro no navegador)
- [ ] HTTP Logs mostram requisições chegando?

---

## 🎯 Próximos Passos

1. **Testar no navegador:**
   - `https://www.matrizsistema.com.br/api/test/`

2. **Verificar logs:**
   - Railway → Deployments → View Logs

3. **Verificar HTTP Logs:**
   - Railway → HTTP Logs

4. **Me diga:**
   - O que aparece ao acessar a URL?
   - Qual erro (se houver)?
   - Logs mostram o que?

---

**Use este guia para testar o domínio e me informe os resultados!**


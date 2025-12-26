# 🇧🇷 Deploy com Domínio Registro.br - Passo a Passo

Guia completo para configurar seu domínio do Registro.br com o Sistema Matriz.

---

## 🚀 Opção Recomendada: Railway

Railway é a opção mais fácil e funciona perfeitamente com Registro.br.

---

## 📋 Passo 1: Deploy no Railway

### 1.1 Criar Conta e Projeto

1. **Acesse:** https://railway.app
2. **Crie conta** (pode usar GitHub para login rápido)
3. Clique em **"New Project"**
4. Escolha **"Deploy from GitHub repo"**
5. **Conecte seu repositório** GitHub
6. Selecione o repositório do projeto

### 1.2 Configurar Deploy

Railway vai detectar automaticamente que é Python, mas você precisa configurar:

**No Railway Dashboard:**

1. Vá em **Settings** → **Deploy**
2. Configure **Start Command:**
   ```
   gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT
   ```
3. **Build Command** (opcional, Railway detecta automaticamente):
   ```
   pip install -r requirements.txt
   ```

### 1.3 Aguardar Primeiro Deploy

- Railway vai instalar dependências e iniciar o servidor
- Aguarde alguns minutos
- Anote a URL gerada: `https://seu-app.up.railway.app`

### 1.4 Testar

Abra no navegador:
```
https://seu-app.up.railway.app/api/test/
```

Deve retornar:
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando"
}
```

---

## 🌐 Passo 2: Configurar Domínio no Railway

### 2.1 Adicionar Domínio Customizado

1. No Railway Dashboard → Seu projeto
2. Clique em **Settings**
3. Vá para **Networking**
4. Na seção **"Custom Domains"**, clique em **"Custom Domain"**
5. Digite seu domínio:
   - Exemplo: `www.seudominio.com.br`
   - Ou: `seudominio.com.br` (sem www)

### 2.2 Obter Informações de DNS

Railway vai mostrar algo como:

```
Para configurar DNS, adicione:

Tipo: CNAME
Nome: www
Valor: seu-app.up.railway.app
```

**ANOTE:** O valor que aparece (algo como `seu-app.up.railway.app`)

---

## 📝 Passo 3: Configurar DNS no Registro.br

### 3.1 Acessar Painel DNS

1. **Acesse:** https://registro.br
2. Faça **login** na sua conta
3. Clique em **"Painel"** no menu superior
4. Clique em **"DNS"** no menu lateral
5. Selecione seu domínio da lista

### 3.2 Configurar CNAME para www

**Para usar www.seudominio.com.br:**

1. Na lista de registros DNS, clique em **"Adicionar"** ou **"Novo Registro"**
2. Configure:
   - **Tipo:** `CNAME`
   - **Nome:** `www`
   - **Valor:** `seu-app.up.railway.app` (o valor que Railway mostrou)
   - **TTL:** `3600` (padrão)

3. Clique em **"Salvar"** ou **"Adicionar"**

### 3.3 Configurar Domínio Raiz (opcional)

**⚠️ IMPORTANTE:** Registro.br **NÃO suporta** CNAME para domínio raiz (sem www).

**Opções:**

**Opção A: Redirecionar (Recomendado)**
1. No painel do Registro.br
2. Vá em **"Redirecionamento"**
3. Configure:
   - **Origem:** `seudominio.com.br` (sem www)
   - **Destino:** `https://www.seudominio.com.br`
   - **Tipo:** Redirecionamento 301 (Permanente)

**Opção B: Usar ALIAS (se disponível)**
- Alguns provedores DNS suportam ALIAS/ANAME
- Verifique se Registro.br suporta para seu plano

**Opção C: Usar apenas www**
- Use sempre `www.seudominio.com.br`
- Mais simples e funciona 100%

---

## ⏳ Passo 4: Aguardar Propagação DNS

### 4.1 Tempo de Propagação

- **Tempo normal:** 15 minutos a 2 horas
- **Máximo:** Até 48 horas (raramente)
- **Geralmente:** Funciona em menos de 1 hora

### 4.2 Verificar Propagação

**Opção 1: Comando (Windows PowerShell)**
```powershell
nslookup www.seudominio.com.br
```

**Opção 2: Site online**
- Acesse: https://dnschecker.org
- Digite: `www.seudominio.com.br`
- Verifique se aparece o CNAME correto

**Opção 3: Testar no navegador**
```
https://www.seudominio.com.br/api/test/
```

---

## 🔒 Passo 5: SSL/HTTPS (Automático)

### Railway Configura Automaticamente

- ✅ Railway detecta quando DNS está correto
- ✅ Gera certificado SSL automaticamente (Let's Encrypt)
- ✅ Renova automaticamente
- ⏱️ Pode levar 5-15 minutos após DNS propagar

**Verificar:**
- Acesse: `https://www.seudominio.com.br/api/test/`
- Deve aparecer o cadeado verde (HTTPS seguro)

---

## 🔧 Passo 6: Configurar CORS (Opcional)

Se quiser restringir CORS ao seu domínio:

**No Railway Dashboard:**
1. Settings → **Variables**
2. Adicione variável:
   - **Nome:** `ALLOWED_ORIGINS`
   - **Valor:** `https://www.seudominio.com.br,https://seudominio.com.br`

O código já está preparado para usar essa variável.

---

## 📋 Checklist Completo

- [ ] ✅ Conta criada no Railway
- [ ] ✅ Projeto deployado no Railway
- [ ] ✅ URL do Railway funcionando (`/api/test/`)
- [ ] ✅ Domínio adicionado no Railway (Custom Domain)
- [ ] ✅ CNAME configurado no Registro.br (www → Railway)
- [ ] ✅ Aguardou propagação DNS (verificou com nslookup)
- [ ] ✅ SSL/HTTPS funcionando (cadeado verde)
- [ ] ✅ Testou: `https://www.seudominio.com.br/api/test/`
- [ ] ✅ Frontend acessível (se configurado)

---

## 🎯 Configurar Frontend

### Opção A: Frontend no mesmo servidor (Railway)

Você pode servir o frontend estático junto com a API. Configure Nginx no Railway ou use o Flask para servir arquivos estáticos.

**Adicione ao `server_flask.py`:**

```python
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('../frontend/desktop_app', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend/desktop_app', path)
```

### Opção B: Frontend separado (Netlify/Vercel)

1. Deploy do frontend em Netlify ou Vercel
2. Configure domínio: `app.seudominio.com.br`
3. Atualize `app.js` para usar: `https://www.seudominio.com.br/api`

---

## 🐛 Problemas e Soluções

### DNS não propaga

**Verificar:**
```powershell
nslookup www.seudominio.com.br
```

**Se não aparecer o CNAME:**
- Verifique se salvou no Registro.br
- Aguarde mais tempo
- Limpe cache DNS: `ipconfig /flushdns` (Windows)

### SSL não funciona

- Aguarde mais tempo (Railway leva alguns minutos)
- Verifique se DNS está correto
- Railway só gera SSL quando DNS está propagado

### CORS bloqueando

**Temporário para testar:**
No `server_flask.py`, linha ~23, mude para:
```python
CORS(app)  # Permite todos (temporário)
```

**Produção:**
Configure variável `ALLOWED_ORIGINS` no Railway.

### Site não carrega

**Verificar:**
1. Railway está rodando? (veja logs no dashboard)
2. DNS está correto? (`nslookup`)
3. SSL está funcionando? (cadeado verde)

---

## 📸 Exemplo Visual - Registro.br

### Tela de DNS no Registro.br:

```
┌─────────────────────────────────────────┐
│ DNS - seudominio.com.br                 │
├─────────────────────────────────────────┤
│ Tipo    │ Nome │ Valor                  │
├─────────┼──────┼────────────────────────┤
│ CNAME   │ www  │ seu-app.up.railway.app │ ← ADICIONE ESTE
└─────────────────────────────────────────┘
```

---

## ✅ Resultado Final

Após configurar tudo, você terá:

**Backend API:**
- ✅ `https://www.seudominio.com.br/api/test/`
- ✅ `https://www.seudominio.com.br/api/gerar-matriz/`

**Frontend (se configurado):**
- ✅ `https://www.seudominio.com.br/`

**Tudo funcionando com:**
- ✅ HTTPS/SSL automático
- ✅ Domínio personalizado
- ✅ Certificado renovado automaticamente

---

## 🆘 Precisa de Ajuda?

Se tiver problemas, me diga:

1. ✅ Em qual etapa está?
2. ✅ Qual erro aparece?
3. ✅ O que você vê no `nslookup`?

Posso ajudar a resolver! 🚀


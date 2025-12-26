# 🌐 Configurar Domínio Existente - Sistema Matriz

Guia para usar seu domínio próprio com o Sistema Matriz.

## 📋 Informações Necessárias

Antes de começar, você precisa saber:
- ✅ Seu domínio (ex: `meusistema.com.br`)
- ✅ Onde está hospedado o DNS (Registro.br, GoDaddy, Cloudflare, etc.)
- ✅ Qual plataforma de deploy você vai usar (Railway, Render, VPS, etc.)

---

## 🚀 Opção 1: Railway (Mais Fácil)

### Passo 1: Deploy no Railway

1. **Acesse:** https://railway.app
2. **Crie conta** e conecte seu repositório GitHub
3. **Faça deploy** do projeto
4. **Anote a URL gerada:** `https://seu-app.up.railway.app`

### Passo 2: Configurar Domínio no Railway

1. No Railway Dashboard → Seu projeto → **Settings**
2. Vá para **Networking**
3. Clique em **"Custom Domain"**
4. Digite seu domínio: `www.seu-dominio.com.br`
5. Railway mostrará as instruções de DNS

### Passo 3: Configurar DNS no Provedor

**Exemplo para Registro.br:**
1. Acesse: https://registro.br
2. Vá em **"Painel"** → **"DNS"**
3. Adicione/Edite registros:

**Para www (recomendado):**
- Tipo: **CNAME**
- Nome: `www`
- Valor: `seu-app.up.railway.app`
- TTL: 3600

**Para domínio raiz (sem www):**
- Tipo: **A** (se suportado) ou **ALIAS**
- Nome: `@` ou deixe em branco
- Valor: IP fornecido pelo Railway (ou use CNAME se suportado)

### Passo 4: Aguardar Propagação

- DNS geralmente propaga em **15 minutos a 2 horas**
- Pode demorar até 48h (mas raro)
- Teste com: https://dnschecker.org

### Passo 5: Configurar SSL (Automático)

Railway configura SSL automaticamente quando o DNS está correto. Aguarde alguns minutos após propagação.

---

## 🚀 Opção 2: Render

### Passo 1: Deploy no Render

1. Acesse: https://render.com
2. **"New" → "Web Service"**
3. Conecte GitHub e faça deploy

### Passo 2: Configurar Domínio

1. Settings → **Custom Domains**
2. Clique em **"Add"**
3. Digite: `www.seu-dominio.com.br`
4. Render mostrará as configurações DNS

### Passo 3: Configurar DNS

No seu provedor de DNS, adicione:

**Para www:**
- Tipo: **CNAME**
- Nome: `www`
- Valor: `seu-app.onrender.com`

**Para domínio raiz:**
- Tipo: **A**
- Nome: `@`
- Valor: (IP fornecido pelo Render)

### Passo 4: SSL

Render configura SSL automaticamente após DNS propagar.

---

## 🖥️ Opção 3: VPS (DigitalOcean, Linode, AWS EC2)

Se você tem ou quer um servidor próprio.

### Passo 1: Configurar Servidor

```bash
# No seu servidor VPS
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx -y
```

### Passo 2: Deploy da Aplicação

```bash
# Criar diretório
sudo mkdir -p /var/www/matriz-app
cd /var/www/matriz-app

# Upload do código (Git, SCP, etc.)
git clone https://github.com/seu-usuario/matriz_csv_to_kml.git .

# Configurar ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Passo 3: Configurar Nginx

**Crie:** `/etc/nginx/sites-available/matriz-app`

```nginx
server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/matriz-app/matriz-app.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Servir arquivos estáticos do frontend
    location /static/ {
        alias /var/www/matriz-app/frontend/desktop_app/;
    }
    
    # Servir arquivos do frontend diretamente
    location / {
        try_files $uri $uri/ /index.html;
        root /var/www/matriz-app/frontend/desktop_app;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/matriz-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Passo 4: Configurar DNS

No provedor de DNS:

**Registro A:**
- Tipo: **A**
- Nome: `@` (ou vazio)
- Valor: **IP do seu servidor VPS**

**Para www:**
- Tipo: **CNAME**
- Nome: `www`
- Valor: `seu-dominio.com.br`

Ou:
- Tipo: **A**
- Nome: `www`
- Valor: **IP do seu servidor VPS**

### Passo 5: Configurar SSL (HTTPS)

```bash
sudo certbot --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br
```

Certbot configura automaticamente HTTPS e renova automaticamente.

---

## 🔧 Atualizar Código para seu Domínio

### 1. Atualizar CORS no Backend

Edite `backend/api/server_flask.py`:

```python
from flask_cors import CORS

# Opção 1: Permitir seu domínio específico (mais seguro)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://seu-dominio.com.br",
            "https://www.seu-dominio.com.br",
            "http://localhost:8000",  # Para desenvolvimento
            "http://localhost:8080"   # Para desenvolvimento
        ]
    }
})

# Opção 2: Permitir todos (menos seguro, mas funciona sempre)
# CORS(app)
```

### 2. Frontend já está configurado

O `app.js` já detecta automaticamente se está em produção ou desenvolvimento. Não precisa mudar nada!

Mas se quiser forçar seu domínio, pode adicionar:

```javascript
// No início do arquivo app.js
const PRODUCTION_DOMAIN = 'https://seu-dominio.com.br';
```

---

## 📝 Exemplo Prático: Registro.br

### 1. No Registro.br:

1. Acesse: https://registro.br
2. Login → **Painel** → **DNS**
3. Selecione seu domínio
4. Adicione registros:

**Registro CNAME para www:**
- Tipo: CNAME
- Nome: `www`
- Valor: `seu-app.up.railway.app` (ou seu servidor)
- TTL: 3600

**Registro A para domínio raiz (se usar VPS):**
- Tipo: A
- Nome: (deixe vazio ou `@`)
- Valor: `123.456.789.012` (IP do seu servidor)

### 2. No Railway/Render:

Siga as instruções da plataforma para adicionar o domínio customizado.

### 3. Aguardar:

- Aguarde 15 minutos a 2 horas
- Teste: `ping www.seu-dominio.com.br` (deve apontar para o servidor)
- Teste: `https://www.seu-dominio.com.br/api/test/`

---

## 🔍 Verificar se Funcionou

### Teste 1: DNS está correto?

```bash
# Windows PowerShell
nslookup www.seu-dominio.com.br

# Linux/Mac
dig www.seu-dominio.com.br
```

Deve mostrar o IP do servidor ou o CNAME correto.

### Teste 2: API está respondendo?

Abra no navegador:
- `https://www.seu-dominio.com.br/api/test/`

Deve retornar:
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando"
}
```

### Teste 3: Frontend funciona?

Abra:
- `https://www.seu-dominio.com.br/` (ou onde você colocou o frontend)

---

## 🌐 Estrutura Recomendada

### Opção A: Tudo no mesmo servidor

```
https://seu-dominio.com.br/
├── / (frontend/index.html)
├── /api/test/ (backend API)
└── /api/gerar-matriz/ (backend API)
```

**Vantagem:** Simples, um só servidor

### Opção B: Frontend separado (CDN/Netlify)

```
Frontend:
- https://app.seu-dominio.com.br
  ou
- https://seu-dominio.com.br

Backend API:
- https://api.seu-dominio.com.br
```

**Vantagem:** Frontend rápido (CDN), backend escalável

---

## 🔒 Segurança - Configurar HTTPS

### Railway/Render:
- ✅ SSL/HTTPS é **automático**
- ✅ Certificado renova automaticamente
- ✅ Sem configuração necessária

### VPS:
- ✅ Use **Certbot** (Let's Encrypt - grátis)
- ✅ Renovação automática
- ✅ Comando: `sudo certbot --nginx -d seu-dominio.com.br`

---

## 🐛 Problemas Comuns

### "DNS não propaga"
- Aguarde mais tempo (até 48h)
- Verifique se configurou DNS corretamente
- Use https://dnschecker.org para verificar globalmente

### "SSL não funciona"
- Aguarde alguns minutos após DNS propagar
- Verifique se o servidor está rodando na porta 443 (HTTPS)
- Railway/Render configuram automaticamente

### "CORS bloqueando"
- Verifique se adicionou seu domínio no CORS
- Use `CORS(app)` temporariamente para testar

### "Site não carrega"
- Verifique se o servidor está rodando
- Verifique logs do Railway/Render
- Teste a URL gerada pela plataforma primeiro

---

## 📋 Checklist Final

- [ ] Deploy feito na plataforma escolhida
- [ ] Domínio configurado na plataforma
- [ ] DNS configurado no provedor
- [ ] Aguardou propagação DNS
- [ ] SSL/HTTPS funcionando
- [ ] CORS configurado para seu domínio
- [ ] Testou `/api/test/` no domínio
- [ ] Frontend acessível no domínio

---

## 💡 Próximos Passos

1. ✅ Escolha a plataforma (Railway, Render, ou VPS)
2. ✅ Faça deploy
3. ✅ Configure domínio na plataforma
4. ✅ Configure DNS no provedor
5. ✅ Aguarde propagação
6. ✅ Teste e verifique SSL
7. ✅ Atualize CORS se necessário

**Precisa de ajuda com alguma etapa específica?** Me diga:
- Qual plataforma você quer usar?
- Qual é seu domínio?
- Onde está hospedado o DNS?

Posso criar instruções mais específicas!


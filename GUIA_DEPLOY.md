# 🌐 Guia de Deploy - Sistema Matriz na Internet

Este guia explica como colocar o Sistema Matriz na internet com um domínio próprio.

## 📋 Opções de Deploy

### ✅ Recomendado para Começar:
1. **Heroku** - Fácil, grátis para começar, configuração mínima
2. **Railway** - Simples, bom para apps Python
3. **Render** - Gratuito, fácil configuração

### Para Produção:
4. **DigitalOcean** - VPS completo, mais controle
5. **AWS/Google Cloud** - Infraestrutura completa
6. **Vercel/Netlify** - Para frontend estático + backend separado

---

## 🚀 Opção 1: Heroku (Mais Fácil)

### Pré-requisitos:
```bash
pip install gunicorn
```

### Passo 1: Criar arquivos de configuração

**`Procfile`** (na raiz do projeto):
```
web: gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT
```

**`requirements.txt`** (na raiz do projeto):
```
flask
flask-cors
pandas
gunicorn
lxml
openpyxl
```

**`runtime.txt`** (na raiz do projeto):
```
python-3.11.0
```

### Passo 2: Modificar server_flask.py para produção

Adicione no final do arquivo `backend/api/server_flask.py`:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Passo 3: Deploy no Heroku

```bash
# 1. Instale Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Criar app
heroku create nome-do-seu-app

# 4. Deploy
git init
git add .
git commit -m "Deploy inicial"
git push heroku main

# 5. Abrir app
heroku open
```

**URL:** `https://nome-do-seu-app.herokuapp.com`

### Passo 4: Configurar Domínio Personalizado

```bash
# No Heroku Dashboard ou via CLI:
heroku domains:add www.seu-dominio.com.br
heroku domains:add seu-dominio.com.br

# Depois configure DNS no seu provedor de domínio:
# Tipo: CNAME
# Nome: www
# Valor: nome-do-seu-app.herokuapp.com

# Tipo: ALIAS/ANAME
# Nome: @
# Valor: nome-do-seu-app.herokuapp.com
```

---

## 🚀 Opção 2: Railway (Recomendado)

### Passo 1: Criar arquivo de configuração

**`railway.json`** (na raiz do projeto):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/api/test/",
    "healthcheckTimeout": 100
  }
}
```

### Passo 2: Deploy

1. Acesse: https://railway.app
2. Conecte seu repositório GitHub
3. Railway detecta automaticamente Python
4. Configure a variável de ambiente:
   - `PORT` (automático)
   - `PYTHONPATH=/app` (se necessário)

### Passo 3: Configurar Domínio

1. No Railway Dashboard → Settings → Networking
2. Clique em "Generate Domain" ou adicione domínio customizado
3. Configure DNS no seu provedor

**URL:** `https://seu-app.up.railway.app`

---

## 🚀 Opção 3: Render

### Passo 1: Criar arquivo de configuração

**`render.yaml`** (na raiz do projeto):
```yaml
services:
  - type: web
    name: matriz-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PORT
        value: 8000
```

### Passo 2: Deploy

1. Acesse: https://render.com
2. Conecte repositório GitHub
3. Crie novo Web Service
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT`

### Passo 3: Domínio

1. Settings → Custom Domain
2. Adicione seu domínio
3. Configure DNS conforme instruções

---

## 🖥️ Opção 4: VPS (DigitalOcean, Linode, etc.)

Para controle total e melhor performance.

### Passo 1: Configurar Servidor

```bash
# No servidor VPS (Ubuntu/Debian):

# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python e dependências
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx -y

# 3. Criar usuário para a aplicação
sudo adduser matriz-app
sudo usermod -aG sudo matriz-app

# 4. Criar diretório da aplicação
sudo mkdir -p /var/www/matriz-app
sudo chown matriz-app:matriz-app /var/www/matriz-app
```

### Passo 2: Fazer Upload dos Arquivos

```bash
# Opção A: Git
cd /var/www/matriz-app
git clone https://github.com/seu-usuario/matriz_csv_to_kml.git .

# Opção B: SCP/SFTP
scp -r . matriz-app@seu-servidor:/var/www/matriz-app/
```

### Passo 3: Configurar Ambiente Virtual

```bash
cd /var/www/matriz-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Passo 4: Criar Serviço Systemd

**`/etc/systemd/system/matriz-app.service`**:
```ini
[Unit]
Description=Matriz App Gunicorn daemon
After=network.target

[Service]
User=matriz-app
Group=www-data
WorkingDirectory=/var/www/matriz-app
Environment="PATH=/var/www/matriz-app/venv/bin"
ExecStart=/var/www/matriz-app/venv/bin/gunicorn --workers 3 --bind unix:/var/www/matriz-app/matriz-app.sock backend.api.server_flask:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start matriz-app
sudo systemctl enable matriz-app
```

### Passo 5: Configurar Nginx

**`/etc/nginx/sites-available/matriz-app`**:
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
}
```

```bash
sudo ln -s /etc/nginx/sites-available/matriz-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Passo 6: Configurar SSL (HTTPS)

```bash
sudo certbot --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br
```

### Passo 7: Configurar DNS

No seu provedor de domínio:
- Tipo: A
- Nome: @
- Valor: IP do seu servidor VPS

- Tipo: A
- Nome: www
- Valor: IP do seu servidor VPS

---

## 🔧 Modificações Necessárias no Código

### 1. Atualizar CORS no server_flask.py

```python
from flask_cors import CORS

# Para produção, restrinja as origens:
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://seu-dominio.com.br", "https://www.seu-dominio.com.br"]
    }
})

# Ou permita todas (menos seguro):
CORS(app)
```

### 2. Atualizar Frontend para usar domínio

No `frontend/desktop_app/app.js`, substitua `localhost`:

```javascript
// Opção A: Detectar automaticamente
const API_BASE_URL = window.location.origin + '/api';

// Opção B: Configurar domínio
const API_BASE_URL = 'https://seu-dominio.com.br/api';

// Usar no fetch:
const API_URL = `${API_BASE_URL}/gerar-matriz/`;
```

### 3. Configurar variáveis de ambiente

**`.env`** (não commitar no Git):
```
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_ORIGINS=https://seu-dominio.com.br,https://www.seu-dominio.com.br
```

---

## 📦 Estrutura de Arquivos para Deploy

```
matriz_csv_to_kml/
├── backend/
│   └── api/
│       └── server_flask.py
├── frontend/
│   └── desktop_app/
│       ├── index.html
│       └── app.js
├── requirements.txt
├── Procfile (para Heroku)
├── runtime.txt (para Heroku)
└── .gitignore
```

### `.gitignore`:
```
__pycache__/
*.pyc
*.pyo
venv/
env/
.env
*.log
resultados/
*.kml
*.csv
.DS_Store
node_modules/
```

---

## 🔒 Segurança para Produção

### 1. Desabilitar Debug Mode

```python
# Em server_flask.py
app.run(host='0.0.0.0', port=port, debug=False)  # debug=False em produção!
```

### 2. Rate Limiting (opcional)

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/gerar-matriz/', methods=['POST'])
@limiter.limit("10 per minute")
def gerar_matriz_api():
    # ...
```

### 3. Validação de Entrada

```python
# Validar tamanho máximo de dados
MAX_VERTICES = 10000
if len(vertices) > MAX_VERTICES:
    return jsonify({'error': 'Muitos vértices'}), 400
```

---

## 📊 Comparação de Opções

| Opção | Custo | Facilidade | Performance | Controle |
|-------|-------|------------|-------------|----------|
| **Heroku** | $7-25/mês | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Railway** | $5-20/mês | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Render** | Grátis-$7/mês | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **VPS** | $5-40/mês | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## ✅ Checklist de Deploy

- [ ] Criar `requirements.txt` com todas as dependências
- [ ] Configurar `Procfile` ou comando de start
- [ ] Modificar `server_flask.py` para produção (debug=False)
- [ ] Atualizar CORS para permitir seu domínio
- [ ] Atualizar frontend para usar URL de produção
- [ ] Configurar variáveis de ambiente
- [ ] Configurar SSL/HTTPS
- [ ] Configurar DNS
- [ ] Testar todos os endpoints
- [ ] Configurar backup (se necessário)

---

## 🎯 Recomendação Final

**Para começar rapidamente:**
1. Use **Railway** ou **Render** (gratuito para começar)
2. Depois migre para **VPS** se precisar de mais controle

**Para produção séria:**
1. Use **VPS** (DigitalOcean, Linode)
2. Configure Nginx + Gunicorn
3. Use SSL/HTTPS (Let's Encrypt grátis)
4. Configure backup automático

---

## 📚 Próximos Passos

1. Escolha uma opção de deploy
2. Siga os passos específicos acima
3. Configure seu domínio
4. Teste a aplicação

Precisa de ajuda com alguma opção específica? Posso criar guias detalhados para cada uma!


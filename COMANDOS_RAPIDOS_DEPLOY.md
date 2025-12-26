# ⚡ Comandos Rápidos - Deploy Registro.br

## 🚀 Deploy no Railway (5 minutos)

### 1. Preparar repositório
```bash
git add .
git commit -m "Preparar para deploy"
git push origin main
```

### 2. No Railway
1. Acesse: https://railway.app
2. Login com GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecione repositório
5. Settings → Deploy → Start Command:
   ```
   gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT
   ```

### 3. Obter URL
- Railway gera: `https://seu-app.up.railway.app`
- Anote essa URL!

---

## 📝 Configurar DNS no Registro.br

### Acesso rápido:
1. https://registro.br → Login
2. Painel → DNS → Seu domínio
3. Adicionar registro:

**CNAME para www:**
- Tipo: **CNAME**
- Nome: **www**
- Valor: **seu-app.up.railway.app** (URL do Railway)
- TTL: 3600

### Redirecionamento (domínio raiz):
- Painel → **Redirecionamento**
- Origem: `seudominio.com.br`
- Destino: `https://www.seudominio.com.br`
- Tipo: 301

---

## ✅ Verificar se Funcionou

### Teste DNS:
```powershell
nslookup www.seudominio.com.br
```
Deve mostrar: `seu-app.up.railway.app`

### Teste API:
```
https://www.seudominio.com.br/api/test/
```
Deve retornar JSON com `"status": "ok"`

---

## ⏱️ Tempos

- ✅ Deploy Railway: 3-5 minutos
- ✅ Configurar DNS: 2 minutos
- ⏳ Propagação DNS: 15 min - 2 horas
- 🔒 SSL Railway: 5-15 minutos após DNS

**Total: ~30 minutos até tudo funcionar!**


# 🔧 Correção do Deploy no Railway

## Problema
O Railway não está detectando automaticamente que este é um projeto Python Flask.

## ✅ Solução

### 1. Verificar arquivos na raiz
O Railway precisa encontrar:
- ✅ `requirements.txt` (já existe)
- ✅ `Procfile` (já existe)
- ✅ `runtime.txt` (já existe)
- ✅ `railway.json` (criado)
- ✅ `nixpacks.toml` (criado)

### 2. Configurar no Railway Dashboard

1. **Acesse seu projeto no Railway**
2. **Vá em Settings → Build & Deploy**
3. **Configure:**

   **Build Command:**
   ```
   pip install -r requirements.txt
   ```

   **Start Command:**
   ```
   gunicorn backend.api.server_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

   **Ou use o Procfile automaticamente (recomendado)**

### 3. Variáveis de Ambiente

No Railway Dashboard → Variables:
- `PORT` - será configurado automaticamente
- `ALLOWED_ORIGINS` (opcional) - domínios permitidos para CORS

### 4. Se ainda não funcionar

**Opção A: Usar Nixpacks Builder**
- No Railway Dashboard → Settings → Build & Deploy
- Selecione "Nixpacks" como Builder
- O arquivo `nixpacks.toml` será usado automaticamente

**Opção B: Limpar cache e fazer novo deploy**
- Settings → Build & Deploy → Clear Build Cache
- Fazer novo deploy

### 5. Verificar logs

Se o erro persistir, verifique os logs no Railway:
- Deployments → Clique no deploy → Ver logs
- Procure por erros de import ou dependências

## 📋 Checklist

- [ ] `requirements.txt` está na raiz
- [ ] `Procfile` está na raiz
- [ ] `runtime.txt` está na raiz (Python 3.9)
- [ ] `railway.json` existe
- [ ] `nixpacks.toml` existe
- [ ] Build Command configurado no Railway
- [ ] Start Command configurado no Railway
- [ ] Sem arquivos Python duplicados na raiz

## 🔍 Troubleshooting

**Erro: "Could not determine how to build"**
→ Verifique se `requirements.txt` está na raiz do repositório

**Erro: "Module not found"**
→ Verifique se todas as dependências estão em `requirements.txt`

**Erro: "Port already in use"**
→ Use `$PORT` no comando de start (já está no Procfile)

**Erro: "Command not found: gunicorn"**
→ Adicione `gunicorn` no `requirements.txt` (já está)


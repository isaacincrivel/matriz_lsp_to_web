# 🔒 Resolver Erro: NET::ERR_CERT_COMMON_NAME_INVALID

## ❌ Problema

**Erro no navegador:**
```
A sua ligação não é privada
NET::ERR_CERT_COMMON_NAME_INVALID
```

**Causa:** Certificado SSL do domínio customizado não está configurado ou ainda não foi emitido pelo Railway.

---

## ✅ Soluções

### Opção 1: Aguardar Certificado SSL (Recomendado)

**O Railway emite certificado SSL automaticamente, mas pode levar tempo:**

1. **Railway → Networking → Custom Domain**
2. **Verificar status do certificado:**
   - ✅ **"SSL Certificate: Active"** → Certificado ativo
   - ⏳ **"SSL Certificate: Pending"** → Aguardando emissão
   - ❌ **"SSL Certificate: Error"** → Erro na configuração

**Tempo de espera:**
- ⏳ Pode levar de **5 minutos a 24 horas**
- ⏳ Railway renova verificação a cada hora
- ⏳ DNS precisa estar propagado corretamente

---

### Opção 2: Verificar Configuração DNS

**No Registro.br:**

1. **Verificar registro CNAME:**
   - **Nome:** `www` (ou `@` para domínio raiz)
   - **Tipo:** `CNAME`
   - **Valor:** O domínio fornecido pelo Railway (ex: `seu-projeto.up.railway.app`)

2. **Verificar propagação DNS:**
   ```bash
   nslookup www.matrizsistema.com.br
   ```
   - Deve retornar o domínio do Railway

3. **Aguardar propagação:**
   - TTL padrão: 1 hora
   - Propagação completa: até 24 horas

---

### Opção 3: Usar Domínio Railway Temporariamente

**Enquanto certificado não está pronto:**

1. **Railway → Networking → Public Networking**
2. **Clique em "Generate Domain"** (se ainda não tiver)
3. **Use o domínio Railway:**
   - Exemplo: `https://seu-projeto.up.railway.app/api/test/`
   - Este domínio já tem SSL ativo

**Vantagem:**
- ✅ Funciona imediatamente
- ✅ SSL já configurado
- ✅ Pode testar enquanto certificado customizado não está pronto

---

### Opção 4: Acessar com HTTP (Temporário - NÃO Recomendado)

**⚠️ ATENÇÃO: Não seguro, apenas para teste!**

1. **Tente acessar com HTTP:**
   ```
   http://www.matrizsistema.com.br/api/test/
   ```

2. **Se funcionar:**
   - ✅ Servidor está rodando
   - ✅ Problema é apenas SSL
   - ⚠️ Mas HTTP não é seguro!

**NÃO use HTTP em produção!** Apenas para verificar se servidor está funcionando.

---

### Opção 5: Aceitar Certificado (Desenvolvimento)

**⚠️ APENAS para desenvolvimento/teste local:**

1. Na página de erro, clique em **"Avançadas"** (Advanced)
2. Clique em **"Prosseguir para www.matrizsistema.com.br (não seguro)"**
3. ⚠️ **NÃO faça isso em produção!**

---

## 🔍 Verificar Status no Railway

### Railway → Networking → Custom Domain

**Verificar:**

1. **Status do domínio:**
   - ✅ **"Active"** → Domínio ativo
   - ⏳ **"Pending"** → Aguardando validação
   - ❌ **"Error"** → Erro na configuração

2. **Status do certificado SSL:**
   - ✅ **"SSL Certificate: Active"** → Certificado ativo
   - ⏳ **"SSL Certificate: Pending"** → Aguardando emissão
   - ❌ **"SSL Certificate: Error"** → Erro

3. **DNS Configuration:**
   - Verificar se mostra instruções de DNS
   - Verificar se DNS está configurado corretamente

---

## 📋 Checklist

- [ ] DNS configurado no Registro.br (CNAME correto)
- [ ] DNS propagado (testar com `nslookup`)
- [ ] Railway mostra domínio como "Active"
- [ ] Railway mostra certificado SSL como "Active" ou "Pending"
- [ ] Aguardou tempo suficiente (até 24h para SSL)

---

## 🎯 Solução Rápida (Teste Imediato)

**Para testar se servidor está funcionando:**

1. **Railway → Networking → Public Networking**
2. **Veja o domínio Railway gerado:**
   - Exemplo: `https://seu-projeto.up.railway.app`
3. **Teste:**
   ```
   https://seu-projeto.up.railway.app/api/test/
   ```

**Se funcionar:**
- ✅ Servidor está rodando
- ✅ Problema é apenas certificado SSL do domínio customizado
- ⏳ Aguardar Railway emitir certificado

---

## ⏳ Tempo de Espera

**Certificado SSL:**
- ⏳ **Mínimo:** 5-10 minutos
- ⏳ **Máximo:** 24 horas
- ⏳ Railway verifica a cada hora

**DNS:**
- ⏳ **TTL:** 1 hora (padrão)
- ⏳ **Propagação completa:** até 24 horas

---

## 🔍 Verificar se Servidor Está Rodando

**Mesmo com erro de certificado, você pode verificar:**

1. **Railway → Deployments → View Logs**
2. **Procurar por:**
   ```
   Starting gunicorn...
   Listening at: http://0.0.0.0:5000
   ```

**Se aparecer:**
- ✅ Servidor está rodando
- ✅ Problema é apenas SSL

**Se não aparecer:**
- ❌ Servidor não está rodando
- ❌ Verificar logs para erros

---

## ✅ Próximos Passos

1. **Verificar Railway → Networking → Custom Domain:**
   - Status do certificado SSL
   - Status do domínio

2. **Testar domínio Railway:**
   - `https://seu-projeto.up.railway.app/api/test/`
   - Se funcionar → servidor OK, problema é SSL

3. **Aguardar certificado:**
   - Railway emite automaticamente
   - Pode levar até 24 horas

4. **Verificar DNS:**
   - Confirmar CNAME no Registro.br
   - Testar propagação com `nslookup`

---

**O erro é de certificado SSL, não do servidor! Verifique o status do certificado no Railway Dashboard.**


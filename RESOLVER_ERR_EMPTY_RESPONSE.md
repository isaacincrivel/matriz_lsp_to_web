# 🔧 Resolver Erro: ERR_EMPTY_RESPONSE

## ❌ Problema

```
GET http://localhost:8000/api/test/ net::ERR_EMPTY_RESPONSE
Servidor Flask não encontrado nas portas 8000-8004
```

**Causa:** O backend Flask não está rodando.

---

## ✅ Solução

### Opção 1: Iniciar Backend com Script (Windows) ⭐ RECOMENDADO

1. **Abra um novo terminal/PowerShell**
2. **Navegue até a pasta do projeto:**
   ```powershell
   cd C:\matriz_csv_to_kml
   ```

3. **Execute o script:**
   ```powershell
   .\backend\api\start_server.bat
   ```

4. **Ou execute diretamente:**
   ```powershell
   python backend\api\server_flask.py
   ```

5. **Aguarde ver:**
   ```
   ================================================================================
   🚀 Servidor Flask iniciando...
   ================================================================================
   🔧 Modo: DESENVOLVIMENTO
   📡 API disponível em: http://0.0.0.0:8000/api/gerar-matriz/
   🧪 Teste: http://0.0.0.0:8000/api/test/
   ================================================================================
   ```

6. **Mantenha este terminal aberto!** O servidor precisa estar rodando.

---

### Opção 2: Verificar se Backend está Rodando

**Teste no navegador:**
Abra: `http://localhost:8000/api/test/`

**Deve retornar:**
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

**Se não funcionar:** Backend não está rodando → Inicie com Opção 1

---

## 🔍 Diagnóstico Completo

### 1. Verificar Porta Disponível

**O Flask procura portas 8000-8009 automaticamente:**

Se a porta 8000 estiver ocupada, o Flask vai tentar 8001, 8002, etc.

**Ver logs do terminal** para ver qual porta foi escolhida:
```
📡 API disponível em: http://0.0.0.0:8001/api/gerar-matriz/
```

**Se for porta diferente de 8000:**
- O frontend vai detectar automaticamente (procura 8000-8004)
- Se for 8005+, você precisa ajustar

---

### 2. Verificar se Porta está Bloqueada

**No PowerShell:**
```powershell
# Ver se porta 8000 está em uso
netstat -ano | findstr :8000

# Ver processos Python rodando
tasklist | findstr python
```

**Se a porta estiver ocupada:**
- Feche outros programas que usam a porta
- Ou deixe o Flask escolher outra porta automaticamente

---

### 3. Verificar Erros no Terminal do Backend

**Procure por mensagens de erro:**
```
❌ Erro ao iniciar servidor
ModuleNotFoundError: ...
```

**Se houver erros:**
1. Instale dependências:
   ```powershell
   pip install -r requirements.txt
   ```

2. Verifique se Python está instalado:
   ```powershell
   python --version
   ```

---

## 📋 Checklist

Antes de testar no frontend:

- [ ] Backend está rodando (terminal aberto com servidor)
- [ ] Terminal mostra: "API disponível em: http://0.0.0.0:8000..."
- [ ] `http://localhost:8000/api/test/` retorna JSON no navegador
- [ ] Frontend está aberto em outro terminal/navegador
- [ ] Ambos estão rodando simultaneamente

---

## 🎯 Fluxo Correto

### Terminal 1 - Backend:
```powershell
python backend\api\server_flask.py
# Mantenha rodando!
```

### Terminal 2 - Frontend (se usar servidor HTTP):
```powershell
cd frontend\desktop_app
python -m http.server 3000
```

### Navegador:
- Abra: `http://localhost:3000` ou `http://localhost:5500`
- Frontend vai detectar backend automaticamente

---

## 🆘 Se Ainda Não Funcionar

### 1. Verificar CORS

O Flask já tem CORS habilitado. Se houver erro de CORS:
- Verifique se está usando servidor HTTP (não `file://`)
- Use `python -m http.server` para servir o frontend

### 2. Verificar Firewall

**Windows pode bloquear a porta:**
- Deixe o firewall permitir Python
- Ou desative temporariamente para testar

### 3. Testar Backend Diretamente

**Use Postman ou curl:**
```powershell
curl http://localhost:8000/api/test/
```

**Ou no navegador:**
`http://localhost:8000/api/test/`

---

## ✅ Solução Rápida

**Em um terminal, execute:**

```powershell
cd C:\matriz_csv_to_kml
python backend\api\server_flask.py
```

**Deixe rodando e teste no navegador:**
1. Abra: `http://localhost:8000/api/test/`
2. Deve retornar JSON
3. Depois teste o frontend

---

**O problema é simples: você precisa ter o backend rodando em um terminal enquanto usa o frontend!** 🚀


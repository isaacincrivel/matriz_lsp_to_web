# 🔍 Debug: Erro 500 na Raiz

## ❌ Problema

Ao acessar `https://www.matrizsistema.com.br/`, aparece:
```
Internal Server Error
The server encountered an internal error and was unable to complete your request.
```

---

## 🔍 Possíveis Causas

### 1. Arquivo não encontrado

**Causa:**
- Caminho do `FRONTEND_DIR` pode estar errado no Docker
- Arquivo `index.html` não existe no caminho esperado

**Sintoma:**
- Erro ao tentar servir `index.html`

---

### 2. Permissões de arquivo

**Causa:**
- Flask não tem permissão para ler o arquivo
- Arquivo não está acessível no container

---

### 3. Erro no tratamento de exceção

**Causa:**
- Exceção não tratada corretamente
- Logs não mostram o erro específico

---

## ✅ Correção Aplicada

### Melhorias:

1. **Verificação de arquivo existe:**
   ```python
   if not os.path.exists(index_path):
       # Log detalhado do erro
   ```

2. **Logging melhorado:**
   - Mostra caminho esperado
   - Mostra diretório atual
   - Mostra conteúdo do diretório

3. **Tratamento de exceção específico:**
   - Captura exceções específicas
   - Log do erro detalhado

---

## 🔍 Como Verificar

### 1. Ver Logs do Railway

**Railway → Deployments → View Logs**

**Procurar por:**
- `❌ Erro: Arquivo não encontrado`
- `📁 FRONTEND_DIR:`
- `📁 Diretório atual:`
- `📁 Conteúdo de FRONTEND_DIR:`

---

### 2. Verificar Caminho no Docker

**O Dockerfile copia:**
```dockerfile
COPY . .
```

**Isso copia tudo para `/app/`**

**Então o caminho deveria ser:**
```
/app/frontend/desktop_app/index.html
```

---

## 🎯 Próximos Passos

1. **Ver logs do Railway** após novo deploy
2. **Copiar logs** que mostram o erro
3. **Verificar** o caminho mostrado nos logs
4. **Ajustar** se necessário

---

**Correção aplicada com melhor tratamento de erros. Verifique os logs do Railway para ver o erro específico.**


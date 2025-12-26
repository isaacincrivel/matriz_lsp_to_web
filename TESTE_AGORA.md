# 🧪 Teste Agora - Guia Rápido

## ✅ Passo 1: Verificar se o Servidor Está Rodando

O servidor Flask foi iniciado em background. Para verificar:

### Opção A: Abrir no Navegador
Abra estas URLs no navegador (tente uma por vez):
- `http://localhost:8000/api/test/`
- `http://localhost:8001/api/test/`
- `http://localhost:8002/api/test/`

**Se funcionar, você verá:**
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

### Opção B: Verificar no Terminal
Se o servidor não estiver rodando, você verá uma mensagem de erro. Nesse caso:

1. **Abra um novo terminal**
2. **Execute:**
   ```bash
   python backend/api/server_flask.py
   ```
3. **Aguarde ver a mensagem:**
   ```
   📡 API disponível em: http://localhost:8000/api/gerar-matriz/
   ```

---

## ✅ Passo 2: Abrir o Frontend

### Opção A: Duplo Clique (Mais Simples)
1. Navegue até: `frontend/desktop_app/`
2. Dê **duplo clique** em `index.html`
3. O arquivo abrirá no navegador

### Opção B: Servidor HTTP (Recomendado)
1. Abra um **novo terminal**
2. Execute:
   ```bash
   cd frontend/desktop_app
   python -m http.server 8080
   ```
3. Acesse: `http://localhost:8080/`

---

## ✅ Passo 3: Testar o Sistema

### 1. Carregar KML
- Clique em **"📎 Clique ou arraste para importar kml"**
- Selecione um arquivo `.kml` ou `.kmz`
- Clique em **"Plotar Projeto"**
- ✅ **Resultado esperado:** Mapa aparece com vértices numerados

### 2. Preencher Dados
- Digite um número de módulo (ex: **"10105"**)
- ✅ **Resultado esperado:** Descrição aparece automaticamente
- Configure:
  - **Poste da derivação:** "Existente" ou "Implantar"
  - **Vão Frouxo:** "sim" ou "não"
- (Opcional) Selecione vértices em **"Não Intercalar Postes"**

### 3. Gerar Matriz
- Clique em **"Gerar Matriz"**
- ✅ **Resultado esperado:**
  - Botão muda para "Gerando Matriz..."
  - No console (F12) você verá logs
  - Arquivos CSV e KML são baixados automaticamente

---

## 🔍 Verificar no Console do Navegador

1. **Abra o DevTools** (F12)
2. **Vá para a aba "Console"**
3. **Clique em "Gerar Matriz"**
4. **Veja os logs:**

### ✅ Se tudo estiver OK:
```
Botão Gerar Matriz clicado
Parâmetros coletados: {...}
Procurando servidor nas portas 8000-8004...
✅ Servidor encontrado na porta 8000
Fazendo requisição para: http://localhost:8000/api/gerar-matriz/
Resposta recebida - Status: 200 OK
Resultado recebido: {success: true, ...}
Iniciando download CSV: T001_matriz_resultado.csv
✅ CSV baixado: T001_matriz_resultado.csv
Iniciando download KML: T001_quadrados_bissetriz.kml
✅ KML baixado: T001_quadrados_bissetriz.kml
```

### ❌ Se houver erro:
- **"Servidor Flask não encontrado"** → Verifique se o servidor está rodando
- **"Failed to fetch"** → Servidor não está respondendo
- **"Erro HTTP 500"** → Erro no backend (veja o terminal do servidor)

---

## 🐛 Problemas Comuns

### Servidor não está rodando
**Solução:**
```bash
# Abra um terminal e execute:
python backend/api/server_flask.py
```

### Porta já está em uso
**Solução:**
- O servidor vai automaticamente tentar a próxima porta (8001, 8002, etc)
- O frontend detecta automaticamente

### Arquivos não baixam
**Solução:**
- Verifique o console do navegador (F12)
- Certifique-se de que o bloqueador de pop-ups não está ativo
- Verifique se há espaço em disco

### Módulo não encontrado
**Solução:**
- Verifique se o código do módulo está correto
- Certifique-se de que `tabela-data.js` está carregado

---

## 📊 Checklist de Teste

Marque conforme testa:

- [ ] Servidor Flask está rodando (teste `/api/test/`)
- [ ] Frontend abre no navegador
- [ ] KML carrega e mostra no mapa
- [ ] Vértices aparecem numerados
- [ ] Módulo é encontrado ao digitar código
- [ ] Botão "Gerar Matriz" está habilitado
- [ ] Requisição é enviada para API (veja console)
- [ ] CSV é baixado automaticamente
- [ ] KML é baixado automaticamente
- [ ] Arquivos baixados abrem corretamente

---

## 🎯 Próximos Passos

Se tudo funcionar:
1. ✅ Sistema web está pronto para uso!
2. ✅ Pode usar normalmente
3. ✅ Pode fazer deploy (opcional)

Se houver problemas:
1. Verifique os logs do servidor no terminal
2. Verifique o console do navegador (F12)
3. Consulte `COMO_USAR_WEB.md` para mais detalhes

---

## 💡 Dica

**Mantenha dois terminais abertos:**
1. **Terminal 1:** Servidor Flask (`python backend/api/server_flask.py`)
2. **Terminal 2:** Servidor HTTP do frontend (opcional, se usar servidor HTTP)

**E uma janela do navegador:**
- Frontend aberto
- DevTools aberto (F12) para ver logs


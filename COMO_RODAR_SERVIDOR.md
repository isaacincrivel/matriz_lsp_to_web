# 🚀 Como Rodar o Servidor - Guia Rápido

## ⚡ Solução Recomendada: Usar Apenas o Flask

O servidor Flask já está configurado para servir tanto o **frontend** quanto a **API**. Use apenas um servidor:

### Opção 1: Usando variável de ambiente (Recomendado)

```powershell
cd C:\matriz_csv_to_kml
$env:PORT=8001; python backend\api\server_flask.py
```

Ou simplesmente:
```powershell
cd C:\matriz_csv_to_kml\backend\api
python server_flask.py
```
(O Flask vai encontrar uma porta disponível automaticamente entre 8000-8009)

### Opção 2: Usando o script batch

```powershell
cd C:\matriz_csv_to_kml
.\backend\api\start_server.bat
```

### 🌐 Acessar a aplicação:

Depois que o servidor iniciar, você verá uma mensagem como:
```
🚀 Servidor Flask iniciando...
📡 API disponível em: http://0.0.0.0:8001/api/gerar-matriz/
🧪 Teste: http://0.0.0.0:8001/api/test/
```

**Acesse no navegador:**
- **Frontend + API**: `http://localhost:8001/` ou `http://localhost:8001/index.html`
- **Teste da API**: `http://localhost:8001/api/test/`

---

## 🔧 Solução Alternativa: Dois Servidores Separados

Se você quiser usar dois servidores separados (não recomendado, mas funciona):

### Terminal 1 - Servidor Flask (API):
```powershell
cd C:\matriz_csv_to_kml\backend\api
$env:PORT=8001; python server_flask.py
```

### Terminal 2 - Servidor HTTP (Frontend):
```powershell
cd C:\matriz_csv_to_kml\frontend\desktop_app
python -m http.server 5500
```

### 🌐 Acessar:
- **Frontend**: `http://localhost:5500/index.html`
- **API**: O frontend vai detectar automaticamente na porta 8001

**⚠️ Nota**: Com dois servidores, você pode ter problemas de CORS, então a **Opção 1 é recomendada**.

---

## ✅ Verificar se está funcionando:

1. **Teste a API diretamente no navegador:**
   - Acesse: `http://localhost:8001/api/test/`
   - Deve retornar: `{"status":"ok","message":"Servidor Flask está funcionando","version":"1.0"}`

2. **Verifique o console do navegador (F12):**
   - Ao abrir a aplicação, deve aparecer: `✅ Servidor encontrado na porta 8001`

3. **Se não funcionar:**
   - Verifique se a porta não está sendo usada por outro programa
   - Feche outros terminais que possam estar usando a mesma porta
   - Reinicie o servidor Flask

---

## 🐛 Problemas Comuns:

### Erro: "Servidor não está respondendo"
- **Solução**: Certifique-se de que o servidor Flask está rodando
- Verifique se você vê a mensagem "API disponível em..." no terminal
- Teste acessar `http://localhost:8001/api/test/` diretamente no navegador

### Erro: "Porta já está em uso"
- **Solução**: Use outra porta ou feche o programa que está usando a porta
- Para usar outra porta: `$env:PORT=8002; python backend\api\server_flask.py`

### O frontend não encontra o backend
- **Solução**: Use apenas o Flask (Opção 1) em vez de dois servidores separados
- O Flask já serve o frontend e a API na mesma porta, evitando problemas de CORS


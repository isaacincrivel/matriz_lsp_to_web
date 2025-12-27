# ⚡ Teste Rápido - 3 Passos

## 🚀 Início Rápido

### 1️⃣ Instalar Dependências (uma vez só)

```powershell
pip install -r requirements.txt
```

### 2️⃣ Iniciar Backend

**Windows:**
```powershell
.\backend\api\start_server.bat
```

**Ou diretamente:**
```powershell
python backend\api\server_flask.py
```

**Você verá:**
```
🚀 Servidor Flask iniciando...
🔧 Modo: DESENVOLVIMENTO
📡 API disponível em: http://0.0.0.0:8000/api/gerar-matriz/
```

### 3️⃣ Abrir Frontend

**Opção A: Simples**
- Clique duas vezes em: `frontend\desktop_app\index.html`

**Opção B: Com Servidor HTTP (recomendado)**
```powershell
cd frontend\desktop_app
python -m http.server 3000
```
- Acesse: `http://localhost:3000`

---

## ✅ Verificar se Funcionou

### Backend:
Abra no navegador: `http://localhost:8000/api/test/`

Deve retornar:
```json
{"status": "ok", "message": "Servidor Flask está funcionando"}
```

### Frontend:
- Abra o console do navegador (F12)
- Deve aparecer: `✅ Servidor encontrado na porta 8000`

---

## 🎯 Pronto!

Agora você pode:
- ✅ Importar arquivos KML/CSV
- ✅ Gerar matriz
- ✅ Testar todas as funcionalidades

**O frontend detecta automaticamente o backend na porta 8000!**

---

**Para mais detalhes, veja: `TESTAR_LOCALMENTE.md`**


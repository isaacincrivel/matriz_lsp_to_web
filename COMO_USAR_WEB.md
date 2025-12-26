# 🌐 Como Usar a Versão Web

## 📋 Pré-requisitos

1. **Python 3.7+** instalado
2. **Dependências Python**:
   ```bash
   pip install flask flask-cors pandas
   ```

## 🚀 Iniciar o Servidor

### Windows
```bash
# Opção 1: Script batch (recomendado)
backend\api\start_server.bat

# Opção 2: Direto
python backend\api\server_flask.py
```

### Linux/Mac
```bash
# Opção 1: Script shell (recomendado)
chmod +x backend/api/start_server.sh
./backend/api/start_server.sh

# Opção 2: Direto
python3 backend/api/server_flask.py
```

### O que acontece?
- O servidor vai procurar uma porta disponível entre 8000-8009
- Você verá uma mensagem como: `📡 API disponível em: http://localhost:8000/api/gerar-matriz/`
- **Mantenha o terminal aberto** enquanto usa a aplicação

## 🌐 Abrir o Frontend

1. **Abra o arquivo HTML**:
   - Navegue até: `frontend/desktop_app/`
   - Dê duplo clique em `index.html`
   - Ou arraste para o navegador

2. **Ou use servidor HTTP simples** (recomendado para desenvolvimento):
   ```bash
   # No diretório frontend/desktop_app/
   python -m http.server 8080
   ```
   - Acesse: `http://localhost:8080/`

## 📝 Como Usar

1. **Carregue um arquivo KML**:
   - Clique em "📎 Clique ou arraste para importar kml"
   - Selecione seu arquivo .kml ou .kmz
   - Clique em "Plotar Projeto"

2. **Preencha os dados**:
   - Digite o número do módulo (ex: "10105")
   - A descrição aparecerá automaticamente
   - Configure "Poste da derivação" e "Vão Frouxo"
   - Selecione vértices em "Não Intercalar Postes" (se necessário)

3. **Gere a matriz**:
   - Clique em "Gerar Matriz"
   - O sistema vai:
     - Enviar dados para o servidor Flask
     - Processar no backend Python
     - Retornar CSV e KML
     - Fazer download automático dos arquivos

## ✅ Verificação

### Testar se o servidor está rodando:
Abra no navegador: `http://localhost:8000/api/test/`

Você deve ver:
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

### Verificar no console do navegador:
1. Abra o DevTools (F12)
2. Vá para a aba "Console"
3. Clique em "Gerar Matriz"
4. Veja os logs:
   - `Procurando servidor nas portas 8000-8004...`
   - `✅ Servidor encontrado na porta 8000`
   - `Fazendo requisição para: http://localhost:8000/api/gerar-matriz/`

## 🐛 Problemas Comuns

### "Servidor Flask não encontrado"
**Solução:**
- Certifique-se de que o servidor está rodando
- Verifique se a porta está correta (8000-8009)
- Veja o terminal onde o servidor está rodando para mensagens de erro

### "ModuleNotFoundError: No module named 'flask'"
**Solução:**
```bash
pip install flask flask-cors pandas
```

### "Porta já está em uso"
**Solução:**
- O servidor vai automaticamente tentar a próxima porta (8001, 8002, etc)
- O frontend vai detectar automaticamente em qual porta está

### Arquivos não baixam
**Solução:**
- Verifique o console do navegador (F12) para erros
- Certifique-se de que o bloqueador de pop-ups não está bloqueando downloads
- Verifique se há espaço em disco

## 📊 Arquitetura

```
Frontend (navegador)
    ↓ HTTP POST /api/gerar-matriz/
Backend Flask (Python)
    ↓ chama gerar_matriz()
Backend Core (Python)
    ↓ processa dados
Retorna CSV + KML (base64)
    ↓
Frontend recebe e faz download
```

## 🔄 Fluxo Completo

1. Usuário preenche formulário no navegador
2. JavaScript coleta dados do formulário
3. Frontend envia POST para `http://localhost:8000/api/gerar-matriz/`
4. Backend Flask recebe dados JSON
5. Backend chama `gerar_matriz()` do Python
6. Python processa e gera CSV/KML
7. Backend retorna arquivos em base64
8. Frontend decodifica e faz download

## 📚 Documentação Adicional

- [README da API](backend/api/README.md)
- [Estratégia de Desenvolvimento](ESTRATEGIA_DESENVOLVIMENTO.md)
- [Funções Relacionadas](FUNCOES_RELACIONADAS_DADOS_JSON.md)


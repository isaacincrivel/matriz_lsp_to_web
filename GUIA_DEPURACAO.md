# 🔍 Guia de Depuração - Sistema Matriz

Este guia explica como usar o sistema de depuração melhorado para identificar erros rapidamente.

## 📊 O que foi melhorado

### ✅ Backend (Python)
- **Logs detalhados** em cada etapa do processamento
- **Stack traces completos** quando há erros
- **Informações do erro** (arquivo, linha, função)
- **Try/catch** em cada função crítica

### ✅ Frontend (JavaScript)
- **Console logs** detalhados
- **Erros formatados** com informações do servidor
- **Grupos de log** para organização
- **Stack traces** completos

## 🔍 Como Depurar

### 1. **Console do Servidor Flask**

Quando você roda o servidor (`python backend/api/server_flask.py`), verá logs como:

```
[API] Gerando matriz para trecho: testexy, módulo: 10104
[API] Vértices recebidos: 9
[API] Parâmetros: loose_gap=NÃO, section_size=700, gap_size=80
🔵 ANTES dividir_tramo: 9 vértices
🟢 DEPOIS dividir_tramo: 11 vértices
🔵 Chamando marcar_vertices_angulo_deflexao() com 11 vértices...
```

**Se houver erro, você verá:**

```
================================================================================
❌ ERRO em marcar_vertices_angulo_deflexao():
Tipo: AttributeError, Mensagem: 'NoneType' object has no attribute 'get'
Parâmetros: gap_size=80, module_name=10104, lista_nao_intercalar=[]
Traceback (most recent call last):
  File "...", line 134, in marcar_vertices_angulo_deflexao
    encabecamento_sim_nao = resultado.get("tang_ou_enc")
                            ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
================================================================================
```

### 2. **Console do Navegador (F12)**

Abra o DevTools (F12) e vá para a aba **Console**.

**Logs normais:**
```
Botão Gerar Matriz clicado
Parâmetros coletados: {...}
Procurando servidor nas portas 8000-8004...
✅ Servidor encontrado na porta 8000
Fazendo requisição para: http://localhost:8000/api/gerar-matriz/
Resposta recebida - Status: 200 OK
```

**Se houver erro:**
```
❌ Erro da API: {
  success: false,
  message: "Erro ao gerar matriz: ...",
  error_type: "AttributeError",
  error_file: "C:\\...\\marcar_vertices_angulo_deflexao.py",
  error_line: "134",
  error_function: "marcar_vertices_angulo_deflexao",
  traceback: "..."
}

🔍 Detalhes do erro no servidor:
  Tipo: AttributeError
  Arquivo: C:\...\marcar_vertices_angulo_deflexao.py
  Linha: 134
  Função: marcar_vertices_angulo_deflexao
  Stack trace completo:
    ...
```

## 📍 Como Identificar o Local do Erro

### Passo 1: Olhe o Console do Servidor

O servidor mostra exatamente onde o erro aconteceu:

```
❌ ERRO em marcar_vertices_angulo_deflexao():
Tipo: AttributeError
Arquivo: backend/elementos/marcar_vertices_angulo_deflexao.py
Linha: 134
```

### Passo 2: Veja o Stack Trace

O stack trace mostra a cadeia completa de chamadas:

```
File "backend/api/server_flask.py", line 100, in gerar_matriz_api
  matriz = gerar_matriz(...)
File "backend/core/matriz_csv_to_kml.py", line 187, in gerar_matriz
  new_vertices = marcar_vertices_angulo_deflexao(...)
File "backend/elementos/marcar_vertices_angulo_deflexao.py", line 134, in marcar_vertices_angulo_deflexao
  encabecamento_sim_nao = resultado.get("tang_ou_enc")
                          ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
```

**Isso mostra:**
1. O erro aconteceu em `marcar_vertices_angulo_deflexao.py`, linha 134
2. Foi chamado por `matriz_csv_to_kml.py`, linha 187
3. Que foi chamado por `server_flask.py`, linha 100

### Passo 3: Veja os Parâmetros

O log também mostra os parâmetros que causaram o erro:

```
Parâmetros: gap_size=80, module_name=10104, lista_nao_intercalar=[]
```

## 🎯 Exemplo Prático

### Cenário: Erro "NoneType object has no attribute 'get'"

**Console do Servidor:**
```
🔵 Chamando marcar_vertices_angulo_deflexao() com 11 vértices...
ERRO: Não foi possível encontrar correspondência no ábaco para:
  - Ângulo: 368.95634665654717
  - Distância: 80
  - Módulo: 10104

================================================================================
❌ ERRO em marcar_vertices_angulo_deflexao():
Tipo: AttributeError, Mensagem: 'NoneType' object has no attribute 'get'
Parâmetros: gap_size=80, module_name=10104, lista_nao_intercalar=[]
Traceback (most recent call last):
  File "...marcar_vertices_angulo_deflexao.py", line 130, in marcar_vertices_angulo_deflexao
    resultado = mosaico(angulo_def, distancia_maior, module_name)
  File "...marcar_vertices_angulo_deflexao.py", line 134, in marcar_vertices_angulo_deflexao
    encabecamento_sim_nao = resultado.get("tang_ou_enc")
                            ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
================================================================================
```

**O que isso nos diz:**
1. ✅ **Onde:** `marcar_vertices_angulo_deflexao.py`, linha 134
2. ✅ **O que:** Tentou fazer `.get()` em `resultado` que é `None`
3. ✅ **Por quê:** `mosaico()` retornou `None` porque não encontrou correspondência no ábaco
4. ✅ **Dados:** Ângulo 368.96°, distância 80m, módulo 10104

**Solução:** Adicionar verificação `if resultado is not None:` antes de usar `.get()`

## 🔧 Dicas de Depuração

### 1. **Mantenha o Console do Servidor Visível**
- O terminal onde o Flask está rodando mostra os logs em tempo real
- Os erros aparecem lá primeiro

### 2. **Use o DevTools do Navegador**
- F12 → Console
- Veja os logs do frontend
- Veja os erros formatados do servidor

### 3. **Verifique os Parâmetros**
- Os logs mostram os parâmetros usados em cada função
- Se o erro acontece com certos parâmetros, isso ajuda a identificar o problema

### 4. **Siga o Stack Trace**
- Comece do erro (última linha)
- Suba pelas funções chamadoras
- Isso mostra o caminho completo que levou ao erro

### 5. **Use Breakpoints no Código**
Se quiser depurar linha por linha, adicione:

```python
import pdb; pdb.set_trace()  # Pausa aqui para depuração
```

No Python, ou:

```javascript
debugger;  // Pausa aqui para depuração (funciona no DevTools)
```

No JavaScript.

## 📋 Checklist de Depuração

Quando encontrar um erro:

- [ ] ✅ Veja o console do servidor Flask
- [ ] ✅ Veja o console do navegador (F12)
- [ ] ✅ Identifique o arquivo e linha do erro
- [ ] ✅ Veja o stack trace completo
- [ ] ✅ Verifique os parâmetros que causaram o erro
- [ ] ✅ Entenda o contexto (que função estava executando)
- [ ] ✅ Corrija o erro na linha identificada

## 🎯 Próximos Passos

Com esse sistema de logs melhorado, você pode:
1. Identificar rapidamente onde o erro aconteceu
2. Ver exatamente qual linha causou o problema
3. Entender o contexto (parâmetros, função chamadora)
4. Corrigir de forma precisa

Se precisar de mais ajuda, compartilhe:
- A mensagem de erro completa do console do servidor
- A linha que mostra o arquivo e número da linha
- O stack trace completo


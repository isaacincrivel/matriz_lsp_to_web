# 🔍 Guia de Depuração - Sistema Matriz

## 📋 Índice
1. [Depuração Frontend (JavaScript/HTML)](#frontend)
2. [Depuração Backend (Python)](#backend)
3. [Ferramentas Recomendadas](#ferramentas)

---

## 🌐 Frontend (JavaScript/HTML) {#frontend}

### 1. Console do Navegador (F12)

#### Como abrir:
- **Chrome/Edge**: Pressione `F12` ou `Ctrl+Shift+I`
- **Firefox**: Pressione `F12` ou `Ctrl+Shift+K`
- Botão direito → "Inspecionar" → Aba "Console"

#### O que fazer:

##### a) Verificar erros:
```javascript
// Procure por mensagens em vermelho
// Exemplos comuns:
- "Uncaught TypeError: ..."
- "Cannot read property '...' of undefined"
- "Failed to load resource: ..."
```

##### b) Usar console.log():
O código já tem vários logs. Veja no arquivo `app.js`:
```javascript
console.log('Página carregada, aguardando Leaflet...');
console.log('Leaflet carregado!');
console.log('Mapa inicializado com sucesso');
console.log('Botão Plotar Projeto clicado');
console.log('Arquivo selecionado:', file.name);
```

##### c) Verificar variáveis:
No console, digite:
```javascript
// Verificar se o mapa foi inicializado
map
mapInitialized

// Verificar se Leaflet carregou
L

// Verificar elementos do DOM
document.getElementById('line-map')
document.getElementById('btnPlotarProjeto')

// Verificar estado
pontosManuais
```

##### d) Executar comandos manualmente:
```javascript
// Inicializar mapa manualmente
initMap()

// Carregar KML manualmente (substitua 'file' pelo arquivo)
loadKMLOnMap(file)

// Verificar arquivo selecionado
fileInput.files[0]
```

### 2. Network Tab (Rede)

#### Verificar carregamento de recursos:
1. Abra DevTools (F12)
2. Vá para aba **Network** (Rede)
3. Recarregue a página (F5)
4. Verifique se todos os arquivos carregaram:
   - ✅ `libs/leaflet.js` - Status 200
   - ✅ `libs/leaflet.css` - Status 200
   - ✅ `libs/papaparse.min.js` - Status 200
   - ✅ `app.js` - Status 200

#### Se algum arquivo falhar:
- Status 404: Arquivo não encontrado (verifique caminho)
- Status 403: Permissão negada
- Status 500: Erro no servidor

### 3. Sources Tab (Fontes)

#### Breakpoints:
1. Abra DevTools (F12)
2. Vá para aba **Sources** (Fontes)
3. Localize o arquivo `app.js`
4. Clique no número da linha para adicionar breakpoint
5. Execute a ação que dispara o código
6. Use controles:
   - ▶️ Continue (F8)
   - ⏭️ Step Over (F10)
   - ⬇️ Step Into (F11)
   - ⬆️ Step Out (Shift+F11)

#### Pontos importantes para breakpoints:
```javascript
// Inicialização do mapa
initMap() - linha ~330

// Carregamento de KML
loadKMLOnMap() - linha ~455
parseAndDisplayKML() - linha ~485

// Event listeners
fileInput.addEventListener('change') - linha ~20
btnPlotarProjeto.addEventListener('click') - linha ~560
```

### 4. Elements Tab (Elementos)

#### Inspecionar HTML:
1. Abra DevTools (F12)
2. Vá para aba **Elements** (Elementos)
3. Clique no ícone de seleção (canto superior esquerdo)
4. Clique no elemento que quer inspecionar
5. Veja:
   - HTML gerado
   - Estilos CSS aplicados
   - Event listeners

#### Verificar se o mapa foi criado:
```html
<!-- Procure por: -->
<div id="line-map" ...>
  <!-- Deve ter uma div interna do Leaflet -->
</div>
```

### 5. Aplicar Estilos no Console

```javascript
// Verificar se elemento existe
document.getElementById('line-map')

// Forçar visibilidade
document.getElementById('line-map').style.display = 'block'
document.getElementById('line-map').style.height = '500px'
document.getElementById('line-map').style.width = '100%'

// Verificar se Leaflet criou o mapa
map
map._container
```

---

## 🐍 Backend (Python) {#backend}

### 1. Print Statements (Simples)

```python
# Adicione prints estratégicos
print("Debug: Variável x =", x)
print(f"Debug: {variavel}")
print("Debug: Chegou aqui")
```

### 2. Python Debugger (pdb)

```python
import pdb

# Coloque onde quer debugar
pdb.set_trace()

# Quando executar, o programa vai parar aqui
# Comandos úteis:
# n (next) - próxima linha
# s (step) - entra na função
# c (continue) - continua execução
# pp variavel - mostra valor da variável
# l (list) - mostra código ao redor
# q (quit) - sai do debugger
```

### 3. VS Code Debugger

#### Configurar launch.json:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

#### Usar:
1. Coloque breakpoints clicando na margem esquerda
2. Pressione `F5` para iniciar debug
3. Use controles na barra superior

### 4. Logging (Profissional)

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Usar
logger = logging.getLogger(__name__)
logger.debug("Mensagem de debug")
logger.info("Informação")
logger.warning("Aviso")
logger.error("Erro")
```

---

## 🛠️ Ferramentas Recomendadas {#ferramentas}

### Frontend:
- ✅ **Chrome DevTools** - F12 (melhor para depuração)
- ✅ **Firefox DevTools** - F12 (boa para CSS)
- ✅ **VS Code Live Server** - Extensão para servidor local
- ✅ **React DevTools** - Se usar React (não é o caso)

### Backend:
- ✅ **VS Code** - Editor com debugger integrado
- ✅ **PyCharm** - IDE Python com debugger avançado
- ✅ **ipdb** - Melhor que pdb (pip install ipdb)

### Outras:
- ✅ **Postman** - Testar APIs REST
- ✅ **Network Monitor** - DevTools Network tab

---

## 🔍 Checklist de Depuração Comum

### Mapa não aparece:
- [ ] Leaflet.js carregou? (Console: `typeof L !== 'undefined'`)
- [ ] Elemento #line-map existe? (`document.getElementById('line-map')`)
- [ ] mapInitialized é true? (`console.log(mapInitialized)`)
- [ ] Erros no Console?

### KML não carrega:
- [ ] Arquivo selecionado? (`fileInput.files[0]`)
- [ ] Mapa inicializado? (`map !== null`)
- [ ] Arquivo é válido? (Abra no Notepad++)
- [ ] Erros no Console?

### Botões não funcionam:
- [ ] Elemento existe? (`document.getElementById('btnNome')`)
- [ ] Event listener adicionado? (Verifique código)
- [ ] Botão habilitado? (`btn.disabled === false`)

---

## 📝 Logs Úteis para Adicionar

```javascript
// No início do app.js
console.log('=== INÍCIO DA APLICAÇÃO ===');
console.log('Elementos carregados:', {
    fileInput: !!fileInput,
    btnImportarArquivo: !!btnImportarArquivo,
    btnPlotarProjeto: !!btnPlotarProjeto,
    mapContainer: !!document.getElementById('line-map')
});

// Antes de inicializar mapa
console.log('=== INICIALIZANDO MAPA ===');
console.log('Leaflet disponível:', typeof L !== 'undefined');
console.log('Elemento mapa existe:', !!document.getElementById('line-map'));

// Ao carregar KML
console.log('=== CARREGANDO KML ===');
console.log('Arquivo:', file.name);
console.log('Tamanho:', file.size);
console.log('Tipo:', file.type);
```

---

## 🚨 Problemas Comuns e Soluções

### Erro: "L is not defined"
**Solução**: Leaflet não carregou. Verifique:
- Arquivo `libs/leaflet.js` existe?
- Está sendo carregado antes do `app.js`?

### Erro: "Cannot read property 'addTo' of undefined"
**Solução**: Mapa não foi inicializado. Verifique:
- `initMap()` foi chamada?
- `mapInitialized === true`?

### Mapa aparece vazio (cinza)
**Solução**: Tiles não carregam. Verifique:
- Conexão com internet (tiles vêm de servidor externo)
- Ou use tiles locais/offline

### KML não desenha no mapa
**Solução**: Verifique:
- Arquivo KML é válido?
- Console mostra erros?
- `parseAndDisplayKML()` foi chamada?
- Adicione breakpoint em `parseAndDisplayKML()`

---

## 💡 Dicas Finais

1. **Sempre verifique o Console primeiro** (F12)
2. **Use breakpoints** em pontos críticos
3. **Adicione logs** estratégicos (`console.log`)
4. **Teste em diferentes navegadores**
5. **Verifique Network tab** para recursos não carregados
6. **Limpe cache** se necessário (Ctrl+Shift+Delete)

---

## 📞 Próximos Passos

Se ainda tiver problemas:
1. Abra Console (F12)
2. Copie mensagens de erro completas
3. Informe em qual etapa o problema acontece
4. Compartilhe screenshot se possível


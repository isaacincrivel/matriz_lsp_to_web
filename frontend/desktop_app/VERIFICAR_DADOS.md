# 🔍 Como Verificar Onde Estão os Dados da Tabela

## Problema Identificado

Se o arquivo CSV tem poucas linhas, mas a tabela mostra muitas, os dados estão no **LocalStorage do navegador**.

## 📍 Onde os Dados Podem Estar:

### 1. **LocalStorage (Mais Provável)**
- **Local**: No navegador do usuário (cache)
- **Como verificar**: F12 → Console → Digite:
  ```javascript
  localStorage.getItem('tabela_dados')
  ```
- **Como limpar**: F12 → Console → Digite:
  ```javascript
  localStorage.removeItem('tabela_dados')
  location.reload()
  ```

### 2. **Arquivo CSV**
- **Local**: `frontend/desktop_app/data/tabela-dados.csv`
- **Linhas atuais**: 6 (1 cabeçalho + 5 dados)

### 3. **Dados Fictícios (Fallback)**
- **Local**: `frontend/desktop_app/tabela-data.js`
- **Linhas**: 150 linhas geradas automaticamente

## 🔄 Ordem de Carregamento:

1. **Primeiro**: LocalStorage (se existir)
2. **Segundo**: CSV (`data/tabela-dados.csv`)
3. **Terceiro**: Dados fictícios (se não encontrar CSV)

## ✅ Solução:

### Opção 1: Limpar LocalStorage e Recarregar do CSV
1. Abra a tabela no navegador
2. Pressione F12 (abrir DevTools)
3. Vá para a aba Console
4. Digite:
   ```javascript
   localStorage.removeItem('tabela_dados')
   location.reload()
   ```

### Opção 2: Usar Botão "Recarregar do CSV"
1. Clique no botão "🔄 Recarregar do CSV" na tabela
2. Isso limpa o LocalStorage e recarrega do CSV

### Opção 3: Adicionar Parâmetro na URL
Acesse: `tabela.html?reload=true`

## 📝 Para Ver Quantas Linhas Estão no LocalStorage:

No Console (F12):
```javascript
const dados = JSON.parse(localStorage.getItem('tabela_dados'))
console.log('Linhas no LocalStorage:', dados ? dados.length : 0)
```


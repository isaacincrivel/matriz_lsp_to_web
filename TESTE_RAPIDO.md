# 🧪 Teste Rápido - Sistema Web

## ✅ Status do Servidor

O servidor Flask está sendo iniciado em background.

## 📋 Passos para Testar

### 1. Verificar se o Servidor Está Rodando

Abra no navegador:
- `http://localhost:8000/api/test/`
- Ou `http://localhost:8001/api/test/` (se 8000 estiver ocupada)

Você deve ver:
```json
{
  "status": "ok",
  "message": "Servidor Flask está funcionando",
  "version": "1.0"
}
```

### 2. Abrir o Frontend

**Opção A: Duplo clique**
- Navegue até: `frontend/desktop_app/`
- Dê duplo clique em `index.html`

**Opção B: Servidor HTTP (recomendado)**
```bash
cd frontend/desktop_app
python -m http.server 8080
```
- Acesse: `http://localhost:8080/`

### 3. Testar o Fluxo Completo

1. **Carregue um KML**:
   - Clique em "📎 Clique ou arraste para importar kml"
   - Selecione um arquivo .kml ou .kmz
   - Clique em "Plotar Projeto"
   - ✅ Deve aparecer o mapa com vértices numerados

2. **Preencha os dados**:
   - Digite um número de módulo (ex: "10105")
   - ✅ A descrição deve aparecer automaticamente
   - Configure "Poste da derivação" e "Vão Frouxo"
   - Selecione vértices em "Não Intercalar Postes" (opcional)

3. **Gere a matriz**:
   - Clique em "Gerar Matriz"
   - ✅ Deve aparecer "Gerando Matriz..." no botão
   - ✅ No console (F12) você verá:
     - `Procurando servidor nas portas 8000-8004...`
     - `✅ Servidor encontrado na porta X`
     - `Fazendo requisição para: http://localhost:X/api/gerar-matriz/`
   - ✅ Os arquivos CSV e KML devem ser baixados automaticamente

## 🐛 Verificar Problemas

### Abra o Console do Navegador (F12)

**Se tudo estiver OK, você verá:**
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

**Se houver erro:**
- Verifique a mensagem de erro no console
- Verifique se o servidor está rodando
- Verifique se a porta está correta

## 📊 Teste Manual da API

Você pode testar a API diretamente usando o arquivo `dados_gerar_matriz.json`:

```bash
# No PowerShell
$json = Get-Content dados_gerar_matriz.json -Raw
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/gerar-matriz/" -Method POST -Body $json -ContentType "application/json" -UseBasicParsing
$response.Content
```

## ✅ Checklist de Teste

- [ ] Servidor Flask está rodando (teste `/api/test/`)
- [ ] Frontend abre no navegador
- [ ] KML carrega e mostra no mapa
- [ ] Vértices aparecem numerados
- [ ] Módulo é encontrado ao digitar código
- [ ] Botão "Gerar Matriz" está habilitado
- [ ] Requisição é enviada para API
- [ ] CSV é baixado automaticamente
- [ ] KML é baixado automaticamente
- [ ] Arquivos baixados estão corretos

## 🎯 Próximos Passos

Se tudo funcionar:
1. ✅ Sistema web está pronto para uso
2. ✅ Pode fazer deploy (opcional)
3. ✅ Pode adicionar mais funcionalidades

Se houver problemas:
1. Verifique os logs do servidor no terminal
2. Verifique o console do navegador (F12)
3. Consulte `COMO_USAR_WEB.md` para troubleshooting


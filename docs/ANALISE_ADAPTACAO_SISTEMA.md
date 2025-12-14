# Análise e Proposta de Adaptação do Sistema

## 📋 Sistema Atual (C:\matriz_kml_to_csv\Sistema-Matriz-main)

### Funcionalidades Existentes

1. **Interface Web Django**
   - Template `project.html` com Leaflet
   - Importação de KML (usando leaflet-omnivore)
   - Desenho de linhas no mapa
   - Geração de matriz em Excel (.xlsx)
   - Visualização de plotagem (KML)

2. **Backend Django**
   - Views para gerar matriz
   - Models (Project, Module)
   - Utils com lógica de processamento
   - Exportação de arquivos

3. **JavaScript**
   - `kml.js`: Importação e manipulação de KML
   - `get_matrix.js`: Geração de matriz via API
   - `get_module.js`: Busca de módulos
   - `load_data.js`: Carregamento de dados

### Limitações Identificadas

1. ❌ **Não é otimizado para mobile** - Interface desktop
2. ❌ **Gera Excel, não CSV** - Precisa gerar CSV no formato `matriz_teste.csv`
3. ❌ **Não permite edição de dados de postes** - Apenas visualização
4. ❌ **Não coleta dados de campo** - Não há formulários para entrada de dados por poste
5. ❌ **Não suporta múltiplos status** - Não permite Implantar/Existente/Retirar/Deslocar por poste

---

## 🎯 Funcionalidades Desejadas

### 1. Entrada de Dados no Campo
- ✅ Interface responsiva (mobile-first)
- ✅ Formulários para cada poste
- ✅ Múltiplos status por poste (Implantar, Existente, Retirar, Deslocar)
- ✅ Campos: tipo_poste, estruturas MT/BT, base_concreto, estai_ancora, etc.

### 2. Importação/Exportação KML
- ✅ Importar KML existente
- ✅ Exportar KML com dados coletados
- ✅ Plotagem no mapa Leaflet

### 3. Geração de CSV
- ✅ Formato compatível com `matriz_teste.csv`
- ✅ Separador: `;` (ponto e vírgula)
- ✅ Decimal: `,` (vírgula)
- ✅ Múltiplas linhas por sequência (uma por status)

---

## 🔧 Proposta de Adaptação

### Opção 1: Adicionar Nova View/Template (Recomendado)

Criar uma nova página no sistema Django para coleta de dados:

```
app/project/
├── templates/
│   ├── project.html (existente)
│   └── caminhamento.html (NOVO) ← Interface de coleta de dados
├── static/
│   └── js/
│       ├── caminhamento.js (NOVO) ← Lógica de coleta
│       └── csv-generator.js (NOVO) ← Geração de CSV
└── views.py
    └── caminhamento_view (NOVO) ← Nova view
```

**Vantagens:**
- ✅ Mantém sistema existente intacto
- ✅ Reutiliza estrutura Django
- ✅ Pode integrar com banco de dados existente
- ✅ Autenticação e sessões já configuradas

### Opção 2: Aplicação Standalone

Criar aplicação separada que gera CSV e depois importa no sistema.

**Vantagens:**
- ✅ Independente do Django
- ✅ Pode funcionar offline (PWA)
- ✅ Mais simples de desenvolver

**Desvantagens:**
- ❌ Não integra com sistema existente
- ❌ Duplicação de código

---

## 📝 Plano de Implementação (Opção 1 - Recomendada)

### Fase 1: Nova Interface de Caminhamento

1. **Criar template `caminhamento.html`**
   - Interface responsiva mobile-first
   - Mapa Leaflet otimizado para touch
   - Formulários modais para edição de postes
   - Lista de postes cadastrados

2. **Criar JavaScript `caminhamento.js`**
   - Controle do mapa
   - Importação/exportação KML
   - Gerenciamento de postes
   - Formulários dinâmicos

3. **Criar JavaScript `csv-generator.js`**
   - Geração de CSV no formato correto
   - Conversão de dados coletados para CSV
   - Download do arquivo

### Fase 2: Backend Django

1. **Nova View `caminhamento_view`**
   - Renderiza template de caminhamento
   - Endpoint para salvar dados coletados (opcional)

2. **Nova View `export_csv_view`**
   - Recebe dados via POST
   - Gera CSV no formato `matriz_teste.csv`
   - Retorna arquivo para download

3. **Atualizar `urls.py`**
   - Adicionar rotas para novas views

### Fase 3: Integração

1. **Compatibilidade com sistema existente**
   - CSV gerado deve ser compatível com `matriz_teste.csv`
   - Testar importação no sistema Python

2. **Melhorias de UX**
   - Armazenamento local (localStorage)
   - Sincronização com servidor (opcional)
   - PWA para funcionar offline

---

## 🔄 Fluxo de Trabalho Proposto

### Cenário 1: Importar KML e Coletar Dados

1. Usuário acessa `/caminhamento/`
2. Importa KML ou desenha linha no mapa
3. Clica em cada marcador (poste) no mapa
4. Preenche formulário com dados do poste
5. Pode adicionar múltiplos status por poste
6. Gera CSV e baixa arquivo
7. Importa CSV no sistema Python existente

### Cenário 2: Trabalho Offline

1. Usuário carrega página (tiles em cache)
2. Coleta dados no campo
3. Dados salvos localmente (localStorage)
4. Quando online, gera e baixa CSV

---

## 📊 Estrutura de Dados

### JSON Interno (armazenamento)
```json
{
  "postes": [
    {
      "sequencia": 0,
      "lat": -17.041935,
      "lon": -49.224541,
      "status": {
        "Implantar": {
          "tipo_poste": "N3",
          "estru_mt_nv1": "N3",
          "est_bt_nv1": "A1",
          "rotacao_poste": "topo1",
          "modulo": "mt7"
        },
        "Existente": {
          "num_poste": "46464546",
          "tipo_poste": "DT10/300",
          "estru_mt_nv1": "N1"
        }
      }
    }
  ]
}
```

### CSV Gerado (formato matriz_teste.csv)
```csv
sequencia;status;lat;long;num_poste;tipo_poste;estru_mt_nv1;...
0;Implantar;-17,041935;-49,224541;;;N3;...
0;Existente;;;46464546;DT10/300;N1;...
```

---

## ✅ Checklist de Implementação

### Prioridade Alta
- [ ] Criar template `caminhamento.html` responsivo
- [ ] Implementar mapa Leaflet otimizado para mobile
- [ ] Criar formulários para coleta de dados
- [ ] Implementar geração de CSV no formato correto
- [ ] Adicionar importação/exportação de KML

### Prioridade Média
- [ ] Armazenamento local (localStorage)
- [ ] Integração com backend Django
- [ ] Validação de dados
- [ ] Edição de postes existentes

### Prioridade Baixa
- [ ] PWA completo
- [ ] Sincronização com servidor
- [ ] Histórico de versões
- [ ] Exportação de projetos (JSON)

---

## 🚀 Próximos Passos

1. **Decidir abordagem**: Opção 1 (integrar no Django) ou Opção 2 (standalone)
2. **Criar estrutura básica**: Template e JavaScript
3. **Implementar funcionalidades core**: Mapa, formulários, CSV
4. **Testar compatibilidade**: CSV gerado com sistema Python
5. **Otimizar para mobile**: Responsividade e touch gestures

---

## 📝 Notas Técnicas

- **Formato CSV**: Separador `;`, decimal `,`, encoding UTF-8 com BOM
- **Leaflet**: Já está no sistema, apenas precisa adaptar
- **Django**: Sistema já configurado, adicionar novas views
- **Mobile**: Usar viewport meta tag e CSS responsivo
- **Offline**: Service Worker para PWA (opcional)


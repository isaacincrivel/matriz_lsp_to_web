# 📋 Sistema de Catalogação de Materiais por Estrutura

Sistema para identificar e catalogar materiais em estruturas de rede de distribuição elétrica, facilitando a geração de listas para desenho no CAD.

## 🎯 Objetivo

Permitir que você:
1. **Catalogar materiais** de cada estrutura (ex: B3CE-PR, UP1, UP4)
2. **Definir posições relativas** de cada material (coordenadas X, Y, Z)
3. **Gerar listas para CAD** em formato CSV ou DXF
4. **Integrar com o sistema existente** de matriz CSV to KML

## 📦 Estrutura

```
backend/elementos/
├── estrutura_materiais.py    # Módulo principal de catalogação
├── exemplo_b3ce_pr.py        # Exemplo de uso com estrutura B3CE-PR
└── README_ESTRUTURA_MATERIAIS.md  # Este arquivo
```

## 🚀 Uso Básico

### 1. Catalogar Materiais de uma Estrutura

```python
from backend.elementos.estrutura_materiais import catalogar_material_estrutura

# Exemplo: Estrutura UP1
materiais = {
    "F-30": {
        "descricao": "Ferramenta tipo 30",
        "tipo": "Ferramenta",
        "posicao": (0, 0, 800),  # X, Y, Z em mm
        "quantidade": 1,
        "angulo": 0.0,
        "observacoes": "Nível 1 - 13,8kV"
    },
    "A-02": {
        "descricao": "Acessório tipo 02",
        "tipo": "Acessório",
        "posicao": (500, 0, 800),
        "quantidade": 1
    }
}

catalogar_material_estrutura(
    codigo_estrutura="UP1",
    materiais=materiais,
    descricao_estrutura="Estrutura tipo UP1"
)
```

### 2. Exportar Lista para CAD

```python
from backend.elementos.estrutura_materiais import exportar_lista_cad

# Exportar para CSV
exportar_lista_cad(
    codigo_estrutura="UP1",
    nome_arquivo="lista_materiais_UP1.csv",
    formato="CSV"
)

# Exportar para DXF
exportar_lista_cad(
    codigo_estrutura="UP1",
    nome_arquivo="lista_materiais_UP1.dxf",
    formato="DXF"
)
```

### 3. Obter Lista de Materiais

```python
from backend.elementos.estrutura_materiais import obter_materiais_estrutura

materiais = obter_materiais_estrutura("UP1")
for material in materiais:
    print(f"{material['codigo']}: {material['descricao']}")
    print(f"  Posição: ({material['posicao_x']}, {material['posicao_y']}, {material['posicao_z']}) mm")
```

## 📐 Sistema de Coordenadas

### Coordenadas Relativas

- **X**: Distância horizontal do centro do poste (mm)
- **Y**: Distância lateral do centro do poste (mm)
- **Z**: Altura relativa ao solo (mm)

### Exemplo de Posicionamento

```
        Z (altura)
        ↑
        |
        |  F-30 (800mm)
        |
        |  A-02 (500mm)
        |
        |  C-01 (300mm)
        |
        |_________________→ X (horizontal)
       /
      /
     Y (lateral)
```

## 📊 Formato do CSV Exportado

O CSV gerado contém as seguintes colunas:

| Código | Descrição | Tipo | Posição X (mm) | Posição Y (mm) | Posição Z (mm) | Quantidade | Unidade | Ângulo (°) | Observações |
|--------|-----------|------|----------------|----------------|----------------|------------|---------|------------|-------------|
| F-30   | Ferramenta tipo 30 | Ferramenta | 0,00 | 0,00 | 800,00 | 1 | UN | 0,00 | Nível 1 |

## 🔧 Exemplo Completo: Estrutura B3CE-PR

Execute o exemplo:

```bash
python backend/elementos/exemplo_b3ce_pr.py
```

Isso irá:
1. Catalogar todos os materiais da estrutura B3CE-PR
2. Gerar arquivo CSV: `resultados/lista_materiais_B3CE-PR.csv`
3. Salvar catálogo completo: `resultados/catalogo_estruturas.json`

## 📝 Integração com Sistema Existente

### Usar com dados da matriz

```python
from backend.core.matriz_csv_to_kml import gerar_matriz
from backend.elementos.estrutura_materiais import (
    catalogar_material_estrutura,
    exportar_lista_cad
)

# Gera matriz normalmente
matriz = gerar_matriz(...)

# Para cada estrutura encontrada, catalogar materiais
for index, row in matriz.iterrows():
    estrutura = row.get('estru_mt_nv1', '')
    if estrutura:
        # Catalogar materiais baseado na estrutura
        materiais = {
            "F-30": {
                "descricao": "Ferramenta tipo 30",
                "tipo": "Ferramenta",
                "posicao": (0, 0, 800),
                "quantidade": 1
            }
        }
        catalogar_material_estrutura(estrutura, materiais)

# Exportar todas as estruturas
exportar_lista_cad(estrutura, f"lista_{estrutura}.csv")
```

## 💾 Persistência

### Salvar Catálogo

```python
from backend.elementos.estrutura_materiais import salvar_catalogo_arquivo

salvar_catalogo_arquivo("catalogo_estruturas.json")
```

### Carregar Catálogo

```python
from backend.elementos.estrutura_materiais import carregar_catalogo_arquivo

carregar_catalogo_arquivo("catalogo_estruturas.json")
```

## 🎨 Tipos de Materiais Suportados

- **Ferramenta**: Ferramentas e acessórios de montagem
- **Acessório**: Acessórios diversos
- **Isolador**: Isoladores
- **Condutor**: Condutores e cabos
- **Equipamento**: Equipamentos (transformadores, chaves, etc.)
- **Aterramento**: Materiais de aterramento
- **Base**: Bases de concreto ou reforçadas

## 📌 Dicas para Uso no CAD

1. **Importar CSV no Excel**: Abra o CSV no Excel para visualizar e filtrar
2. **Usar coordenadas relativas**: As coordenadas são relativas ao centro do poste
3. **Converter para coordenadas absolutas**: Se necessário, some as coordenadas base (lat, lon)
4. **Usar blocos no CAD**: Crie blocos para cada tipo de material
5. **Inserir por coordenadas**: Use as coordenadas X, Y, Z para posicionar blocos

## 🔍 Exemplo de Uso no AutoCAD

1. Abra o CSV no Excel
2. Copie as coordenadas X, Y, Z
3. No AutoCAD:
   ```
   INSERT [nome_do_bloco] [X] [Y] [Z]
   ```
4. Ou use script LISP para automatizar

## 📚 API Completa

### Funções Principais

- `catalogar_material_estrutura(codigo, materiais, descricao)`: Catalogar materiais
- `obter_materiais_estrutura(codigo)`: Obter lista de materiais
- `exportar_lista_cad(codigo, arquivo, coordenadas_base, formato)`: Exportar para CAD
- `salvar_catalogo_arquivo(arquivo)`: Salvar catálogo em JSON
- `carregar_catalogo_arquivo(arquivo)`: Carregar catálogo de JSON
- `obter_todas_estruturas()`: Obter todas as estruturas catalogadas

## ❓ Perguntas Frequentes

**Q: Como adicionar uma nova estrutura?**
A: Use `catalogar_material_estrutura()` com o código da nova estrutura.

**Q: Posso usar coordenadas absolutas?**
A: Sim, passe `coordenadas_base=(lat, lon)` em `exportar_lista_cad()`.

**Q: O formato DXF é completo?**
A: O DXF gerado é básico (pontos e texto). Para DXF completo, use bibliotecas como `ezdxf`.

**Q: Como integrar com outros sistemas?**
A: O catálogo é salvo em JSON, fácil de integrar com outras ferramentas.

## 🚧 Melhorias Futuras

- [ ] Suporte a DXF completo (usando `ezdxf`)
- [ ] Interface web para catalogação visual
- [ ] Importação de desenhos CAD para extrair materiais
- [ ] Validação automática de posições
- [ ] Geração de relatórios de materiais

## 📞 Suporte

Para dúvidas ou sugestões, consulte a documentação principal do projeto ou entre em contato com a equipe de desenvolvimento.

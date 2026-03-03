# Editor de Pontos da Matriz – Memória da Conversa

> **Status:** Planejamento – aguardando implementação. Tema será revisitado em breve.

---

## Contexto

- **Fluxo atual:** Google Earth (KML) → Importa na Matriz Web → Define módulo, não intercalar postes → Exporta CSV (+ KML)
- **CSV** é a fonte única: alimenta Matriz Web (KML) e ferramenta CAD (desenho)
- **Necessidade:** Permitir que o usuário edite um ponto (ex.: mover cabo da posição 1 para 2)
- **Regra:** Ao mover cabo, a estrutura acompanha (dinâmico); mudanças disparam recálculo mecânico (futuro)

---

## Regras de Acoplamento Cabo ↔ Estrutura

| Posição | Cabo | Estrutura |
|---------|------|-----------|
| 1A | CB_1A | EST_1A |
| 1B | CB_1B | EST_1B |
| ... | ... | ... |
| BT1A | CB_BT1A | EST_BT1A |

**Regra:** Mover cabo de X → Y implica: esvaziar X (cabo + estrutura), preencher Y com ambos.

---

## Modos de Edição Propostos

1. **Por número:** Usuário informa sequência do ponto → painel de edição
2. **Visual (mapa):** Clique no poste no mapa → popup/painel lateral
3. **Tabela editável:** Grid com linhas = pontos, colunas = CB/EST

---

## Propagação de Mudanças

```
Usuário move cabo 1A → 1B
  → CB_1A = ""; CB_1B = valor_antigo_CB_1A
  → EST_1A = ""; EST_1B = valor_antigo_EST_1A
  → [Futuro] Recalcular esforço mecânico
```

---

## Componentes Sugeridos

- Editor de ponto (formulário/modal)
- Camada de interação no mapa (clique no poste)
- Tabela editável (opcional)
- Motor de regras (cabo ↔ estrutura)
- Validador de consistência
- Módulo de esforço mecânico (futuro)

---

## Ordem de Evolução

1. **Fase 1:** Edição por número + regras cabo ↔ estrutura
2. **Fase 2:** Edição visual no mapa
3. **Fase 3:** Tabela editável
4. **Fase 4:** Integração esforço mecânico
5. **Fase 5:** IA/automação (sugestões, validações)

---

## Pontos a Decidir

- Onde editar: só Matriz Web ou também CAD?
- Propagação em tempo real ou ao salvar?
- Undo/Redo?
- Edição em lote?
- Tratamento das 4 linhas por vértice (implantar/existente/retirar/deslocar)

---

*Documento criado para preservar o planejamento. Não implementar sem autorização.*

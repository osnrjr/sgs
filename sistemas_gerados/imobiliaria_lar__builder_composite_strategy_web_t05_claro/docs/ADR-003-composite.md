# ADR 003 — Composite em Imobiliária Lar

- Status: aceito (exemplo de estudo gerado)
- Família: Padrão estrutural (GoF) — além das aulas; referência: lista GoF da Wikipédia

## Contexto
`total_antigo(coisa)` pergunta com `isinstance` se é lista ou Contrato e se chama de novo — cada operação nova (descrição, contagem) repete essa checagem.

## Decisão
APLICAMOS **Composite**. `Componente` define a interface comum (`preco`, `descricao`); `Unitario` (folha) embrulha uma Contrato; `Pacote` (composto) guarda filhos — folhas ou pacotes — e repassa a pergunta a eles.

## Alternativa descartada
Listas aninhadas + `isinstance` — cada operação repete a recursão.

## Consequências
Árvores de qualquer profundidade com uma interface só. Custo: a interface comum pode ficar genérica.
Quando NÃO usar: Lista plana, sem pacotes dentro de pacotes — `sum()` resolve.

## Onde está no código
`nucleo/pacotes.py` (antes: `nucleo/antes_pacotes.py`) · testes: `tests/test_pacotes.py`

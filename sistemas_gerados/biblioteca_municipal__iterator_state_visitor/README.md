# Biblioteca Municipal — sistema gerado

> Gerado por `sgs/gerar_sistema.py` v2.0 — **determinístico, sem IA**: a mesma
> entrada gera sempre os mesmos arquivos. Modo: para **estudo** (smell `antes_*.py`, ADRs, tripé) · código **comentado**.
> Padrões (4): Encapsulamento com @property, Iterator, State, Visitor.

## 1. Como o gerador decidiu

Escolha explícita: domínio **biblioteca**, padrões: encapsulamento, iterator, state, visitor.

## 2. Mapa dos arquivos

```
nucleo/
  entidades.py              ← Emprestimo com @property (base de tudo)
  colecao.py
  antes_colecao.py
  situacao.py
  antes_situacao.py
  orcamento.py
  antes_orcamento.py
tests/
  fabrica.py                ← cria Emprestimo válidas para os testes
  test_entidades.py
  test_colecao.py
  test_situacao.py
  test_orcamento.py
docs/                       ← um ADR por padrão
especificacao.json          ← a entrada usada (dá para editar e regenerar)
```

**Ligações entre os arquivos:**

- `tests/fabrica.py` cria `Emprestimo` válidas (`nucleo/entidades.py`) para TODOS os testes
- `nucleo/colecao.py` → `ColecaoEmprestimo` guarda `Emprestimo`s e entrega `IteradorDeItens`
- `nucleo/situacao.py` → `SituacaoEmprestimo` TEM-UMA `Emprestimo` e um `Estado`
- `nucleo/orcamento.py` → `LinhaEmprestimo` embrulha a `Emprestimo`; os visitantes percorrem o `Orcamento`

## 3. Como rodar

Com o `.venv` do projeto ativado (na raiz do projeto: `source .venv/bin/activate`), dentro desta pasta:

```bash
python -m pytest -v
```

## 4. Os padrões deste sistema

### 4.1 Encapsulamento com @property

_Fundamento de OO — Aulas 02 e 03_ · `nucleo/entidades.py` · testes: `tests/test_entidades.py`

**Problema (smell):** Um atributo público aceita qualquer valor: `obj.dias = 0` ou `obj.taxa_dia = -50` passariam e o `total` ficaria errado — a regra existiria só na cabeça de quem programa.

**Conceito:** O objeto controla o acesso ao próprio estado: cada atributo com regra vira `@property` + setter que valida ANTES de gravar no atributo interno `_nome`; o `__init__` usa `self.x = x` (passa pelo setter); `total` é property CALCULADA, sem setter.

| Peça | No código |
|---|---|
| Atributo interno | `self._dias`, `self._taxa_dia`… |
| Getter | `@property` |
| Setter (a fechadura) | `@dias.setter` → `ValueError` se inválido |
| Dado calculado | `total` (só leitura) |

**Quando NÃO usar:** Atributo sem regra (texto livre) fica simples — `@property` sem problema que a justifique é cerimônia. No model Django a regra vai em `validators`/`clean()`: setter em campo quebra ModelForm, admin e ORM.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Emprestimo.dias` (setter) | Intercepta toda escrita em `dias` e só grava se a regra for respeitada; senão levanta `ValueError`. | Encapsulamento: a regra mora no objeto, num lugar só; como o `__init__` faz `self.dias = ...`, vale também na criação. Descartado: validar só na tela. | Sem o setter, um valor inválido entra e o `total` sai errado; se o `__init__` gravar direto em `_dias`, o objeto pode nascer inválido. |
| `Emprestimo.total` | Calcula `dias × taxa_dia` na hora. | Dado derivado não se guarda: se fosse atributo, mudar `dias` deixaria o total desatualizado. | Virando atributo comum, dois dados podem discordar; com setter, alguém gravaria um total que não bate com a conta. |


### 4.2 Iterator

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/colecao.py` · antes: `nucleo/antes_colecao.py` · testes: `tests/test_colecao.py`

**Problema (smell):** `totais_antigo(colecao)` lê `colecao._itens[i]` por índice — depende da lista interna; trocar a estrutura quebra todos os laços.

**Conceito:** `ColecaoEmprestimo` esconde como guarda (dicionário por leitor) e entrega um ITERADOR (`IteradorDeItens`, com `__next__`) em `__iter__`. Percursos especiais (`acima_de`, `ordenados_por_total`) não expõem o interior.

| Peça | No código |
|---|---|
| Agregado | `ColecaoEmprestimo` |
| Iterador | `IteradorDeItens` (`__iter__`, `__next__`) |
| Percursos | `acima_de` (gerador), `ordenados_por_total` |

**Quando NÃO usar:** Lista e dicionário já são iteráveis em Python; classe de iterador só para percurso especial — um gerador (`yield`) é o atalho.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `IteradorDeItens.__next__()` | Devolve o próximo item e avança a posição; no fim levanta `StopIteration`. | Iterator: a posição fica no iterador, então dois `for` não se atrapalham. | Sem `StopIteration` o `for` não termina (ou dá IndexError); com a posição na coleção, dois percursos se misturariam. |


### 4.3 State

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/situacao.py` · antes: `nucleo/antes_situacao.py` · testes: `tests/test_situacao.py`

**Problema (smell):** `SituacaoAntiga` repete a mesma escada de `if/elif` sobre `self.status` em `confirmar`, `concluir` e `cancelar`.

**Conceito:** Cada estado é uma classe (`Aberto`, `Confirmado`, `Concluido`, `Cancelado`) que sabe as SUAS transições; `SituacaoEmprestimo` (contexto) guarda o estado atual e delega. Transição proibida levanta `TransicaoInvalida`.

| Peça | No código |
|---|---|
| Contexto | `SituacaoEmprestimo` |
| Estado base | `Estado` (tudo proibido por padrão) |
| Estados | `Aberto`, `Confirmado`, `Concluido`, `Cancelado` |

**Quando NÃO usar:** Dois estados e uma regra (um booleano basta). State × Strategy: no State o próprio estado troca o objeto do contexto; no Strategy quem escolhe é o cliente.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Aberto.confirmar(contexto)` | Troca o estado do contexto para `Confirmado`. | State: a transição pertence ao estado de origem; o contexto só delega. | Sem sobrescrever, valeria o padrão da base (TransicaoInvalida); trocando para `Concluido`, pularia a confirmação. |


### 4.4 Visitor

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/orcamento.py` · antes: `nucleo/antes_orcamento.py` · testes: `tests/test_orcamento.py`

**Problema (smell):** `total_antigo` e `texto_antigo` percorrem as linhas perguntando o tipo — cada operação nova repete a escada; cada tipo novo mexe em todas.

**Conceito:** Cada linha tem `aceitar(visitante)` e chama o método certo do visitante (despacho duplo); cada OPERAÇÃO é um visitante (`CalculoDoTotal`, `TextoDoOrcamento`) com um `visitar_*` por tipo.

| Peça | No código |
|---|---|
| Elementos | `LinhaEmprestimo`, `LinhaExtra`, `LinhaDesconto` (`aceitar`) |
| Estrutura | `Orcamento` |
| Visitantes | `CalculoDoTotal`, `TextoDoOrcamento` |
| Operação nova | `ContagemPorTipo` |

**Quando NÃO usar:** Tipos de elemento que mudam muito (cada tipo novo mexe em TODOS os visitantes) — prefira polimorfismo comum.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `LinhaExtra.aceitar(visitante)` | Chama `visitante.visitar_extra(self)`. | Visitor: o despacho duplo escolhe o método pelo tipo da linha E pelo visitante, sem `if`. | Chamando outro `visitar_*`, a linha seria tratada como outro tipo; sem `aceitar`, voltaria o `isinstance` em cada operação. |

## 5. Roteiro de estudo (30–40 min)

1. Abra cada `nucleo/antes_*.py` e diga **em voz alta** qual é o smell.
2. Abra a versão "depois" e aponte as **peças** do padrão (tabelas da seção 4).
3. **Preveja** o resultado de um teste antes de rodar; depois rode e confira.
4. Responda o **tripé** de cada função em voz alta (o que faz · por que assim · o que muda se).
5. Mude um número (um fator, um limite) e preveja **qual teste quebra**.
6. Gere de novo em modo exercício e refaça sem olhar:
   `python sgs/gerar_sistema.py --spec <caminho>/biblioteca_municipal__iterator_state_visitor/especificacao.json --exercicio --nome biblioteca_municipal__iterator_state_visitor_treino`


## Campo `Emprestimo.data_devolucao` (novo)

Regra: data_devolucao: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30) — `data-hora` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.

# Imobiliária Lar — sistema gerado

> Gerado por `sgs/gerar_sistema.py` v2.0 — **determinístico, sem IA**: a mesma
> entrada gera sempre os mesmos arquivos. Modo: para **estudo** (smell `antes_*.py`, ADRs, tripé) · código **comentado**.
> Padrões (4): Encapsulamento com @property, Builder, Composite, Strategy.

## 1. Como o gerador decidiu

Escolha explícita: domínio **imobiliaria**, padrões: encapsulamento, builder, composite, strategy.

> --django incluiu o Strategy: o Service da camada web reaproveita as políticas do núcleo.

## 2. Mapa dos arquivos

```
nucleo/
  entidades.py              ← Contrato com @property (base de tudo)
  construtor.py
  antes_construtor.py
  pacotes.py
  antes_pacotes.py
  politicas.py
  antes_politicas.py
tests/
  fabrica.py                ← cria Contrato válidas para os testes
  test_entidades.py
  test_construtor.py
  test_pacotes.py
  test_politicas.py
docs/                       ← um ADR por padrão
especificacao.json          ← a entrada usada (dá para editar e regenerar)
requirements.txt            ← o Python exigido, o Django e o que ele usa, os testes e as deste sistema
iniciar.sh                  ← prepara e sobe o site: venv · deps · .env · migrations · admin
web/                        ← projeto Django (MVT) que usa o núcleo
  .env.example              ← modelo do .env (chave secreta, admin, porta)
  contratos/  settings · models · forms · services · viewmodels · views · api (REST) · urls · templates/ · tests/
```

**Ligações entre os arquivos:**

- `tests/fabrica.py` cria `Contrato` válidas (`nucleo/entidades.py`) para TODOS os testes
- `nucleo/construtor.py` → `ContratoBuilder` cria a `Contrato` de `nucleo/entidades.py`
- `nucleo/pacotes.py` → `Unitario` embrulha a `Contrato`; `Pacote` guarda componentes
- `nucleo/politicas.py` → `Cobranca` usa `item.total` da `Contrato`
- `web/contratos/services.py` importa as políticas de `nucleo/politicas.py` (Strategy) → `viewmodels.py` prepara a tela → `views.py` só orquestra → os templates exibem

## 3. Como rodar

Com o `.venv` do projeto ativado (na raiz do projeto: `source .venv/bin/activate`), dentro desta pasta:

```bash
python -m pytest -v
```

## 4. Os padrões deste sistema

### 4.1 Encapsulamento com @property

_Fundamento de OO — Aulas 02 e 03_ · `nucleo/entidades.py` · testes: `tests/test_entidades.py`

**Problema (smell):** Um atributo público aceita qualquer valor: `obj.meses = 0` ou `obj.valor_aluguel = -50` passariam e o `total` ficaria errado — a regra existiria só na cabeça de quem programa.

**Conceito:** O objeto controla o acesso ao próprio estado: cada atributo com regra vira `@property` + setter que valida ANTES de gravar no atributo interno `_nome`; o `__init__` usa `self.x = x` (passa pelo setter); `total` é property CALCULADA, sem setter.

| Peça | No código |
|---|---|
| Atributo interno | `self._meses`, `self._valor_aluguel`… |
| Getter | `@property` |
| Setter (a fechadura) | `@meses.setter` → `ValueError` se inválido |
| Dado calculado | `total` (só leitura) |

**Quando NÃO usar:** Atributo sem regra (texto livre) fica simples — `@property` sem problema que a justifique é cerimônia. No model Django a regra vai em `validators`/`clean()`: setter em campo quebra ModelForm, admin e ORM.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Contrato.meses` (setter) | Intercepta toda escrita em `meses` e só grava se a regra for respeitada; senão levanta `ValueError`. | Encapsulamento: a regra mora no objeto, num lugar só; como o `__init__` faz `self.meses = ...`, vale também na criação. Descartado: validar só na tela. | Sem o setter, um valor inválido entra e o `total` sai errado; se o `__init__` gravar direto em `_meses`, o objeto pode nascer inválido. |
| `Contrato.total` | Calcula `meses × valor_aluguel` na hora. | Dado derivado não se guarda: se fosse atributo, mudar `meses` deixaria o total desatualizado. | Virando atributo comum, dois dados podem discordar; com setter, alguém gravaria um total que não bate com a conta. |


### 4.2 Builder

_Padrão de criação (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/construtor.py` · antes: `nucleo/antes_construtor.py` · testes: `tests/test_construtor.py`

**Problema (smell):** `nova_contrato_antiga(...)` recebe os campos na ORDEM certa; trocar dois números de lugar cria uma Contrato válida porém errada, e não há valores padrão.

**Conceito:** `ContratoBuilder` tem um `com_<campo>()` por atributo, cada um devolvendo o próprio builder (interface fluente); `construir()` confere o que falta e só então cria a Contrato. `DiretorDeContrato` guarda receitas prontas.

| Peça | No código |
|---|---|
| Builder | `ContratoBuilder` (`com_…`, `faltando`, `construir`) |
| Produto | `Contrato` |
| Diretor | `DiretorDeContrato.basico(...)` |

**Quando NÃO usar:** Objeto com poucos campos: em Python, argumentos NOMEADOS já resolvem a ordem.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `ContratoBuilder.construir()` | Confere os campos obrigatórios e cria a Contrato com os valores juntados. | Builder: separa o passo a passo da montagem da criação final; cada valor continua validado pelos setters. | Sem `faltando()`, o erro seria um TypeError confuso do construtor; se `com_…` não devolvesse `self`, não daria para encadear. |


### 4.3 Composite

_Padrão estrutural (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/pacotes.py` · antes: `nucleo/antes_pacotes.py` · testes: `tests/test_pacotes.py`

**Problema (smell):** `total_antigo(coisa)` pergunta com `isinstance` se é lista ou Contrato e se chama de novo — cada operação nova (descrição, contagem) repete essa checagem.

**Conceito:** `Componente` define a interface comum (`preco`, `descricao`); `Unitario` (folha) embrulha uma Contrato; `Pacote` (composto) guarda filhos — folhas ou pacotes — e repassa a pergunta a eles.

| Peça | No código |
|---|---|
| Componente | `Componente` |
| Folha | `Unitario(item)` |
| Composto | `Pacote(nome, desconto)` com `adicionar` |
| Recursão | `Pacote.preco()` soma `filho.preco()` |

**Quando NÃO usar:** Lista plana, sem pacotes dentro de pacotes — `sum()` resolve.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Pacote.preco()` | Soma o preço de cada filho (que pode ser outro pacote) e aplica o desconto do pacote. | Composite: folha e composto respondem `preco()`, então a soma não pergunta o tipo e a recursão acontece sozinha. | Com `isinstance` aqui o pacote voltaria a conhecer os tipos; sem `round`, centavos se acumulariam. |


### 4.4 Strategy

_Padrão comportamental (GoF) — Aula 05_ · `nucleo/politicas.py` · antes: `nucleo/antes_politicas.py` · testes: `tests/test_politicas.py`

**Problema (smell):** `CobrancaAntiga.valor()` tem um `if/elif` por tipo de cliente que cresce a cada regra nova — cada uma obriga a reabrir a classe.

**Conceito:** Cada regra vira uma classe com o MESMO método `aplicar(base)`; `Cobranca` (o contexto) RECEBE a política e DELEGA: `self.politica.aplicar(self.item.total)` — sem `if`.

| Peça | No código |
|---|---|
| Contexto | `Cobranca` |
| Interface da estratégia | `aplicar(base)` |
| Estratégias | `PoliticaResidencial`, `PoliticaComercial`, `PoliticaEstudante` |
| Estratégia nova (OCP) | `PoliticaCorporativo` |
| Versão pythônica | `CobrancaComFuncao` (estratégia = função) |

**Quando NÃO usar:** Uma regra só, que nunca varia → uma função ou constante basta (Strategy seria cerimônia). Em Python a estratégia pode ser uma função.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Cobranca.valor()` | Pega o `total` da Contrato e devolve o valor depois da política aplicada. | Strategy: a família de regras de tipo de cliente varia; cada uma é uma classe e o contexto delega, sem `if`. | Voltando ao `if/elif` os números seguem iguais, mas toda política nova reabre a classe (perde OCP). Trocar `cobranca.politica` muda o valor sem criar outra cobrança. |

## 5. Roteiro de estudo (30–40 min)

1. Abra cada `nucleo/antes_*.py` e diga **em voz alta** qual é o smell.
2. Abra a versão "depois" e aponte as **peças** do padrão (tabelas da seção 4).
3. **Preveja** o resultado de um teste antes de rodar; depois rode e confira.
4. Responda o **tripé** de cada função em voz alta (o que faz · por que assim · o que muda se).
5. Mude um número (um fator, um limite) e preveja **qual teste quebra**.
6. Gere de novo em modo exercício e refaça sem olhar:
   `python sgs/gerar_sistema.py --spec <caminho>/imobiliaria_lar__builder_composite_strategy_web_t05_claro/especificacao.json --exercicio --nome imobiliaria_lar__builder_composite_strategy_web_t05_claro_treino`

## 6. Camada web (Django · MVT)

| Camada | Arquivo | Papel |
|---|---|---|
| Model | `web/contratos/models.py` | campos com **validators** (encapsulamento no mundo Django) + `total` calculado |
| Form | `web/contratos/forms.py` | `ModelForm` reaproveita os validators |
| Service | `web/contratos/services.py` | regra sem web; reaproveita o **Strategy** do núcleo |
| ViewModel | `web/contratos/viewmodels.py` | prepara título, valor formatado, selo e rodapé |
| View | `web/contratos/views.py` | **fina**: busca → Service/ViewModel → render |
| API REST | `web/contratos/api.py` | JSON em `api/v1/` (GET/POST) e `api/v1/<id>/` (GET/PUT/PATCH/DELETE), validado pelo **mesmo** Form |
| Settings da app | `web/contratos/settings.py` | `API_LIMITE` e `API_ESCRITA`, trocáveis no projeto com o prefixo `CONTRATOS_` |
| Template | `web/contratos/templates/contratos/` | só exibe |

Pegadinha testada em `tests/test_models.py`: `save()` sozinho **não** valida — quem valida é
`full_clean()` / o `ModelForm`.

### Subir o site (no WSL, dentro desta pasta)

Tudo de uma vez — cria o `.venv`, instala o `requirements.txt`, copia `web/.env.example` para
`web/.env` (com uma chave secreta nova), roda as migrations, cria o superusuário e sobe o servidor:

```bash
bash iniciar.sh
```

O site abre sozinho em **modo PWA** — uma janela de app isolada das abas (Edge/Chrome `--app`); com
`PWA=0` no `web/.env` abre numa aba comum, e `ABRIR=0 bash iniciar.sh` não abre nada. Endereços:
http://127.0.0.1:8000/ (site) e http://127.0.0.1:8000/admin/ (usuário e senha do `web/.env`:
`DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD`). Outra porta: `bash iniciar.sh tudo 8001`.
O site é instalável (manifest em `/manifest.webmanifest`, service worker em `/sw.js`, ícones em `static/`).

Os mesmos passos, separados (cada um pode ser repetido sem estragar nada):

```bash
bash iniciar.sh venv        # cria .venv nesta pasta (se não existir)
bash iniciar.sh deps        # instala requirements.txt (se faltar algo)
bash iniciar.sh env         # web/.env a partir de web/.env.example (não sobrescreve)
bash iniciar.sh migrar      # makemigrations contratos + migrate
bash iniciar.sh admin       # cria/atualiza o superusuário com os dados do web/.env
bash iniciar.sh testar      # testes do núcleo e da web
bash iniciar.sh rodar 8000  # sobe o servidor (Ctrl+C para parar)
```

Sem o script (comandos puros do Django):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp web/.env.example web/.env
cd web
python manage.py makemigrations contratos && python manage.py migrate
python manage.py garantir_admin
python manage.py runserver 127.0.0.1:8000
```

Reaproveitar um `.venv` que já tem Django (ex.: o do SGS, `sgs/.venv`):
`VENV=/caminho/.venv bash iniciar.sh`. As dependências estão explicadas no `requirements.txt` (o Python
exigido, o Django e o que ele usa, os testes e as pontuais deste sistema).


## Campo `Contrato.descricao_completa` (novo)

Regra: descricao_completa: texto longo obrigatório (descrição/memo) — `texto-longo` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.


## Campo `Contrato.foto_capa` (novo)

Regra: foto_capa: caminho ou URL de imagem (.png, .jpg, .jpeg, .webp, .gif, .svg) — `imagem` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.

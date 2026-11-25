# Escola Saber — sistema gerado

> Gerado por `sgs/gerar_sistema.py` v2.0 — **determinístico, sem IA**: a mesma
> entrada gera sempre os mesmos arquivos. Modo: para **estudo** (smell `antes_*.py`, ADRs, tripé) · código **comentado**.
> Padrões (4): Encapsulamento com @property, Mediator, Strategy, Template Method.

## 1. Como o gerador decidiu

Escolha explícita: domínio **escola**, padrões: encapsulamento, mediator, strategy, template_method.

> --django incluiu o Strategy: o Service da camada web reaproveita as políticas do núcleo.

## 2. Mapa dos arquivos

```
nucleo/
  entidades.py              ← Turma com @property (base de tudo)
  mediador.py
  antes_mediador.py
  politicas.py
  antes_politicas.py
  fechamento.py
  antes_fechamento.py
tests/
  fabrica.py                ← cria Turma válidas para os testes
  test_entidades.py
  test_mediador.py
  test_politicas.py
  test_fechamento.py
docs/                       ← um ADR por padrão
especificacao.json          ← a entrada usada (dá para editar e regenerar)
requirements.txt            ← o Python exigido, o Django e o que ele usa, os testes e as deste sistema
iniciar.sh                  ← prepara e sobe o site: venv · deps · .env · migrations · admin
web/                        ← projeto Django (MVT) que usa o núcleo
  .env.example              ← modelo do .env (chave secreta, admin, porta)
  turmas/  settings · models · forms · services · viewmodels · views · api (REST) · urls · templates/ · tests/
```

**Ligações entre os arquivos:**

- `tests/fabrica.py` cria `Turma` válidas (`nucleo/entidades.py`) para TODOS os testes
- `nucleo/mediador.py` → os componentes avisam o `FormularioMediador` (independente da entidade)
- `nucleo/politicas.py` → `Cobranca` usa `item.total` da `Turma`
- `nucleo/fechamento.py` → `Fechamento.fechar` lê `item.total` da `Turma`
- `web/turmas/services.py` importa as políticas de `nucleo/politicas.py` (Strategy) → `viewmodels.py` prepara a tela → `views.py` só orquestra → os templates exibem

## 3. Como rodar

Com o `.venv` do projeto ativado (na raiz do projeto: `source .venv/bin/activate`), dentro desta pasta:

```bash
python -m pytest -v
```

## 4. Os padrões deste sistema

### 4.1 Encapsulamento com @property

_Fundamento de OO — Aulas 02 e 03_ · `nucleo/entidades.py` · testes: `tests/test_entidades.py`

**Problema (smell):** Um atributo público aceita qualquer valor: `obj.meses = 0` ou `obj.mensalidade = -50` passariam e o `total` ficaria errado — a regra existiria só na cabeça de quem programa.

**Conceito:** O objeto controla o acesso ao próprio estado: cada atributo com regra vira `@property` + setter que valida ANTES de gravar no atributo interno `_nome`; o `__init__` usa `self.x = x` (passa pelo setter); `total` é property CALCULADA, sem setter.

| Peça | No código |
|---|---|
| Atributo interno | `self._meses`, `self._mensalidade`… |
| Getter | `@property` |
| Setter (a fechadura) | `@meses.setter` → `ValueError` se inválido |
| Dado calculado | `total` (só leitura) |

**Quando NÃO usar:** Atributo sem regra (texto livre) fica simples — `@property` sem problema que a justifique é cerimônia. No model Django a regra vai em `validators`/`clean()`: setter em campo quebra ModelForm, admin e ORM.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Turma.meses` (setter) | Intercepta toda escrita em `meses` e só grava se a regra for respeitada; senão levanta `ValueError`. | Encapsulamento: a regra mora no objeto, num lugar só; como o `__init__` faz `self.meses = ...`, vale também na criação. Descartado: validar só na tela. | Sem o setter, um valor inválido entra e o `total` sai errado; se o `__init__` gravar direto em `_meses`, o objeto pode nascer inválido. |
| `Turma.total` | Calcula `meses × mensalidade` na hora. | Dado derivado não se guarda: se fosse atributo, mudar `meses` deixaria o total desatualizado. | Virando atributo comum, dois dados podem discordar; com setter, alguém gravaria um total que não bate com a conta. |


### 4.2 Mediator

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/mediador.py` · antes: `nucleo/antes_mediador.py` · testes: `tests/test_mediador.py`

**Problema (smell):** O campo de meses conhece o seletor, o resumo e o botão e mexe neles direto — todos acoplados a todos; componente novo obriga a mexer nos outros.

**Conceito:** Cada componente só conhece o MEDIADOR e avisa `notificar(self, evento)`; `FormularioMediador` decide quem reage (recalcula o resumo, liga/desliga o botão).

| Peça | No código |
|---|---|
| Mediador | `FormularioMediador` |
| Componentes | `CampoMeses`, `SeletorTipo`, `Resumo`, `BotaoConfirmar` |
| Aviso | `mediador.notificar(origem, evento)` |

**Quando NÃO usar:** 2–3 objetos que conversam pouco. Cuidado para o mediador não virar um "objeto deus".

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `FormularioMediador.notificar(origem, evento)` | Recalcula o resumo (meses × preço × fator do tipo) e só habilita o botão se a meses for válida. | Mediator: a coordenação fica num lugar; os componentes não se conhecem. | Se o campo voltasse a atualizar o resumo direto, perderia a reutilização; esquecendo o botão aqui, ele ficaria ligado com valor inválido. |


### 4.3 Strategy

_Padrão comportamental (GoF) — Aula 05_ · `nucleo/politicas.py` · antes: `nucleo/antes_politicas.py` · testes: `tests/test_politicas.py`

**Problema (smell):** `CobrancaAntiga.valor()` tem um `if/elif` por tipo de bolsa que cresce a cada regra nova — cada uma obriga a reabrir a classe.

**Conceito:** Cada regra vira uma classe com o MESMO método `aplicar(base)`; `Cobranca` (o contexto) RECEBE a política e DELEGA: `self.politica.aplicar(self.item.total)` — sem `if`.

| Peça | No código |
|---|---|
| Contexto | `Cobranca` |
| Interface da estratégia | `aplicar(base)` |
| Estratégias | `PoliticaRegular`, `PoliticaIrmaos`, `PoliticaBolsista` |
| Estratégia nova (OCP) | `PoliticaFilhoDeProfessor` |
| Versão pythônica | `CobrancaComFuncao` (estratégia = função) |

**Quando NÃO usar:** Uma regra só, que nunca varia → uma função ou constante basta (Strategy seria cerimônia). Em Python a estratégia pode ser uma função.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Cobranca.valor()` | Pega o `total` da Turma e devolve o valor depois da política aplicada. | Strategy: a família de regras de tipo de bolsa varia; cada uma é uma classe e o contexto delega, sem `if`. | Voltando ao `if/elif` os números seguem iguais, mas toda política nova reabre a classe (perde OCP). Trocar `cobranca.politica` muda o valor sem criar outra cobrança. |


### 4.4 Template Method

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/fechamento.py` · antes: `nucleo/antes_fechamento.py` · testes: `tests/test_fechamento.py`

**Problema (smell):** `fechar_padrao_antigo` e `fechar_com_taxa_antigo` são cópias do mesmo roteiro (validar → calcular → ajustar → formatar); corrigir um passo exige lembrar de todas as cópias.

**Conceito:** `Fechamento.fechar(item)` é o método TEMPLATE: fixa a ordem dos passos; as subclasses sobrescrevem só o passo que muda (`ajustar`), e o gancho tem padrão vazio.

| Peça | No código |
|---|---|
| Classe abstrata | `Fechamento` |
| Método template | `fechar(item)` |
| Passos / gancho | `validar`, `calcular`, `ajustar` (gancho), `formatar` |
| Subclasses | `FechamentoPadrao`, `FechamentoComTaxa`, `FechamentoIrmaos` |

**Quando NÃO usar:** Só um passo varia — passe uma função (Strategy). Template Method usa HERANÇA; Strategy, COMPOSIÇÃO.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Fechamento.fechar(item)` | Chama validar, calcular, ajustar e formatar, nessa ordem. | Template Method: o esqueleto é fixo e as subclasses preenchem só os passos variáveis. | Se uma subclasse sobrescrever `fechar`, perde-se a garantia da ordem; esquecendo `validar`, total inválido passaria. |

## 5. Roteiro de estudo (30–40 min)

1. Abra cada `nucleo/antes_*.py` e diga **em voz alta** qual é o smell.
2. Abra a versão "depois" e aponte as **peças** do padrão (tabelas da seção 4).
3. **Preveja** o resultado de um teste antes de rodar; depois rode e confira.
4. Responda o **tripé** de cada função em voz alta (o que faz · por que assim · o que muda se).
5. Mude um número (um fator, um limite) e preveja **qual teste quebra**.
6. Gere de novo em modo exercício e refaça sem olhar:
   `python sgs/gerar_sistema.py --spec <caminho>/escola_saber__mediator_strategy_template_method_web_t06_tom2/especificacao.json --exercicio --nome escola_saber__mediator_strategy_template_method_web_t06_tom2_treino`

## 6. Camada web (Django · MVT)

| Camada | Arquivo | Papel |
|---|---|---|
| Model | `web/turmas/models.py` | campos com **validators** (encapsulamento no mundo Django) + `total` calculado |
| Form | `web/turmas/forms.py` | `ModelForm` reaproveita os validators |
| Service | `web/turmas/services.py` | regra sem web; reaproveita o **Strategy** do núcleo |
| ViewModel | `web/turmas/viewmodels.py` | prepara título, valor formatado, selo e rodapé |
| View | `web/turmas/views.py` | **fina**: busca → Service/ViewModel → render |
| API REST | `web/turmas/api.py` | JSON em `api/v1/` (GET/POST) e `api/v1/<id>/` (GET/PUT/PATCH/DELETE), validado pelo **mesmo** Form |
| Settings da app | `web/turmas/settings.py` | `API_LIMITE` e `API_ESCRITA`, trocáveis no projeto com o prefixo `TURMAS_` |
| Template | `web/turmas/templates/turmas/` | só exibe |

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
bash iniciar.sh migrar      # makemigrations turmas + migrate
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
python manage.py makemigrations turmas && python manage.py migrate
python manage.py garantir_admin
python manage.py runserver 127.0.0.1:8000
```

Reaproveitar um `.venv` que já tem Django (ex.: o do SGS, `sgs/.venv`):
`VENV=/caminho/.venv bash iniciar.sh`. As dependências estão explicadas no `requirements.txt` (o Python
exigido, o Django e o que ele usa, os testes e as pontuais deste sistema).


## Campo `Turma.portal_url` (novo)

Regra: portal_url: URL válida começando com http:// ou https:// — `url` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.


## Campo `Turma.comprovante` (novo)

Regra: comprovante: caminho ou URL de arquivo/anexo com extensão (ex.: relatorio.pdf) — `arquivo` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.

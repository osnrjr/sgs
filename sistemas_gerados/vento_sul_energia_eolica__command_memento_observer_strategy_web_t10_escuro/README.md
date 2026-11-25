# Vento Sul Energia Eólica — sistema gerado

> Gerado por `sgs/gerar_sistema.py` v2.0 — **determinístico, sem IA**: a mesma
> entrada gera sempre os mesmos arquivos. Modo: para **estudo** (smell `antes_*.py`, ADRs, tripé) · código **comentado**.
> Padrões (5): Encapsulamento com @property, Command, Memento, Observer, Strategy.

## 1. Como o gerador decidiu

Escolha explícita: domínio **energia_eolica**, padrões: encapsulamento, command, memento, observer, strategy.

> --django incluiu o Strategy: o Service da camada web reaproveita as políticas do núcleo.

## 2. Mapa dos arquivos

```
nucleo/
  entidades.py              ← ParqueAerogerador com @property (base de tudo)
  comandos.py
  antes_comandos.py
  versoes.py
  antes_versoes.py
  eventos.py
  antes_eventos.py
  politicas.py
  antes_politicas.py
tests/
  fabrica.py                ← cria ParqueAerogerador válidas para os testes
  test_entidades.py
  test_comandos.py
  test_versoes.py
  test_eventos.py
  test_politicas.py
docs/                       ← um ADR por padrão
especificacao.json          ← a entrada usada (dá para editar e regenerar)
requirements.txt            ← o Python exigido, o Django e o que ele usa, os testes e as deste sistema
iniciar.sh                  ← prepara e sobe o site: venv · deps · .env · migrations · admin
web/                        ← projeto Django (MVT) que usa o núcleo
  .env.example              ← modelo do .env (chave secreta, admin, porta)
  parque_aerogeradores/  settings · models · forms · services · viewmodels · views · api (REST) · urls · templates/ · tests/
```

**Ligações entre os arquivos:**

- `tests/fabrica.py` cria `ParqueAerogerador` válidas (`nucleo/entidades.py`) para TODOS os testes
- `nucleo/comandos.py` → `AlterarCampo` muda a `ParqueAerogerador` pelos setters; `Historico` empilha
- `nucleo/versoes.py` → `EditorParqueAerogerador` salva/restaura o estado da `ParqueAerogerador` em `Memento`s
- `nucleo/eventos.py` → `ParqueAerogeradorObservavel` embrulha a `ParqueAerogerador` e avisa os observadores
- `nucleo/politicas.py` → `Cobranca` usa `item.total` da `ParqueAerogerador`
- `web/parque_aerogeradores/services.py` importa as políticas de `nucleo/politicas.py` (Strategy) → `viewmodels.py` prepara a tela → `views.py` só orquestra → os templates exibem

## 3. Como rodar

Com o `.venv` do projeto ativado (na raiz do projeto: `source .venv/bin/activate`), dentro desta pasta:

```bash
python -m pytest -v
```

## 4. Os padrões deste sistema

### 4.1 Encapsulamento com @property

_Fundamento de OO — Aulas 02 e 03_ · `nucleo/entidades.py` · testes: `tests/test_entidades.py`

**Problema (smell):** Um atributo público aceita qualquer valor: `obj.megawatts = 0` ou `obj.preco_mwh = -50` passariam e o `total` ficaria errado — a regra existiria só na cabeça de quem programa.

**Conceito:** O objeto controla o acesso ao próprio estado: cada atributo com regra vira `@property` + setter que valida ANTES de gravar no atributo interno `_nome`; o `__init__` usa `self.x = x` (passa pelo setter); `total` é property CALCULADA, sem setter.

| Peça | No código |
|---|---|
| Atributo interno | `self._megawatts`, `self._preco_mwh`… |
| Getter | `@property` |
| Setter (a fechadura) | `@megawatts.setter` → `ValueError` se inválido |
| Dado calculado | `total` (só leitura) |

**Quando NÃO usar:** Atributo sem regra (texto livre) fica simples — `@property` sem problema que a justifique é cerimônia. No model Django a regra vai em `validators`/`clean()`: setter em campo quebra ModelForm, admin e ORM.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `ParqueAerogerador.megawatts` (setter) | Intercepta toda escrita em `megawatts` e só grava se a regra for respeitada; senão levanta `ValueError`. | Encapsulamento: a regra mora no objeto, num lugar só; como o `__init__` faz `self.megawatts = ...`, vale também na criação. Descartado: validar só na tela. | Sem o setter, um valor inválido entra e o `total` sai errado; se o `__init__` gravar direto em `_megawatts`, o objeto pode nascer inválido. |
| `ParqueAerogerador.total` | Calcula `megawatts × preco_mwh` na hora. | Dado derivado não se guarda: se fosse atributo, mudar `megawatts` deixaria o total desatualizado. | Virando atributo comum, dois dados podem discordar; com setter, alguém gravaria um total que não bate com a conta. |


### 4.2 Command

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/comandos.py` · antes: `nucleo/antes_comandos.py` · testes: `tests/test_comandos.py`

**Problema (smell):** `alterar_antigo(item, campo, valor)` muda a ParqueAerogerador direto e a ação some — sem registro do valor anterior, não dá para desfazer.

**Conceito:** Cada ação vira um OBJETO (`AlterarCampo`) que sabe `executar()` e `desfazer()` (guarda o valor anterior). `Historico` (o invocador) empilha os comandos e faz desfazer/refazer em ordem.

| Peça | No código |
|---|---|
| Comando | `Comando` → `AlterarCampo` |
| Invocador | `Historico` (`executar`, `desfazer`, `refazer`) |
| Receptor | a `ParqueAerogerador` (setters validam) |

**Quando NÃO usar:** Ação simples que nunca será desfeita, enfileirada ou registrada — chame o método direto.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Historico.executar(comando)` | Executa o comando e só então o empilha; limpa a pilha de refazer. | Command: a ação é um objeto, então pode ser guardada, desfeita e refeita. | Empilhando antes de executar, um comando inválido entraria no histórico; sem limpar `_desfeitos`, refazer misturaria linhas do tempo. |


### 4.3 Memento

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/versoes.py` · antes: `nucleo/antes_versoes.py` · testes: `tests/test_versoes.py`

**Problema (smell):** Para "voltar atrás", quem usa copia os campos internos (`_campo`) da ParqueAerogerador num dicionário — depende do interior dela e esquece campos novos.

**Conceito:** `EditorParqueAerogerador` (originador) cria um `Memento` com a cópia do próprio estado e sabe restaurá-lo; `HistoricoDeVersoes` (zelador) só empilha mementos, sem olhar dentro.

| Peça | No código |
|---|---|
| Originador | `EditorParqueAerogerador` (`salvar`, `restaurar`) |
| Memento | `Memento` (estado + rótulo) |
| Zelador | `HistoricoDeVersoes` |

**Quando NÃO usar:** Estado grande e muitas versões (memória). Memento × Command: o Command desfaz UMA ação; o Memento volta o estado inteiro.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `EditorParqueAerogerador.salvar(rotulo)` | Cria um Memento com uma CÓPIA profunda do estado atual. | Memento: só o originador conhece o próprio estado; o zelador guarda sem abrir. | Sem `deepcopy`, o memento apontaria para o mesmo estado e mudaria junto; guardando os campos fora, o encapsulamento se perde. |


### 4.4 Observer

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/eventos.py` · antes: `nucleo/antes_eventos.py` · testes: `tests/test_eventos.py`

**Problema (smell):** `alterar_antigo(...)` chama painel e log um por um — conhece todos os interessados; um interessado novo obriga a editar a função.

**Conceito:** `ParqueAerogeradorObservavel` (sujeito) guarda a lista de observadores e, a cada mudança, chama `atualizar(evento)` em todos. Interessado novo = `inscrever(obj)`; o sujeito não muda.

| Peça | No código |
|---|---|
| Sujeito | `ParqueAerogeradorObservavel` (`inscrever`, `cancelar`, `notificar`) |
| Observadores | `PainelObservador`, `LogObservador`, `AlertaObservador` |
| Evento | dict com campo, valor, total anterior e total |

**Quando NÃO usar:** Um interessado único e fixo — chame-o direto. Cadeias de observadores escondem o fluxo.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `ParqueAerogeradorObservavel.alterar(campo, valor)` | Altera a ParqueAerogerador (validando) e avisa todos os inscritos com um evento. | Observer: o sujeito não sabe quem escuta; cada observador reage do seu jeito. | Notificando ANTES do setter, um valor inválido seria anunciado; sem copiar a lista, quem se cancelasse no meio faria pular um observador. |


### 4.5 Strategy

_Padrão comportamental (GoF) — Aula 05_ · `nucleo/politicas.py` · antes: `nucleo/antes_politicas.py` · testes: `tests/test_politicas.py`

**Problema (smell):** `CobrancaAntiga.valor()` tem um `if/elif` por tipo de contrato que cresce a cada regra nova — cada uma obriga a reabrir a classe.

**Conceito:** Cada regra vira uma classe com o MESMO método `aplicar(base)`; `Cobranca` (o contexto) RECEBE a política e DELEGA: `self.politica.aplicar(self.item.total)` — sem `if`.

| Peça | No código |
|---|---|
| Contexto | `Cobranca` |
| Interface da estratégia | `aplicar(base)` |
| Estratégias | `PoliticaPadrao`, `PoliticaCorporativo`, `PoliticaRecorrente` |
| Estratégia nova (OCP) | `PoliticaEmergencial` |
| Versão pythônica | `CobrancaComFuncao` (estratégia = função) |

**Quando NÃO usar:** Uma regra só, que nunca varia → uma função ou constante basta (Strategy seria cerimônia). Em Python a estratégia pode ser uma função.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Cobranca.valor()` | Pega o `total` da ParqueAerogerador e devolve o valor depois da política aplicada. | Strategy: a família de regras de tipo de contrato varia; cada uma é uma classe e o contexto delega, sem `if`. | Voltando ao `if/elif` os números seguem iguais, mas toda política nova reabre a classe (perde OCP). Trocar `cobranca.politica` muda o valor sem criar outra cobrança. |

## 5. Roteiro de estudo (30–40 min)

1. Abra cada `nucleo/antes_*.py` e diga **em voz alta** qual é o smell.
2. Abra a versão "depois" e aponte as **peças** do padrão (tabelas da seção 4).
3. **Preveja** o resultado de um teste antes de rodar; depois rode e confira.
4. Responda o **tripé** de cada função em voz alta (o que faz · por que assim · o que muda se).
5. Mude um número (um fator, um limite) e preveja **qual teste quebra**.
6. Gere de novo em modo exercício e refaça sem olhar:
   `python sgs/gerar_sistema.py --spec <caminho>/vento_sul_energia_eolica__command_memento_observer_strategy_web_t10_escuro/especificacao.json --exercicio --nome vento_sul_energia_eolica__command_memento_observer_strategy_web_t10_escuro_treino`

## 6. Camada web (Django · MVT)

| Camada | Arquivo | Papel |
|---|---|---|
| Model | `web/parque_aerogeradores/models.py` | campos com **validators** (encapsulamento no mundo Django) + `total` calculado |
| Form | `web/parque_aerogeradores/forms.py` | `ModelForm` reaproveita os validators |
| Service | `web/parque_aerogeradores/services.py` | regra sem web; reaproveita o **Strategy** do núcleo |
| ViewModel | `web/parque_aerogeradores/viewmodels.py` | prepara título, valor formatado, selo e rodapé |
| View | `web/parque_aerogeradores/views.py` | **fina**: busca → Service/ViewModel → render |
| API REST | `web/parque_aerogeradores/api.py` | JSON em `api/v1/` (GET/POST) e `api/v1/<id>/` (GET/PUT/PATCH/DELETE), validado pelo **mesmo** Form |
| Settings da app | `web/parque_aerogeradores/settings.py` | `API_LIMITE` e `API_ESCRITA`, trocáveis no projeto com o prefixo `PARQUE_AEROGERADORES_` |
| Template | `web/parque_aerogeradores/templates/parque_aerogeradores/` | só exibe |

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
bash iniciar.sh migrar      # makemigrations parque_aerogeradores + migrate
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
python manage.py makemigrations parque_aerogeradores && python manage.py migrate
python manage.py garantir_admin
python manage.py runserver 127.0.0.1:8000
```

Reaproveitar um `.venv` que já tem Django (ex.: o do SGS, `sgs/.venv`):
`VENV=/caminho/.venv bash iniciar.sh`. As dependências estão explicadas no `requirements.txt` (o Python
exigido, o Django e o que ele usa, os testes e as pontuais deste sistema).


## Campo `ParqueAerogerador.geoloc` (novo)

Regra: geoloc: coordenadas latitude,longitude (-90..90, -180..180) — `geolocalizacao` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.


## Campo `ParqueAerogerador.parametros_json` (novo)

Regra: parametros_json: objeto ou lista JSON estruturada (dict ou list) — `json` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.

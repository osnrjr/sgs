# Farmácia Saúde — sistema gerado

> Gerado por `sgs/gerar_sistema.py` v2.0 — **determinístico, sem IA**: a mesma
> entrada gera sempre os mesmos arquivos. Modo: para **estudo** (smell `antes_*.py`, ADRs, tripé) · código **comentado**.
> Padrões (4): Encapsulamento com @property, Proxy, Chain of Responsibility, Strategy.

## 1. Como o gerador decidiu

Escolha explícita: domínio **farmacia**, padrões: encapsulamento, proxy, chain, strategy.

> --django incluiu o Strategy: o Service da camada web reaproveita as políticas do núcleo.

## 2. Mapa dos arquivos

```
nucleo/
  entidades.py              ← Receita com @property (base de tudo)
  acesso.py
  antes_acesso.py
  aprovacao.py
  antes_aprovacao.py
  politicas.py
  antes_politicas.py
tests/
  fabrica.py                ← cria Receita válidas para os testes
  test_entidades.py
  test_acesso.py
  test_aprovacao.py
  test_politicas.py
docs/                       ← um ADR por padrão
especificacao.json          ← a entrada usada (dá para editar e regenerar)
requirements.txt            ← o Python exigido, o Django e o que ele usa, os testes e as deste sistema
iniciar.sh                  ← prepara e sobe o site: venv · deps · .env · migrations · admin
web/                        ← projeto Django (MVT) que usa o núcleo
  .env.example              ← modelo do .env (chave secreta, admin, porta)
  receitas/  settings · models · forms · services · viewmodels · views · api (REST) · urls · templates/ · tests/
```

**Ligações entre os arquivos:**

- `tests/fabrica.py` cria `Receita` válidas (`nucleo/entidades.py`) para TODOS os testes
- `nucleo/acesso.py` → os proxies embrulham `ConsultaDePreco`, que lê `item.total`
- `nucleo/aprovacao.py` → a cadeia de `Aprovador` lê `item.total`
- `nucleo/politicas.py` → `Cobranca` usa `item.total` da `Receita`
- `web/receitas/services.py` importa as políticas de `nucleo/politicas.py` (Strategy) → `viewmodels.py` prepara a tela → `views.py` só orquestra → os templates exibem

## 3. Como rodar

Com o `.venv` do projeto ativado (na raiz do projeto: `source .venv/bin/activate`), dentro desta pasta:

```bash
python -m pytest -v
```

## 4. Os padrões deste sistema

### 4.1 Encapsulamento com @property

_Fundamento de OO — Aulas 02 e 03_ · `nucleo/entidades.py` · testes: `tests/test_entidades.py`

**Problema (smell):** Um atributo público aceita qualquer valor: `obj.unidades = 0` ou `obj.preco_unitario = -50` passariam e o `total` ficaria errado — a regra existiria só na cabeça de quem programa.

**Conceito:** O objeto controla o acesso ao próprio estado: cada atributo com regra vira `@property` + setter que valida ANTES de gravar no atributo interno `_nome`; o `__init__` usa `self.x = x` (passa pelo setter); `total` é property CALCULADA, sem setter.

| Peça | No código |
|---|---|
| Atributo interno | `self._unidades`, `self._preco_unitario`… |
| Getter | `@property` |
| Setter (a fechadura) | `@unidades.setter` → `ValueError` se inválido |
| Dado calculado | `total` (só leitura) |

**Quando NÃO usar:** Atributo sem regra (texto livre) fica simples — `@property` sem problema que a justifique é cerimônia. No model Django a regra vai em `validators`/`clean()`: setter em campo quebra ModelForm, admin e ORM.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Receita.unidades` (setter) | Intercepta toda escrita em `unidades` e só grava se a regra for respeitada; senão levanta `ValueError`. | Encapsulamento: a regra mora no objeto, num lugar só; como o `__init__` faz `self.unidades = ...`, vale também na criação. Descartado: validar só na tela. | Sem o setter, um valor inválido entra e o `total` sai errado; se o `__init__` gravar direto em `_unidades`, o objeto pode nascer inválido. |
| `Receita.total` | Calcula `unidades × preco_unitario` na hora. | Dado derivado não se guarda: se fosse atributo, mudar `unidades` deixaria o total desatualizado. | Virando atributo comum, dois dados podem discordar; com setter, alguém gravaria um total que não bate com a conta. |


### 4.2 Proxy

_Padrão estrutural (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/acesso.py` · antes: `nucleo/antes_acesso.py` · testes: `tests/test_acesso.py`

**Problema (smell):** Quem consulta faz o cache e confere a permissão na mão, misturado com a chamada — cada ponto de uso repete (ou esquece) essas regras.

**Conceito:** `ConsultaComCache` e `ConsultaProtegida` têm o MESMO `calcular(item)` do objeto real (`ConsultaDePreco`); por dentro guardam respostas ou barram perfis e só então repassam. Quem usa nem percebe — e os proxies empilham.

| Peça | No código |
|---|---|
| Sujeito real | `ConsultaDePreco` |
| Proxy de cache | `ConsultaComCache` |
| Proxy de proteção | `ConsultaProtegida` |

**Quando NÃO usar:** Acesso simples, sem custo nem regra. Proxy × Decorator: o Decorator ACRESCENTA comportamento; o Proxy CONTROLA o acesso ao objeto real.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `ConsultaComCache.calcular(item)` | Devolve o valor guardado; se ainda não tem, pergunta ao objeto real e guarda. | Proxy: mesma interface do real, então substitui o original sem o cliente mudar. | Com a chave só pelo cliente, mudar a unidades devolveria valor velho; sem guardar, todo pedido iria ao real. |


### 4.3 Chain of Responsibility

_Padrão comportamental (GoF) — além das aulas; referência: lista GoF da Wikipédia_ · `nucleo/aprovacao.py` · antes: `nucleo/antes_aprovacao.py` · testes: `tests/test_aprovacao.py`

**Problema (smell):** `quem_aprova_antigo(item)` tem todas as alçadas num `if/elif`; incluir um nível (ex.: supervisor) obriga a reescrever a função.

**Conceito:** Cada `Aprovador` conhece só a SUA alçada e o PRÓXIMO elo: se pode, aprova; senão, repassa. A cadeia é montada de fora (`encadear`) — incluir ou tirar um nível não mexe nos outros.

| Peça | No código |
|---|---|
| Elo base | `Aprovador` (`encadear`, `aprovar`) |
| Elos | `Atendente`, `Gerente`, `Diretoria` |
| Nível novo | `Supervisor` |
| Montagem | `cadeia_padrao()` |

**Quando NÃO usar:** Poucas regras fixas — um `if/elif` curto é mais legível. O pedido pode chegar ao fim da cadeia sem ninguém tratar.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Aprovador.aprovar(item)` | Aprova se o total cabe na alçada; senão repassa ao próximo; no fim devolve "sem aprovador". | Chain of Responsibility: cada elo decide sozinho e não conhece a cadeia inteira. | Sem testar `proximo is None`, o último elo quebraria com AttributeError; trocando a ordem dos elos, muda quem aprova. |


### 4.4 Strategy

_Padrão comportamental (GoF) — Aula 05_ · `nucleo/politicas.py` · antes: `nucleo/antes_politicas.py` · testes: `tests/test_politicas.py`

**Problema (smell):** `CobrancaAntiga.valor()` tem um `if/elif` por tipo de cliente que cresce a cada regra nova — cada uma obriga a reabrir a classe.

**Conceito:** Cada regra vira uma classe com o MESMO método `aplicar(base)`; `Cobranca` (o contexto) RECEBE a política e DELEGA: `self.politica.aplicar(self.item.total)` — sem `if`.

| Peça | No código |
|---|---|
| Contexto | `Cobranca` |
| Interface da estratégia | `aplicar(base)` |
| Estratégias | `PoliticaComum`, `PoliticaConvenio`, `PoliticaIdoso` |
| Estratégia nova (OCP) | `PoliticaFarmaciaPopular` |
| Versão pythônica | `CobrancaComFuncao` (estratégia = função) |

**Quando NÃO usar:** Uma regra só, que nunca varia → uma função ou constante basta (Strategy seria cerimônia). Em Python a estratégia pode ser uma função.

**Tripé arquitetural** (o que faz · por que assim · o que muda):

| Função | O que faz | Por que assim | O que muda se alterar |
|---|---|---|---|
| `Cobranca.valor()` | Pega o `total` da Receita e devolve o valor depois da política aplicada. | Strategy: a família de regras de tipo de cliente varia; cada uma é uma classe e o contexto delega, sem `if`. | Voltando ao `if/elif` os números seguem iguais, mas toda política nova reabre a classe (perde OCP). Trocar `cobranca.politica` muda o valor sem criar outra cobrança. |

## 5. Roteiro de estudo (30–40 min)

1. Abra cada `nucleo/antes_*.py` e diga **em voz alta** qual é o smell.
2. Abra a versão "depois" e aponte as **peças** do padrão (tabelas da seção 4).
3. **Preveja** o resultado de um teste antes de rodar; depois rode e confira.
4. Responda o **tripé** de cada função em voz alta (o que faz · por que assim · o que muda se).
5. Mude um número (um fator, um limite) e preveja **qual teste quebra**.
6. Gere de novo em modo exercício e refaça sem olhar:
   `python sgs/gerar_sistema.py --spec <caminho>/farmacia_saude__proxy_chain_strategy_web_t08_escuro/especificacao.json --exercicio --nome farmacia_saude__proxy_chain_strategy_web_t08_escuro_treino`

## 6. Camada web (Django · MVT)

| Camada | Arquivo | Papel |
|---|---|---|
| Model | `web/receitas/models.py` | campos com **validators** (encapsulamento no mundo Django) + `total` calculado |
| Form | `web/receitas/forms.py` | `ModelForm` reaproveita os validators |
| Service | `web/receitas/services.py` | regra sem web; reaproveita o **Strategy** do núcleo |
| ViewModel | `web/receitas/viewmodels.py` | prepara título, valor formatado, selo e rodapé |
| View | `web/receitas/views.py` | **fina**: busca → Service/ViewModel → render |
| API REST | `web/receitas/api.py` | JSON em `api/v1/` (GET/POST) e `api/v1/<id>/` (GET/PUT/PATCH/DELETE), validado pelo **mesmo** Form |
| Settings da app | `web/receitas/settings.py` | `API_LIMITE` e `API_ESCRITA`, trocáveis no projeto com o prefixo `RECEITAS_` |
| Template | `web/receitas/templates/receitas/` | só exibe |

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
bash iniciar.sh migrar      # makemigrations receitas + migrate
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
python manage.py makemigrations receitas && python manage.py migrate
python manage.py garantir_admin
python manage.py runserver 127.0.0.1:8000
```

Reaproveitar um `.venv` que já tem Django (ex.: o do SGS, `sgs/.venv`):
`VENV=/caminho/.venv bash iniciar.sh`. As dependências estão explicadas no `requirements.txt` (o Python
exigido, o Django e o que ele usa, os testes e as pontuais deste sistema).


## Campo `Receita.cnpj_fornecedor` (novo)

Regra: cnpj_fornecedor: CNPJ válido com 14 dígitos e dígitos verificadores — `cnpj` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.


## Campo `Receita.metadados` (novo)

Regra: metadados: objeto ou lista JSON estruturada (dict ou list) — `json` (sgs incrementar). Vale no @property do núcleo, no model (validators/choices), no form e na API; os testes da classe foram refeitos.

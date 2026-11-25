# SGS — Sistema Gerador de Sistemas

O **SGS** gera projetos completos em **Python + Django** (ou núcleo Python puro) com foco em arquitetura limpa, **28 padrões de projeto** (4 fundamentos OOP, 1 arquitetural e os 23 GoF), **300 domínios nativos** (mais cadastro de domínios personalizados), **25 tipos de campo categorizados**, camada de **Infraestrutura, Segurança e Bibliotecas de Terceiros**, API REST (`/api/v1/` e DRF), **10 temas × 6 tons + 20 paletas**, interface visual **WYSIWYG em 5 colunas**, terminal interativo **CMD** e **tutoriais guiados passo a passo**.

Cada sistema gerado nasce pronto para rodar, com testes `pytest`, camada de domínio desacoplada da camada web (`nucleo/` + `web/`), `requirements.txt`, `iniciar.sh` / `iniciar.bat` e documentação própria.

---

## Início rápido

### Pré-requisitos
- **Python 3.12+** (recomendado 3.12, 3.13 ou 3.14)
- `git` e `pip`

### Linux / macOS / WSL
```bash
bash iniciar.sh
```
Cria `.venv`, instala `requirements.txt` e sobe o SGS em `http://127.0.0.1:6100/` (abrindo direto no **WYSIWYG**; o modo **CMD** fica em `/cmd` e no alternador fixo à esquerda).

Outros comandos do `iniciar.sh`:
```bash
bash iniciar.sh preparar            # prepara .venv e dependências sem subir o servidor
source iniciar.sh ativar            # ativa o .venv no terminal atual
bash iniciar.sh rodar 6150          # sobe o SGS em outra porta
bash iniciar.sh sistema <pasta>     # prepara e sobe um sistema de sistemas_gerados/
bash iniciar.sh testar              # executa a suíte pytest do SGS
```

### Windows (cmd / PowerShell)
```bat
iniciar.bat
```
Suporta os mesmos subcomandos: `iniciar.bat preparar`, `iniciar.bat ativar`, `iniciar.bat rodar 6150`, `iniciar.bat sistema <pasta>` e `iniciar.bat testar`.

### Execução manual (com `.venv` ativo)
```bash
python manage.py runserver 127.0.0.1:6100
```

---

## Fluxo arquitetural em 5 passos (WYSIWYG e CMD)

Tanto a bancada visual **WYSIWYG** (`/`) quanto o terminal **CMD** (`/cmd`) seguem a mesma arquitetura em 5 etapas, com paridade de recursos e opções mutuamente excludentes validadas automaticamente:

| Passo | Coluna no WYSIWYG | O que você configura | Equivalente no CMD |
|---|---|---|---|
| **1** | **Projeto & Domínio** | Escolha entre **300 domínios nativos** (ou texto livre), camada **Com Django** vs. **Só Python**, estilo web (`web`, `bootstrap`, `simples`, `cmd`), tema/paleta do sistema gerado, modo **Completo** vs. **Exercício (TODOs)** e opções de estudo/comentários. | `sgs dominios`, `sgs gerar`, `sgs estilo`, `sgs config` |
| **2** | **Infra, Segurança & Libs** | Layout (`app` raiz ou `apps/`), PK (`BigAutoField` vs. `UUIDv4`), motor de ID interno (`nenhum`, `LNNL`, `UUIDv7` + tamanho), banco (`SQLite3`, `PostgreSQL`, `MongoDB`) + `Redis`, hardening (`básica` vs. `baseline`), `Argon2id`, `Fernet`, `Anti-Bot`, `RBAC`, `Recuperação de Usuário/Senha`, `Two-Factor (2FA)` com expiração configurável (`5/10/15/30 min`) e bibliotecas (`django-ratelimit`, `django-anymail`, `django-tinymce`). | `sgs infra`, `sgs config <chave>=<valor>`, `sgs info <n>` |
| **3** | **Padrões da Classe** | **28 padrões** classificados por escopo de aplicação (**Arquitetura**, **Classe**, **Campo** e **Ligação / FK**) com descrição prática do problema que cada padrão resolve. | `sgs padroes [escopo]`, `sgs info <n>` |
| **4** | **Classes & Campos** | Montagem visual de classes e **25 tipos de campo** organizados em 4 categorias (**Primitivos**, **Seleção & Lista**, **Domínio & Negócio** — CPF, CNPJ, CEP, telefone, e-mail, moeda, URL — e **Estruturados & Mídia** — imagem, arquivo, geolocalização, JSON, calculado `@property`). | `sgs incrementar`, `sgs editar`, `sgs tipos`, `sgs app` |
| **5** | **Ligações & API** | Relacionamentos `ForeignKey` (arrastar uma classe sobre outra), atalhos para padrões de colaboração entre classes e configuração da API REST (`/api/v1/` e DRF). | `sgs ligar`, `sgs api config` |

---

## Tutoriais interativos integrados

Logo abaixo do seletor fixo **`WYSIWYG | CMD`** no canto superior esquerdo existe o botão **`Tutorial`**:
- **No WYSIWYG (`/`)**: tour interativo em 8 passos destacando cada uma das 5 colunas, a barra de projetos, os temas/tons e a barra de comando sincronizada.
- **No CMD (`/cmd`)**: tour interativo em 7 passos cobrindo a barra de comandos rápidos, histórico/saída, prompt interativo, caixas do rodapé e comandos de infraestrutura (`sgs infra`, `sgs padroes`, `sgs info`).
- Navegação por **Voltar**, **Próximo**, **Fechar (`×`)** ou teclado (**`←`**, **`→`**, **`Esc`**).

---

## Catálogo de 10 sistemas de exemplo prontos (`sistemas_gerados/`)

O repositório já inclui **10 sistemas completos** (numerados de `01` a `10`) cobrindo diferentes domínios, combinações de padrões, bancos, recursos de segurança, bibliotecas de terceiros, relacionamentos FK, temas e execução em Django ou Python puro:

| Nº | Pasta em `sistemas_gerados/` | Domínio / Entidades | Destaques de Arquitetura, Infra & Segurança |
|---|---|---|---|
| `01` | `hotel_resort__state_strategy_web_t01_tom3` | Hotel Resort · `Reserva` | `State`, `Strategy` · Tema T01 (Tom 3) · campos `data-hora`, `email` |
| `02` | `clinica_vida__service_observer_strategy_web_t07_escuro` | Clínica Vida · `Consulta` | `Service`, `Observer`, `Strategy` · Tema T07 Escuro · `UUIDv4`, hardening `baseline`, `Fernet`, `cpf`, `telefone` |
| `03` | `loja_virtual__decorator_facade_strategy_web_t02_tom4` | Loja Virtual · `Pedido` → `Comprador` (FK) | `Decorator`, `Facade`, `Strategy` · Tema T02 (Tom 4) · layout `apps/`, `PostgreSQL`, `Redis`, `django-ratelimit`, `moeda`, `cep` |
| `04` | `translog_cargas__factory_method_adapter_state_strategy_web_t03_tom5` | TransLog Cargas · `Frete` | `Factory Method`, `Adapter`, `State`, `Strategy` · Tema T03 (Tom 5) · motor ID `LNNL (24)`, `RBAC`, `geolocalizacao`, `multipla` |
| `05` | `imobiliaria_lar__builder_composite_strategy_web_t05_claro` | Imobiliária Lar · `Contrato` | `Builder`, `Composite`, `Strategy` · Tema T05 Claro · `django-tinymce`, `django-anymail`, recuperação de senha, `texto-longo`, `imagem` |
| `06` | `escola_saber__mediator_strategy_template_method_web_t06_tom2` | Escola Saber · `Turma` | `Mediator`, `Strategy`, `Template Method` · Tema T06 (Tom 2) · `Two-Factor (15 min)`, `Argon2id`, `Anti-Bot`, `url`, `arquivo` |
| `07` | `farmacia_saude__proxy_chain_strategy_web_t08_escuro` | Farmácia Saúde · `Receita` | `Proxy`, `Chain of Responsibility`, `Strategy` · Tema T08 Escuro · `UUIDv4`, motor ID `LNNL (32)`, `Fernet`, `RBAC`, `cnpj`, `json` |
| `08` | `restaurante_sabor__polimorfismo_service_decorator_strategy_web_t04_tom3` | Restaurante Sabor · `Comanda` → `Salao` (FK) | `Polimorfismo`, `Service`, `Decorator`, `Strategy` · Tema T04 (Tom 3) · layout `apps/`, `PostgreSQL`, `data-hora` |
| `09` | `vento_sul_energia_eolica__command_memento_observer_strategy_web_t10_escuro` | Vento Sul Energia Eólica · `ParqueAerogerador` | `Command`, `Memento`, `Observer`, `Strategy` · Tema T10 Escuro (Paleta P12) · `MongoDB`, `Redis`, `geolocalizacao`, `json` |
| `10` | `biblioteca_municipal__iterator_state_visitor` | Biblioteca Municipal · `Emprestimo` | `Iterator`, `State`, `Visitor` · **Só Python (núcleo puro sem Django)** · `data-hora` |

Para subir qualquer um dos sistemas Django diretamente:
```bash
bash iniciar.sh sistema hotel_resort__state_strategy_web_t01_tom3
```
Ou pelo próprio SGS (no WYSIWYG clicando no chip do projeto, ou no CMD com `sgs rodar 01`).

---

## Principais comandos no modo CMD (`/cmd`)

| Comando | Descrição |
|---|---|
| `sgs` | Mostra o resumo dos comandos disponíveis |
| `sgs gerar <dominio> [padroes...]` | Gera um novo sistema (aceita `-sp` só Python, `-e` exercício, `-nt` sem testar, `-p` modo guiado) |
| `sgs infra` | Exibe o painel atual do Passo 2 (Infra, Segurança & Libs) e atalhos de alteração |
| `sgs padroes [arquitetura\|classe\|campo\|relacao]` | Lista os 28 padrões filtrados por escopo |
| `sgs dominios [filtro \| novo]` | Lista os 300 domínios nativos ou cadastra um domínio personalizado |
| `sgs tipos <campo1, campo2...>` | Mostra a inferência automática de tipos e regras de campo |
| `sgs listar` / `sgs info <n>` | Lista os sistemas gerados ou exibe ficha técnica completa (padrões, campos e infra/segurança) |
| `sgs incrementar <n> Classe.campo [regra]` | Adiciona um novo campo a uma classe existente e regenera o sistema |
| `sgs ligar <n> Origem.campo -> Destino` | Cria ligação `ForeignKey` entre classes |
| `sgs app <n> <NomeClasse>` | Adiciona uma nova classe/entidade ao sistema |
| `sgs editar <n>` / `sgs duplicar <n>` | Edita atributos/opções ou duplica um sistema existente |
| `sgs api config <n> ...` | Configura campos expostos na API REST |
| `sgs rodar <n>` / `sgs parar <n>` / `sgs testar <n>` | Sobe, para ou testa um sistema gerado |
| `sgs estilo [T01..T10] [tom] [P01..P20]` | Define tema visual, tom (claro, escuro, tom2..tom5) e paleta (T10) |
| `sgs config [chave=valor ...]` | Lê ou altera configurações padrão do gerador (banco, segurança, libs, admin, porta) |
| `sgs wysiwyg [n]` | Abre a bancada visual (opcionalmente já focado no sistema `n`) |
| `sgs tutorial` / `sgs wiki` / `sgs hub` | Abre os materiais de estudo e referências locais |

---

## Estrutura do repositório

```text
.
├── iniciar.sh / iniciar.bat      # Preparação automática (.venv, deps) e inicialização do SGS
├── manage.py                     # Entrypoint Django do servidor do SGS (porta padrão 6100)
├── requirements.txt              # Dependências do SGS (Django 6, DRF, pytest, pytest-django)
├── gerar_sistema.py              # Motor gerador (núcleo Python, Django, Infra/Segurança, testes)
├── tela_prompt.py                # Servidor HTTP + comandos CMD + endpoints do WYSIWYG
├── sgs_wysiwyg.py                # Interface visual em 5 colunas, temas, paletas e tour interativo
├── sgs_perguntas.py              # Fluxo guiado interativo de criação (-p)
├── sgs_comand.py                 # Assistente de comandos interativo
├── sgs_tutorial.py               # Conteúdo do tutorial de padrões e fluxo do SGS
├── dominios.py                   # Catálogo base (domínios 001–101) + regras
├── dominios_102_300.py           # Catálogo expandido (domínios 102–300)
├── sgs_dominios.py               # Persistência de domínios personalizados
├── tipos_campos.py               # Inferência e validação dos 25 tipos de campo
├── temas_web.py / temas/         # 10 temas × 6 tons + 20 paletas do T10
├── sgs_web/                      # Aplicação Django que hospeda o SGS
├── referencias/                  # Cópias estáticas de estudo (Wikipédia GoF e Django Study Hub)
├── sistemas_gerados/             # 10 sistemas de exemplo (01 a 10) + .sgs_registro.json
└── tests/                        # Suíte pytest do gerador e da interface (WYSIWYG + CMD)
```

---

## Rodando os testes

```bash
bash iniciar.sh testar
```
Ou diretamente com o `.venv` ativo:
```bash
pytest -q
```
Para filtrar um módulo específico:
```bash
pytest -q tests/test_gerador.py -k "infra_seguranca"
pytest -q tests/test_tela.py -k "wysiwyg"
```

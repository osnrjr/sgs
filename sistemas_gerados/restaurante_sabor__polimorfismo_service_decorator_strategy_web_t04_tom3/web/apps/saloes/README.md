# Módulo `saloes` — Salao (acrescentado por `sgs app`)

Pedido: _"saloes do restaurante com nome e capacidade"_ · domínio: `restaurante`

| Item | Conteúdo |
|---|---|
| Pacote | `apps.saloes` (registrado em `INSTALLED_APPS` de `web/config/settings.py`) |
| Entidade | `Salao` — campos: `cliente`, `mesa`, `pratos`, `preco_prato`, `observacao`, `tipo` |
| Padrões | Encapsulamento com @property, State, Strategy — o núcleo deste módulo fica em `nucleo/` (dentro da app) |
| Form | `SalaoForm` (`forms.py`): o MESMO ModelForm valida as telas e a API |
| CRUD (telas) | `/saloes/` · `/saloes/novo/` · `/saloes/<id>/` · `/saloes/<id>/editar/` · `/saloes/<id>/excluir/` |
| API REST | `/saloes/api/v1/` (GET, POST) · `/saloes/api/v1/<id>/` (GET, PUT, PATCH, DELETE) |
| Settings | `settings.py` desta app: `API_LIMITE`, `API_ESCRITA` (no projeto: `SALOES_API_LIMITE`…) |
| Arquivos | `settings.py` · `models.py` · `forms.py` · `services.py` · `viewmodels.py` · `views.py` · `api.py` · `urls.py` · `templates/` · `static/` · `nucleo/` · `tests/` |
| Testes | `cd web && python -m pytest apps/saloes` (telas, API e o núcleo em `tests/nucleo/`) |
| Banco | `bash iniciar.sh migrar` (o `makemigrations` já inclui `saloes`) |

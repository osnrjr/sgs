# Módulo `compradores` — Comprador (acrescentado por `sgs app`)

Pedido: _"compradores com nome e email"_ · domínio: `generico`

| Item | Conteúdo |
|---|---|
| Pacote | `apps.compradores` (registrado em `INSTALLED_APPS` de `web/config/settings.py`) |
| Entidade | `Comprador` — campos: `cliente`, `codigo`, `quantidade`, `valor_unitario`, `observacao`, `tipo` |
| Padrões | Encapsulamento com @property, Strategy — o núcleo deste módulo fica em `nucleo/` (dentro da app) |
| Form | `CompradorForm` (`forms.py`): o MESMO ModelForm valida as telas e a API |
| CRUD (telas) | `/compradores/` · `/compradores/novo/` · `/compradores/<id>/` · `/compradores/<id>/editar/` · `/compradores/<id>/excluir/` |
| API REST | `/compradores/api/v1/` (GET, POST) · `/compradores/api/v1/<id>/` (GET, PUT, PATCH, DELETE) |
| Settings | `settings.py` desta app: `API_LIMITE`, `API_ESCRITA` (no projeto: `COMPRADORES_API_LIMITE`…) |
| Arquivos | `settings.py` · `models.py` · `forms.py` · `services.py` · `viewmodels.py` · `views.py` · `api.py` · `urls.py` · `templates/` · `static/` · `nucleo/` · `tests/` |
| Testes | `cd web && python -m pytest apps/compradores` (telas, API e o núcleo em `tests/nucleo/`) |
| Banco | `bash iniciar.sh migrar` (o `makemigrations` já inclui `compradores`) |

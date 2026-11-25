# App `comandas` — Restaurante Sabor

Documentação individual da app (Instruções de desenvolvimento DJANGO §9.3).

| Item | Conteúdo |
|---|---|
| Finalidade | Cadastro e listagem de `Comanda` com o valor calculado pela política de tipo de cliente (Strategy do núcleo). Não faz autenticação nem pagamento. |
| Dependências | `nucleo/` (Python puro, `nucleo.politicas`); Django; chaves do `web/.env`. |
| Modelos | `Comanda` — sem escopo de tenant (modo `single`). |
| Serviços públicos | `ComandaService.valor_final(obj)` e `ComandaService.resumo(objetos)` (`services.py`). |
| URLs | `comandas:lista` (`/`), `comandas:criar` (`/novo/`), `comandas:api` (`/api/`). |
| API REST | `comandas:api_colecao` (`/api/v1/`: GET, POST) e `comandas:api_item` (`/api/v1/<id>/`: GET, PUT, PATCH, DELETE). |
| Settings | `settings.py` da app: `API_LIMITE`, `API_ESCRITA` (no projeto: `COMANDAS_API_LIMITE`…). |
| Instalação em outro projeto | `INSTALLED_APPS += ["apps.comandas"]`, `path("", include("apps.comandas.urls"))`, `python manage.py migrate`. |
| Testes | `cd web && python -m pytest apps/comandas` |

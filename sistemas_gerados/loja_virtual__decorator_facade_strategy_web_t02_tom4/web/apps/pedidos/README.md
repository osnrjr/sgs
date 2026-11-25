# App `pedidos` — Loja Virtual

Documentação individual da app (Instruções de desenvolvimento DJANGO §9.3).

| Item | Conteúdo |
|---|---|
| Finalidade | Cadastro e listagem de `Pedido` com o valor calculado pela política de tipo de cliente (Strategy do núcleo). Não faz autenticação nem pagamento. |
| Dependências | `nucleo/` (Python puro, `nucleo.politicas`); Django; chaves do `web/.env`. |
| Modelos | `Pedido` — sem escopo de tenant (modo `single`). |
| Serviços públicos | `PedidoService.valor_final(obj)` e `PedidoService.resumo(objetos)` (`services.py`). |
| URLs | `pedidos:lista` (`/`), `pedidos:criar` (`/novo/`), `pedidos:api` (`/api/`). |
| API REST | `pedidos:api_colecao` (`/api/v1/`: GET, POST) e `pedidos:api_item` (`/api/v1/<id>/`: GET, PUT, PATCH, DELETE). |
| Settings | `settings.py` da app: `API_LIMITE`, `API_ESCRITA` (no projeto: `PEDIDOS_API_LIMITE`…). |
| Instalação em outro projeto | `INSTALLED_APPS += ["apps.pedidos"]`, `path("", include("apps.pedidos.urls"))`, `python manage.py migrate`. |
| Testes | `cd web && python -m pytest apps/pedidos` |

"""Controle de acesso baseado em papéis (RBAC — §17.4)."""
from functools import wraps

from django.http import HttpResponseForbidden

PAPEIS = ("admin", "gestor", "operador", "leitor")
PERMISSOES = {
    "admin": {"ver", "criar", "editar", "apagar", "configurar"},
    "gestor": {"ver", "criar", "editar", "apagar"},
    "operador": {"ver", "criar", "editar"},
    "leitor": {"ver"},
}


def tem_permissao(papel, acao):
    return acao in PERMISSOES.get(str(papel).lower(), set())


def exigir_papel(*permitidos):
    alvos = {p.lower() for p in permitidos}

    def decorador(view):
        @wraps(view)
        def embrulho(request, *args, **kwargs):
            papel = getattr(request, "papel_usuario", None) or request.headers.get("X-Papel", "")
            if str(papel).lower() not in alvos:
                return HttpResponseForbidden("Acesso negado pelo RBAC.")
            return view(request, *args, **kwargs)

        return embrulho

    return decorador

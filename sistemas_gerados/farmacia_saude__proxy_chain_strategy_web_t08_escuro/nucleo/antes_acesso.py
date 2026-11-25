"""ANTES — o smell do Proxy: cache e permissão feitos na mão por quem consulta."""

CACHE = {}


def consultar_antigo(consulta, item, perfil):
    if perfil not in ("gerente", "atendente"):
        raise PermissionError(f"perfil sem acesso: {perfil}")
    chave = (item.cliente, item.unidades, item.preco_unitario)
    if chave not in CACHE:
        CACHE[chave] = consulta.calcular(item)
    return CACHE[chave]

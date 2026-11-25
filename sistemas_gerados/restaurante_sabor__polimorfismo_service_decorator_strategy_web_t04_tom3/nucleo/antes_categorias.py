"""ANTES — o smell do polimorfismo ausente: um if que cresce a cada categoria nova."""


def imprimir_preco(tipo):
    """Para a categoria "Salada" seria preciso EDITAR esta função (e ela cai no else, errada)."""
    if tipo == "prato_chef":
        return "Prato do chef: R$ 95.00 por prato"
    elif tipo == "massa":
        return "Massa: R$ 58.00 por prato"
    else:
        return "Prato executivo: R$ 42.00 por prato"

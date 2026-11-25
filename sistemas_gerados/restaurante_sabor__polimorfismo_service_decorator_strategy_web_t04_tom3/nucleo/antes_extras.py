"""ANTES — o smell do Decorator: uma pilha de flags e ifs (cada extra novo = parâmetro + if)."""


def preco_com_flags(item, couvert=False, sobremesa=False, taca_vinho=False):
    total = item.total
    if couvert:
        total += 12.0
    if sobremesa:
        total += 22.0
    if taca_vinho:
        total += 80.0
    return round(total, 2)

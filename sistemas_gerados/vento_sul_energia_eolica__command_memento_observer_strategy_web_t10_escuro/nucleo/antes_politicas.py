"""ANTES — o smell do Strategy: um if/elif por tipo de contrato que cresce a cada regra nova."""


class CobrancaAntiga:
    def __init__(self, item, tipo):
        self.item = item
        self.tipo = tipo  # um TEXTO decide o comportamento

    def valor(self):
        base = self.item.total
        if self.tipo == "padrao":
            return round(base * 1.0, 2)
        elif self.tipo == "corporativo":
            return round(base * 0.9, 2)
        elif self.tipo == "recorrente":
            return round(base * 0.85, 2)
        else:
            raise ValueError(f"tipo de contrato desconhecido: {self.tipo}")

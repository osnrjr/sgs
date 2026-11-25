"""ANTES — o smell do Strategy: um if/elif por tipo de bolsa que cresce a cada regra nova."""


class CobrancaAntiga:
    def __init__(self, item, tipo):
        self.item = item
        self.tipo = tipo  # um TEXTO decide o comportamento

    def valor(self):
        base = self.item.total
        if self.tipo == "regular":
            return round(base * 1.0, 2)
        elif self.tipo == "irmaos":
            return round(base * 0.9, 2)
        elif self.tipo == "bolsista":
            return round(base * 0.5, 2)
        else:
            raise ValueError(f"tipo de bolsa desconhecido: {self.tipo}")

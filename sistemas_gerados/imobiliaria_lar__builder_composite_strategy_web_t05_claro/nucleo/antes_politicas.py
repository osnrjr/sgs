"""ANTES — o smell do Strategy: um if/elif por tipo de cliente que cresce a cada regra nova."""


class CobrancaAntiga:
    def __init__(self, item, tipo):
        self.item = item
        self.tipo = tipo  # um TEXTO decide o comportamento

    def valor(self):
        base = self.item.total
        if self.tipo == "residencial":
            return round(base * 1.0, 2)
        elif self.tipo == "comercial":
            return round(base * 1.2, 2)
        elif self.tipo == "estudante":
            return round(base * 0.9, 2)
        else:
            raise ValueError(f"tipo de cliente desconhecido: {self.tipo}")

"""ANTES — o smell do Strategy: um if/elif por tipo de convênio que cresce a cada regra nova."""


class CobrancaAntiga:
    def __init__(self, item, tipo):
        self.item = item
        self.tipo = tipo  # um TEXTO decide o comportamento

    def valor(self):
        base = self.item.total
        if self.tipo == "particular":
            return round(base * 1.0, 2)
        elif self.tipo == "convenio_ouro":
            return round(base * 0.6, 2)
        elif self.tipo == "convenio_prata":
            return round(base * 0.75, 2)
        else:
            raise ValueError(f"tipo de convênio desconhecido: {self.tipo}")

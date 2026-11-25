"""
Restaurante Sabor — DECORATOR (Aula 10): somar opcionais empilhando embrulhos.

COMPONENTE       ComandaBase(item)  → preco() / descricao()
DECORADOR BASE   Adicional          → guarda o embrulhado e DELEGA
DECORADORES      Com…               → chamam o de DENTRO e somam a SUA parte
Como a interface por fora é IGUAL à de dentro, um embrulho pode embrulhar outro: EMPILHA.
Quando NÃO usar: extras que só somam valor fixo → lista + sum() basta.
O @decorator do Python decora FUNÇÕES; este padrão decora OBJETOS.
"""


class ComandaBase:
    """COMPONENTE: expõe a Comanda pela interface preco()/descricao()."""

    def __init__(self, item):
        self._item = item

    def preco(self):
        return self._item.total

    def descricao(self):
        return f"Comanda de {self._item.cliente} ({self._item.pratos} prato(s))"


class Adicional:
    """DECORADOR BASE: mesma interface; guarda o objeto de dentro e, por padrão, só repassa."""

    def __init__(self, componente):
        self._componente = componente  # pode ser ComandaBase OU outro Adicional → por isso empilha

    def preco(self):
        return self._componente.preco()

    def descricao(self):
        return self._componente.descricao()


class ComCouvert(Adicional):
    """Soma R$ 12.00 (couvert) ao que está DENTRO."""

    VALOR = 12.0

    def preco(self):
        return round(self._componente.preco() + self.VALOR, 2)  # de dentro + a minha parte

    def descricao(self):
        return self._componente.descricao() + " + couvert"


class ComSobremesa(Adicional):
    """Soma R$ 22.00 (sobremesa) ao que está DENTRO."""

    VALOR = 22.0

    def preco(self):
        return round(self._componente.preco() + self.VALOR, 2)  # de dentro + a minha parte

    def descricao(self):
        return self._componente.descricao() + " + sobremesa"


class ComTacaVinho(Adicional):
    """Soma R$ 80.00 (taça de vinho) ao que está DENTRO."""

    VALOR = 80.0

    def preco(self):
        return round(self._componente.preco() + self.VALOR, 2)  # de dentro + a minha parte

    def descricao(self):
        return self._componente.descricao() + " + taça de vinho"


class ComTaxaServico(Adicional):
    """MUDA comportamento: multiplica TUDO o que está dentro por 1.1 — aqui a ORDEM importa."""

    FATOR = 1.1

    def preco(self):
        return round(self._componente.preco() * self.FATOR, 2)

    def descricao(self):
        return self._componente.descricao() + " (+10% serviço)"

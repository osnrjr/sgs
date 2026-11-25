"""
Restaurante Sabor — POLIMORFISMO (Aula 04): muitas categorias, uma função.

ANTES (nucleo/antes_categorias.py): imprimir_preco(tipo) com if/elif por categoria.
DEPOIS: cada categoria SOBRESCREVE descricao() e preco_unidade(); imprimir_preco(categoria)
só chama os métodos — o Python escolhe a versão pelo tipo REAL do objeto.
Herdar = ganhar o que é igual · sobrescrever = mudar o que é diferente.
"""


class PratoExecutivo:
    """Classe BASE: o comportamento PADRÃO de toda categoria."""

    def __init__(self, codigo):
        self.codigo = codigo

    def descricao(self):
        return 'Prato executivo'

    def preco_unidade(self):
        return 42.0


class PratoChef(PratoExecutivo):
    """PratoChef É-UM PratoExecutivo: HERDA o __init__ e SOBRESCREVE descricao() e preco_unidade()."""

    def descricao(self):
        return 'Prato do chef'

    def preco_unidade(self):
        return 95.0


class Massa(PratoExecutivo):
    """Massa É-UM PratoExecutivo: HERDA o __init__ e SOBRESCREVE descricao() e preco_unidade()."""

    def descricao(self):
        return 'Massa'

    def preco_unidade(self):
        return 58.0


class Salada(PratoExecutivo):
    """NOVA categoria: entrou SEM mudar imprimir_preco (aberto ao novo)."""

    def descricao(self):
        return 'Salada'

    def preco_unidade(self):
        return 38.0


class PratoExecutivoPadrao(PratoExecutivo):
    """Não sobrescreve nada: o Python procura o método aqui, não acha e SOBE para PratoExecutivo."""


def imprimir_preco(categoria):
    """Função POLIMÓRFICA: não pergunta o tipo (zero if); cada categoria responde a seu modo."""
    return f"{categoria.descricao()}: R$ {categoria.preco_unidade():.2f} por prato"

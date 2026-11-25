"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Comanda ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Comanda

DADOS_EXEMPLO = [
    {'cliente': 'Márcio', 'mesa': 101, 'pratos': 2, 'preco_prato': 58.0, 'horario_pedido': '2026-01-10T09:30'},
    {'cliente': 'Natália', 'mesa': 201, 'pratos': 3, 'preco_prato': 42.0, 'horario_pedido': '2026-02-15T14:00'},
    {'cliente': 'Otávio', 'mesa': 301, 'pratos': 1, 'preco_prato': 95.0, 'horario_pedido': '2026-03-20T18:45'},
    {'cliente': 'Priscila', 'mesa': 401, 'pratos': 4, 'preco_prato': 0.0, 'horario_pedido': '2026-04-25T08:15'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Comanda (válida, a menos que as mudanças a tornem inválida)."""
    return Comanda(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Comandas diferentes e válidas — objetos novos a cada chamada."""
    return [Comanda(**d) for d in DADOS_EXEMPLO]

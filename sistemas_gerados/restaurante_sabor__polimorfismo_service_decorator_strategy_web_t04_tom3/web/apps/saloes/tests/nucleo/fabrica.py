"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Salao ganhar um atributo, só este arquivo muda.
"""
from apps.saloes.nucleo.entidades import Salao

DADOS_EXEMPLO = [
    {'cliente': 'Márcio', 'mesa': 101, 'pratos': 2, 'preco_prato': 58.0},
    {'cliente': 'Natália', 'mesa': 201, 'pratos': 3, 'preco_prato': 42.0},
    {'cliente': 'Otávio', 'mesa': 301, 'pratos': 1, 'preco_prato': 95.0},
    {'cliente': 'Priscila', 'mesa': 401, 'pratos': 4, 'preco_prato': 0.0}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Salao (válida, a menos que as mudanças a tornem inválida)."""
    return Salao(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Salaos diferentes e válidas — objetos novos a cada chamada."""
    return [Salao(**d) for d in DADOS_EXEMPLO]

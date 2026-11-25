"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Pedido ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Pedido

DADOS_EXEMPLO = [
    {'cliente': 'Juliana', 'produto': 101, 'quantidade': 2, 'preco_unitario': 50.0, 'frete': 10.5, 'cep_entrega': '01310-100'},
    {'cliente': 'Kleber', 'produto': 201, 'quantidade': 3, 'preco_unitario': 19.9, 'frete': 21.0, 'cep_entrega': '20040-020'},
    {'cliente': 'Larissa', 'produto': 301, 'quantidade': 1, 'preco_unitario': 300.0, 'frete': 31.5, 'cep_entrega': '30130-110'},
    {'cliente': 'Marcos', 'produto': 401, 'quantidade': 4, 'preco_unitario': 0.0, 'frete': 42.0, 'cep_entrega': '80020-310'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Pedido (válida, a menos que as mudanças a tornem inválida)."""
    return Pedido(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Pedidos diferentes e válidas — objetos novos a cada chamada."""
    return [Pedido(**d) for d in DADOS_EXEMPLO]

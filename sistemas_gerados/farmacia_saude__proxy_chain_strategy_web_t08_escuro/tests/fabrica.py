"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Receita ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Receita

DADOS_EXEMPLO = [
    {'cliente': 'Ana', 'balcao': 101, 'unidades': 2, 'preco_unitario': 25.9, 'cnpj_fornecedor': '11.222.333/0001-81', 'metadados': {'chave': 'metadados_1', 'ativo': True}},
    {'cliente': 'Bruno', 'balcao': 201, 'unidades': 3, 'preco_unitario': 12.5, 'cnpj_fornecedor': '11.444.777/0001-61', 'metadados': {'chave': 'metadados_2', 'ativo': True}},
    {'cliente': 'Carla', 'balcao': 301, 'unidades': 1, 'preco_unitario': 89.9, 'cnpj_fornecedor': '45.997.418/0001-53', 'metadados': {'chave': 'metadados_3', 'ativo': True}},
    {'cliente': 'Diego', 'balcao': 401, 'unidades': 4, 'preco_unitario': 0.0, 'cnpj_fornecedor': '27.865.757/0001-02', 'metadados': {'chave': 'metadados_4', 'ativo': True}}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Receita (válida, a menos que as mudanças a tornem inválida)."""
    return Receita(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Receitas diferentes e válidas — objetos novos a cada chamada."""
    return [Receita(**d) for d in DADOS_EXEMPLO]

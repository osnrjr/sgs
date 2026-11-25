"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Emprestimo ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Emprestimo

DADOS_EXEMPLO = [
    {'leitor': 'Beatriz', 'exemplar': 101, 'dias': 2, 'taxa_dia': 2.5, 'data_devolucao': '2026-01-10T09:30'},
    {'leitor': 'Caio', 'exemplar': 201, 'dias': 3, 'taxa_dia': 1.0, 'data_devolucao': '2026-02-15T14:00'},
    {'leitor': 'Denise', 'exemplar': 301, 'dias': 1, 'taxa_dia': 10.0, 'data_devolucao': '2026-03-20T18:45'},
    {'leitor': 'Eduardo', 'exemplar': 401, 'dias': 4, 'taxa_dia': 0.0, 'data_devolucao': '2026-04-25T08:15'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Emprestimo (válida, a menos que as mudanças a tornem inválida)."""
    return Emprestimo(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Emprestimos diferentes e válidas — objetos novos a cada chamada."""
    return [Emprestimo(**d) for d in DADOS_EXEMPLO]

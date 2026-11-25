"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Turma ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Turma

DADOS_EXEMPLO = [
    {'aluno': 'Márcio', 'sala': 101, 'meses': 2, 'mensalidade': 850.0, 'portal_url': 'https://exemplo.com.br/item-1', 'comprovante': 'documentos/anexo_1.pdf'},
    {'aluno': 'Natália', 'sala': 201, 'meses': 3, 'mensalidade': 600.0, 'portal_url': 'https://exemplo.com.br/item-2', 'comprovante': 'documentos/planilha_2.xlsx'},
    {'aluno': 'Otávio', 'sala': 301, 'meses': 1, 'mensalidade': 1200.0, 'portal_url': 'https://exemplo.com.br/item-3', 'comprovante': 'documentos/contrato_3.docx'},
    {'aluno': 'Priscila', 'sala': 401, 'meses': 4, 'mensalidade': 0.0, 'portal_url': 'https://exemplo.com.br/item-4', 'comprovante': 'documentos/relatorio_4.pdf'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Turma (válida, a menos que as mudanças a tornem inválida)."""
    return Turma(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Turmas diferentes e válidas — objetos novos a cada chamada."""
    return [Turma(**d) for d in DADOS_EXEMPLO]

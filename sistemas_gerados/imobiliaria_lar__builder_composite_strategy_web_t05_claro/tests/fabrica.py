"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Contrato ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Contrato

DADOS_EXEMPLO = [
    {'locatario': 'Danilo', 'imovel': 101, 'meses': 2, 'valor_aluguel': 1800.0, 'descricao_completa': 'Descrição detalhada de descricao completa 1.', 'foto_capa': 'imagens/foto_1.png'},
    {'locatario': 'Érica', 'imovel': 201, 'meses': 3, 'valor_aluguel': 1200.0, 'descricao_completa': 'Descrição detalhada de descricao completa 2.', 'foto_capa': 'imagens/banner_2.jpg'},
    {'locatario': 'Felipe', 'imovel': 301, 'meses': 1, 'valor_aluguel': 3500.0, 'descricao_completa': 'Descrição detalhada de descricao completa 3.', 'foto_capa': 'imagens/avatar_3.webp'},
    {'locatario': 'Giovana', 'imovel': 401, 'meses': 4, 'valor_aluguel': 0.0, 'descricao_completa': 'Descrição detalhada de descricao completa 4.', 'foto_capa': 'imagens/icone_4.svg'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Contrato (válida, a menos que as mudanças a tornem inválida)."""
    return Contrato(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Contratos diferentes e válidas — objetos novos a cada chamada."""
    return [Contrato(**d) for d in DADOS_EXEMPLO]

"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Frete ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Frete

DADOS_EXEMPLO = [
    {'cliente': 'Elisa', 'caminhao': 101, 'toneladas': 2, 'valor_tonelada': 280.0, 'coordenadas': '-23.5505,-46.6333', 'etiquetas': 'fragil'},
    {'cliente': 'Fábio', 'caminhao': 201, 'toneladas': 3, 'valor_tonelada': 220.0, 'coordenadas': '-22.9068,-43.1729', 'etiquetas': 'fragil,urgente'},
    {'cliente': 'Gabriela', 'caminhao': 301, 'toneladas': 1, 'valor_tonelada': 450.0, 'coordenadas': '-19.9167,-43.9345', 'etiquetas': 'fragil'},
    {'cliente': 'Henrique', 'caminhao': 401, 'toneladas': 4, 'valor_tonelada': 0.0, 'coordenadas': '-25.4284,-49.2733', 'etiquetas': 'fragil,urgente'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Frete (válida, a menos que as mudanças a tornem inválida)."""
    return Frete(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Fretes diferentes e válidas — objetos novos a cada chamada."""
    return [Frete(**d) for d in DADOS_EXEMPLO]

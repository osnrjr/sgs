"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Reserva ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Reserva

DADOS_EXEMPLO = [
    {'hospede': 'Ana', 'quarto': 101, 'diarias': 2, 'valor_diaria': 200.0, 'agendado_em': '2026-01-10T09:30', 'email_hospede': 'contato@exemplo.com.br'},
    {'hospede': 'Bruno', 'quarto': 201, 'diarias': 3, 'valor_diaria': 150.0, 'agendado_em': '2026-02-15T14:00', 'email_hospede': 'financeiro@exemplo.com.br'},
    {'hospede': 'Carla', 'quarto': 301, 'diarias': 1, 'valor_diaria': 99.9, 'agendado_em': '2026-03-20T18:45', 'email_hospede': 'suporte@exemplo.com.br'},
    {'hospede': 'Diego', 'quarto': 401, 'diarias': 4, 'valor_diaria': 0.0, 'agendado_em': '2026-04-25T08:15', 'email_hospede': 'vendas@exemplo.com.br'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Reserva (válida, a menos que as mudanças a tornem inválida)."""
    return Reserva(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Reservas diferentes e válidas — objetos novos a cada chamada."""
    return [Reserva(**d) for d in DADOS_EXEMPLO]

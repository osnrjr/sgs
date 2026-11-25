"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a Consulta ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import Consulta

DADOS_EXEMPLO = [
    {'paciente': 'Sérgio', 'sala': 101, 'sessoes': 2, 'valor_sessao': 150.0, 'cpf_paciente': '123.456.789-09', 'telefone_contato': '(11) 99999-1111'},
    {'paciente': 'Tatiana', 'sala': 201, 'sessoes': 3, 'valor_sessao': 300.0, 'cpf_paciente': '987.654.321-00', 'telefone_contato': '(21) 98888-2222'},
    {'paciente': 'Ulisses', 'sala': 301, 'sessoes': 1, 'valor_sessao': 99.9, 'cpf_paciente': '111.444.777-35', 'telefone_contato': '(31) 3333-4444'},
    {'paciente': 'Vanessa', 'sala': 401, 'sessoes': 4, 'valor_sessao': 0.0, 'cpf_paciente': '529.982.247-25', 'telefone_contato': '(41) 97777-3333'}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma Consulta (válida, a menos que as mudanças a tornem inválida)."""
    return Consulta(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro Consultas diferentes e válidas — objetos novos a cada chamada."""
    return [Consulta(**d) for d in DADOS_EXEMPLO]

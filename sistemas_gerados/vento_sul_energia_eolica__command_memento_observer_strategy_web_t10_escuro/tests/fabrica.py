"""Fábrica de objetos VÁLIDOS para todos os testes (gerada).

Centraliza os dados de exemplo: se a ParqueAerogerador ganhar um atributo, só este arquivo muda.
"""
from nucleo.entidades import ParqueAerogerador

DADOS_EXEMPLO = [
    {'operador': 'Ana', 'torre': 101, 'megawatts': 2, 'preco_mwh': 220.0, 'geoloc': '-23.5505,-46.6333', 'parametros_json': {'chave': 'parametros_json_1', 'ativo': True}},
    {'operador': 'Bruno', 'torre': 201, 'megawatts': 3, 'preco_mwh': 140.0, 'geoloc': '-22.9068,-43.1729', 'parametros_json': {'chave': 'parametros_json_2', 'ativo': True}},
    {'operador': 'Carla', 'torre': 301, 'megawatts': 1, 'preco_mwh': 450.0, 'geoloc': '-19.9167,-43.9345', 'parametros_json': {'chave': 'parametros_json_3', 'ativo': True}},
    {'operador': 'Diego', 'torre': 401, 'megawatts': 4, 'preco_mwh': 0.0, 'geoloc': '-25.4284,-49.2733', 'parametros_json': {'chave': 'parametros_json_4', 'ativo': True}}
]


def dados(indice=0, **mudancas):
    """Cópia dos dados válidos nº `indice`, com as mudanças pedidas."""
    copia = dict(DADOS_EXEMPLO[indice])
    copia.update(mudancas)
    return copia


def criar(indice=0, **mudancas):
    """Cria uma ParqueAerogerador (válida, a menos que as mudanças a tornem inválida)."""
    return ParqueAerogerador(**dados(indice, **mudancas))


def itens_exemplo():
    """Quatro ParqueAerogeradors diferentes e válidas — objetos novos a cada chamada."""
    return [ParqueAerogerador(**d) for d in DADOS_EXEMPLO]

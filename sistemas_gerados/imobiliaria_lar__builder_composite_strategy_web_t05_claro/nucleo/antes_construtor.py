"""ANTES — o smell do Builder: construtor com muitos argumentos POSICIONAIS (a ordem é decorada)."""
from nucleo.entidades import Contrato


def nova_contrato_antiga(locatario, imovel, meses, valor_aluguel, descricao_completa, foto_capa, observacao=""):
    # Quem chama precisa lembrar a ORDEM: trocar dois números de lugar não dá erro, dá objeto errado.
    return Contrato(locatario, imovel, meses, valor_aluguel, descricao_completa, foto_capa, observacao)

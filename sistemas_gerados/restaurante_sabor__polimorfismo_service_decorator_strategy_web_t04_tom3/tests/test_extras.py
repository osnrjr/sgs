"""Testes do DECORATOR: mesma conta das flags, empilhamento e ordem com camada que multiplica."""
import itertools

import pytest

from nucleo.antes_extras import preco_com_flags
from nucleo.extras import Adicional, ComandaBase, ComCouvert, ComSobremesa, ComTacaVinho, ComTaxaServico
from tests.fabrica import criar

FLAGS = {ComCouvert: "couvert", ComSobremesa: "sobremesa", ComTacaVinho: "taca_vinho"}
COMBINACOES = [c for n in range(len(FLAGS) + 1) for c in itertools.combinations(FLAGS, n)]


@pytest.mark.parametrize("combinacao", COMBINACOES)
def test_qualquer_combinacao_bate_com_as_flags(combinacao):
    item = criar()
    componente = ComandaBase(item)
    for extra in combinacao:
        componente = extra(componente)
    esperado = preco_com_flags(item, **{FLAGS[e]: True for e in combinacao})
    assert componente.preco() == pytest.approx(esperado)


def test_componente_entrega_o_total():
    item = criar()
    assert ComandaBase(item).preco() == item.total


def test_decorador_base_so_delega():
    item = criar()
    assert Adicional(ComandaBase(item)).preco() == item.total


def test_descricao_segue_a_ordem_do_embrulho():
    item = criar()
    componente = ComSobremesa(ComCouvert(ComandaBase(item)))
    base = f"Comanda de {item.cliente} ({item.pratos} prato(s))"
    assert componente.descricao() == base + " + couvert" + " + sobremesa"


def test_mesmo_extra_duas_vezes():
    item = criar()
    assert ComCouvert(ComCouvert(ComandaBase(item))).preco() == pytest.approx(item.total + 2 * 12.0)


def test_com_camada_que_multiplica_a_ordem_importa():
    item = criar()
    base = item.total
    por_fora = ComTaxaServico(ComCouvert(ComandaBase(item)))
    por_dentro = ComCouvert(ComTaxaServico(ComandaBase(item)))
    assert por_fora.preco() == pytest.approx(round((base + 12.0) * 1.1, 2))
    assert por_dentro.preco() == pytest.approx(round(round(base * 1.1, 2) + 12.0, 2))
    assert por_fora.preco() != por_dentro.preco()


@pytest.mark.parametrize("classe", [Adicional, ComCouvert, ComSobremesa, ComTacaVinho, ComTaxaServico])
def test_todo_decorador_mantem_a_interface(classe):
    embrulho = classe(ComandaBase(criar()))
    assert callable(embrulho.preco) and callable(embrulho.descricao)

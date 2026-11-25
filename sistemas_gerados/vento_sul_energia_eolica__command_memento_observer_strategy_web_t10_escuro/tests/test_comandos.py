"""Testes do COMMAND: executar, desfazer e refazer em ordem; comando inválido não entra."""
import pytest

from nucleo.antes_comandos import alterar_antigo
from nucleo.comandos import AlterarCampo, Historico
from tests.fabrica import criar


def test_executar_muda_o_campo():
    item = criar()
    Historico().executar(AlterarCampo(item, "megawatts", item.megawatts + 1))
    assert item.megawatts == criar().megawatts + 1


def test_mesmo_efeito_da_versao_antiga():
    a, b = criar(), criar()
    alterar_antigo(a, "megawatts", a.megawatts + 2)
    Historico().executar(AlterarCampo(b, "megawatts", b.megawatts + 2))
    assert vars(a) == vars(b)


def test_desfazer_volta_ao_valor_anterior():
    item = criar()
    historico = Historico()
    historico.executar(AlterarCampo(item, "megawatts", item.megawatts + 1))
    assert historico.desfazer() is True and vars(item) == vars(criar())


def test_desfaz_na_ordem_inversa_e_refaz():
    item = criar()
    q0 = item.megawatts
    historico = Historico()
    historico.executar(AlterarCampo(item, "megawatts", q0 + 1))
    historico.executar(AlterarCampo(item, "megawatts", q0 + 2))
    historico.desfazer()
    assert item.megawatts == q0 + 1
    historico.desfazer()
    assert item.megawatts == q0
    historico.refazer()
    assert item.megawatts == q0 + 1


def test_comando_invalido_nao_entra_no_historico():
    item = criar()
    historico = Historico()
    with pytest.raises(ValueError):
        historico.executar(AlterarCampo(item, "megawatts", 0))
    assert historico.acoes() == [] and historico.desfazer() is False


def test_acao_nova_apaga_o_refazer():
    item = criar()
    historico = Historico()
    historico.executar(AlterarCampo(item, "megawatts", item.megawatts + 1))
    historico.desfazer()
    historico.executar(AlterarCampo(item, "preco_mwh", item.preco_mwh + 1))
    assert historico.refazer() is False

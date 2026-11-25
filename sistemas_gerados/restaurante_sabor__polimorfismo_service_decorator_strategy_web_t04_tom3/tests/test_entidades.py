"""Testes da Comanda (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.pratos * obj.preco_prato, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.pratos = obj.pratos + 1
    assert obj.total == round(obj.pratos * obj.preco_prato, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(cliente="  Márcio  ").cliente == "Márcio"


def test_observacao_sem_regra_aceita_qualquer_texto():
    assert criar().observacao == ""
    assert criar(observacao="qualquer coisa").observacao == "qualquer coisa"


@pytest.mark.parametrize("invalido", ['', '   ', 123, None])
def test_cliente_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(cliente=invalido)


def test_cliente_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.cliente = ''
    assert obj.cliente == DADOS_EXEMPLO[0]["cliente"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['X'])
def test_cliente_valor_no_limite_e_aceito(limite):
    assert criar(cliente=limite).cliente == limite


@pytest.mark.parametrize("invalido", [0, -9, 2.5, '3', True, None])
def test_mesa_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(mesa=invalido)


def test_mesa_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.mesa = 0
    assert obj.mesa == DADOS_EXEMPLO[0]["mesa"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1])
def test_mesa_valor_no_limite_e_aceito(limite):
    assert criar(mesa=limite).mesa == limite


@pytest.mark.parametrize("invalido", [0, 21, 2.5, '3', True, None])
def test_pratos_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(pratos=invalido)


def test_pratos_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.pratos = 0
    assert obj.pratos == DADOS_EXEMPLO[0]["pratos"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 20])
def test_pratos_valor_no_limite_e_aceito(limite):
    assert criar(pratos=limite).pratos == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_preco_prato_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(preco_prato=invalido)


def test_preco_prato_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.preco_prato = -0.01
    assert obj.preco_prato == DADOS_EXEMPLO[0]["preco_prato"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_preco_prato_valor_no_limite_e_aceito(limite):
    assert criar(preco_prato=limite).preco_prato == limite


@pytest.mark.parametrize("invalido", ['2026-01-10', '2026-02-30T10:00', '10/01/2026 09:30', '', 20260110, None])
def test_horario_pedido_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(horario_pedido=invalido)


def test_horario_pedido_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.horario_pedido = '2026-01-10'
    assert obj.horario_pedido == DADOS_EXEMPLO[0]["horario_pedido"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['2000-01-01T00:00', '2099-12-31T23:59', '2028-02-29T12:30'])
def test_horario_pedido_valor_no_limite_e_aceito(limite):
    assert criar(horario_pedido=limite).horario_pedido == limite

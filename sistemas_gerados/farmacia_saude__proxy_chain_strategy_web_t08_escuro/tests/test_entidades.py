"""Testes da Receita (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.unidades * obj.preco_unitario, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.unidades = obj.unidades + 1
    assert obj.total == round(obj.unidades * obj.preco_unitario, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(cliente="  Ana  ").cliente == "Ana"


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
def test_balcao_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(balcao=invalido)


def test_balcao_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.balcao = 0
    assert obj.balcao == DADOS_EXEMPLO[0]["balcao"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1])
def test_balcao_valor_no_limite_e_aceito(limite):
    assert criar(balcao=limite).balcao == limite


@pytest.mark.parametrize("invalido", [0, 21, 2.5, '3', True, None])
def test_unidades_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(unidades=invalido)


def test_unidades_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.unidades = 0
    assert obj.unidades == DADOS_EXEMPLO[0]["unidades"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 20])
def test_unidades_valor_no_limite_e_aceito(limite):
    assert criar(unidades=limite).unidades == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_preco_unitario_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(preco_unitario=invalido)


def test_preco_unitario_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.preco_unitario = -0.01
    assert obj.preco_unitario == DADOS_EXEMPLO[0]["preco_unitario"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_preco_unitario_valor_no_limite_e_aceito(limite):
    assert criar(preco_unitario=limite).preco_unitario == limite


@pytest.mark.parametrize("invalido", ['', '11.111.111/1111-11', '11.222.333/0001-00', '12345', 11222333000181, None])
def test_cnpj_fornecedor_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(cnpj_fornecedor=invalido)


def test_cnpj_fornecedor_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.cnpj_fornecedor = ''
    assert obj.cnpj_fornecedor == DADOS_EXEMPLO[0]["cnpj_fornecedor"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['11.222.333/0001-81', '11.444.777/0001-61'])
def test_cnpj_fornecedor_valor_no_limite_e_aceito(limite):
    assert criar(cnpj_fornecedor=limite).cnpj_fornecedor == limite


@pytest.mark.parametrize("invalido", ['nao-json', 123, True, None])
def test_metadados_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(metadados=invalido)


def test_metadados_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.metadados = 'nao-json'
    assert obj.metadados == DADOS_EXEMPLO[0]["metadados"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [{'ok': True}, [1, 2]])
def test_metadados_valor_no_limite_e_aceito(limite):
    assert criar(metadados=limite).metadados == limite

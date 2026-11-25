"""Testes da Frete (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.toneladas * obj.valor_tonelada, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.toneladas = obj.toneladas + 1
    assert obj.total == round(obj.toneladas * obj.valor_tonelada, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(cliente="  Elisa  ").cliente == "Elisa"


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
def test_caminhao_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(caminhao=invalido)


def test_caminhao_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.caminhao = 0
    assert obj.caminhao == DADOS_EXEMPLO[0]["caminhao"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1])
def test_caminhao_valor_no_limite_e_aceito(limite):
    assert criar(caminhao=limite).caminhao == limite


@pytest.mark.parametrize("invalido", [0, 41, 2.5, '3', True, None])
def test_toneladas_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(toneladas=invalido)


def test_toneladas_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.toneladas = 0
    assert obj.toneladas == DADOS_EXEMPLO[0]["toneladas"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 40])
def test_toneladas_valor_no_limite_e_aceito(limite):
    assert criar(toneladas=limite).toneladas == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_valor_tonelada_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(valor_tonelada=invalido)


def test_valor_tonelada_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.valor_tonelada = -0.01
    assert obj.valor_tonelada == DADOS_EXEMPLO[0]["valor_tonelada"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_valor_tonelada_valor_no_limite_e_aceito(limite):
    assert criar(valor_tonelada=limite).valor_tonelada == limite


@pytest.mark.parametrize("invalido", ['', 'abc,def', '95.0,-46.6', '-23.5,200.0', '-23.5', None])
def test_coordenadas_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(coordenadas=invalido)


def test_coordenadas_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.coordenadas = ''
    assert obj.coordenadas == DADOS_EXEMPLO[0]["coordenadas"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['-90,180', '90,-180', '-23.5505,-46.6333'])
def test_coordenadas_valor_no_limite_e_aceito(limite):
    assert criar(coordenadas=limite).coordenadas == limite


@pytest.mark.parametrize("invalido", ['', '   ', 'opcao_inexistente', 'fragil,opcao_inexistente', 123, None])
def test_etiquetas_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(etiquetas=invalido)


def test_etiquetas_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.etiquetas = ''
    assert obj.etiquetas == DADOS_EXEMPLO[0]["etiquetas"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['fragil', 'fragil,urgente,refrigerado'])
def test_etiquetas_valor_no_limite_e_aceito(limite):
    assert criar(etiquetas=limite).etiquetas == limite

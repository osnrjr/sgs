"""Testes da ParqueAerogerador (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.megawatts * obj.preco_mwh, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.megawatts = obj.megawatts + 1
    assert obj.total == round(obj.megawatts * obj.preco_mwh, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(operador="  Ana  ").operador == "Ana"


def test_observacao_sem_regra_aceita_qualquer_texto():
    assert criar().observacao == ""
    assert criar(observacao="qualquer coisa").observacao == "qualquer coisa"


@pytest.mark.parametrize("invalido", ['', '   ', 123, None])
def test_operador_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(operador=invalido)


def test_operador_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.operador = ''
    assert obj.operador == DADOS_EXEMPLO[0]["operador"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['X'])
def test_operador_valor_no_limite_e_aceito(limite):
    assert criar(operador=limite).operador == limite


@pytest.mark.parametrize("invalido", [0, -9, 2.5, '3', True, None])
def test_torre_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(torre=invalido)


def test_torre_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.torre = 0
    assert obj.torre == DADOS_EXEMPLO[0]["torre"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1])
def test_torre_valor_no_limite_e_aceito(limite):
    assert criar(torre=limite).torre == limite


@pytest.mark.parametrize("invalido", [0, 51, 2.5, '3', True, None])
def test_megawatts_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(megawatts=invalido)


def test_megawatts_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.megawatts = 0
    assert obj.megawatts == DADOS_EXEMPLO[0]["megawatts"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 50])
def test_megawatts_valor_no_limite_e_aceito(limite):
    assert criar(megawatts=limite).megawatts == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_preco_mwh_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(preco_mwh=invalido)


def test_preco_mwh_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.preco_mwh = -0.01
    assert obj.preco_mwh == DADOS_EXEMPLO[0]["preco_mwh"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_preco_mwh_valor_no_limite_e_aceito(limite):
    assert criar(preco_mwh=limite).preco_mwh == limite


@pytest.mark.parametrize("invalido", ['', 'abc,def', '95.0,-46.6', '-23.5,200.0', '-23.5', None])
def test_geoloc_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(geoloc=invalido)


def test_geoloc_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.geoloc = ''
    assert obj.geoloc == DADOS_EXEMPLO[0]["geoloc"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['-90,180', '90,-180', '-23.5505,-46.6333'])
def test_geoloc_valor_no_limite_e_aceito(limite):
    assert criar(geoloc=limite).geoloc == limite


@pytest.mark.parametrize("invalido", ['nao-json', 123, True, None])
def test_parametros_json_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(parametros_json=invalido)


def test_parametros_json_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.parametros_json = 'nao-json'
    assert obj.parametros_json == DADOS_EXEMPLO[0]["parametros_json"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [{'ok': True}, [1, 2]])
def test_parametros_json_valor_no_limite_e_aceito(limite):
    assert criar(parametros_json=limite).parametros_json == limite

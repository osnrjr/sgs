"""Testes da Contrato (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.meses * obj.valor_aluguel, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.meses = obj.meses + 1
    assert obj.total == round(obj.meses * obj.valor_aluguel, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(locatario="  Danilo  ").locatario == "Danilo"


def test_observacao_sem_regra_aceita_qualquer_texto():
    assert criar().observacao == ""
    assert criar(observacao="qualquer coisa").observacao == "qualquer coisa"


@pytest.mark.parametrize("invalido", ['', '   ', 123, None])
def test_locatario_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(locatario=invalido)


def test_locatario_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.locatario = ''
    assert obj.locatario == DADOS_EXEMPLO[0]["locatario"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['X'])
def test_locatario_valor_no_limite_e_aceito(limite):
    assert criar(locatario=limite).locatario == limite


@pytest.mark.parametrize("invalido", [0, -9, 2.5, '3', True, None])
def test_imovel_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(imovel=invalido)


def test_imovel_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.imovel = 0
    assert obj.imovel == DADOS_EXEMPLO[0]["imovel"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1])
def test_imovel_valor_no_limite_e_aceito(limite):
    assert criar(imovel=limite).imovel == limite


@pytest.mark.parametrize("invalido", [0, 37, 2.5, '3', True, None])
def test_meses_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(meses=invalido)


def test_meses_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.meses = 0
    assert obj.meses == DADOS_EXEMPLO[0]["meses"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 36])
def test_meses_valor_no_limite_e_aceito(limite):
    assert criar(meses=limite).meses == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_valor_aluguel_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(valor_aluguel=invalido)


def test_valor_aluguel_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.valor_aluguel = -0.01
    assert obj.valor_aluguel == DADOS_EXEMPLO[0]["valor_aluguel"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_valor_aluguel_valor_no_limite_e_aceito(limite):
    assert criar(valor_aluguel=limite).valor_aluguel == limite


@pytest.mark.parametrize("invalido", ['', '   ', 123, None])
def test_descricao_completa_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(descricao_completa=invalido)


def test_descricao_completa_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.descricao_completa = ''
    assert obj.descricao_completa == DADOS_EXEMPLO[0]["descricao_completa"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['X'])
def test_descricao_completa_valor_no_limite_e_aceito(limite):
    assert criar(descricao_completa=limite).descricao_completa == limite


@pytest.mark.parametrize("invalido", ['', 'documento.pdf', 'foto_sem_extensao', 'planilha.xlsx', 123, None])
def test_foto_capa_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(foto_capa=invalido)


def test_foto_capa_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.foto_capa = ''
    assert obj.foto_capa == DADOS_EXEMPLO[0]["foto_capa"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['foto.png', 'https://exemplo.com.br/banner.webp'])
def test_foto_capa_valor_no_limite_e_aceito(limite):
    assert criar(foto_capa=limite).foto_capa == limite

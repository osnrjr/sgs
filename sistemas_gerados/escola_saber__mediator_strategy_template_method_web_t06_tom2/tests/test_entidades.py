"""Testes da Turma (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.meses * obj.mensalidade, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.meses = obj.meses + 1
    assert obj.total == round(obj.meses * obj.mensalidade, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(aluno="  Márcio  ").aluno == "Márcio"


def test_observacao_sem_regra_aceita_qualquer_texto():
    assert criar().observacao == ""
    assert criar(observacao="qualquer coisa").observacao == "qualquer coisa"


@pytest.mark.parametrize("invalido", ['', '   ', 123, None])
def test_aluno_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(aluno=invalido)


def test_aluno_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.aluno = ''
    assert obj.aluno == DADOS_EXEMPLO[0]["aluno"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['X'])
def test_aluno_valor_no_limite_e_aceito(limite):
    assert criar(aluno=limite).aluno == limite


@pytest.mark.parametrize("invalido", [0, -9, 2.5, '3', True, None])
def test_sala_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(sala=invalido)


def test_sala_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.sala = 0
    assert obj.sala == DADOS_EXEMPLO[0]["sala"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1])
def test_sala_valor_no_limite_e_aceito(limite):
    assert criar(sala=limite).sala == limite


@pytest.mark.parametrize("invalido", [0, 13, 2.5, '3', True, None])
def test_meses_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(meses=invalido)


def test_meses_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.meses = 0
    assert obj.meses == DADOS_EXEMPLO[0]["meses"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 12])
def test_meses_valor_no_limite_e_aceito(limite):
    assert criar(meses=limite).meses == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_mensalidade_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(mensalidade=invalido)


def test_mensalidade_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.mensalidade = -0.01
    assert obj.mensalidade == DADOS_EXEMPLO[0]["mensalidade"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_mensalidade_valor_no_limite_e_aceito(limite):
    assert criar(mensalidade=limite).mensalidade == limite


@pytest.mark.parametrize("invalido", ['', 'exemplo.com', 'ftp://exemplo.com', 'http://', 123, None])
def test_portal_url_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(portal_url=invalido)


def test_portal_url_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.portal_url = ''
    assert obj.portal_url == DADOS_EXEMPLO[0]["portal_url"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['http://exemplo.com', 'https://exemplo.com.br/recurso'])
def test_portal_url_valor_no_limite_e_aceito(limite):
    assert criar(portal_url=limite).portal_url == limite


@pytest.mark.parametrize("invalido", ['', '   ', 'sem_extensao', 'arquivo.', 123, None])
def test_comprovante_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(comprovante=invalido)


def test_comprovante_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.comprovante = ''
    assert obj.comprovante == DADOS_EXEMPLO[0]["comprovante"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['doc.pdf', 'https://exemplo.com.br/anexo.xlsx'])
def test_comprovante_valor_no_limite_e_aceito(limite):
    assert criar(comprovante=limite).comprovante == limite

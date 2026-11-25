"""Testes da Consulta (ENCAPSULAMENTO): regras, LIMITES e total calculado."""
import pytest

from tests.fabrica import DADOS_EXEMPLO, criar, itens_exemplo


def test_cria_com_dados_validos():
    obj = criar()
    for campo, valor in DADOS_EXEMPLO[0].items():
        assert getattr(obj, campo) == valor


def test_total_e_quantidade_vezes_preco():
    for obj in itens_exemplo():
        assert obj.total == round(obj.sessoes * obj.valor_sessao, 2)


def test_total_acompanha_mudanca():
    obj = criar()
    obj.sessoes = obj.sessoes + 1
    assert obj.total == round(obj.sessoes * obj.valor_sessao, 2)


def test_total_e_somente_leitura():
    with pytest.raises(AttributeError):
        criar().total = 1


def test_texto_obrigatorio_e_guardado_sem_espacos():
    assert criar(paciente="  Sérgio  ").paciente == "Sérgio"


def test_anotacao_sem_regra_aceita_qualquer_texto():
    assert criar().anotacao == ""
    assert criar(anotacao="qualquer coisa").anotacao == "qualquer coisa"


@pytest.mark.parametrize("invalido", ['', '   ', 123, None])
def test_paciente_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(paciente=invalido)


def test_paciente_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.paciente = ''
    assert obj.paciente == DADOS_EXEMPLO[0]["paciente"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['X'])
def test_paciente_valor_no_limite_e_aceito(limite):
    assert criar(paciente=limite).paciente == limite


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
def test_sessoes_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(sessoes=invalido)


def test_sessoes_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.sessoes = 0
    assert obj.sessoes == DADOS_EXEMPLO[0]["sessoes"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [1, 12])
def test_sessoes_valor_no_limite_e_aceito(limite):
    assert criar(sessoes=limite).sessoes == limite


@pytest.mark.parametrize("invalido", [-0.01, -10, '10', True, None])
def test_valor_sessao_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(valor_sessao=invalido)


def test_valor_sessao_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.valor_sessao = -0.01
    assert obj.valor_sessao == DADOS_EXEMPLO[0]["valor_sessao"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", [0.0])
def test_valor_sessao_valor_no_limite_e_aceito(limite):
    assert criar(valor_sessao=limite).valor_sessao == limite


@pytest.mark.parametrize("invalido", ['', '111.111.111-11', '123.456.789-00', '12345', 12345678909, None])
def test_cpf_paciente_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(cpf_paciente=invalido)


def test_cpf_paciente_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.cpf_paciente = ''
    assert obj.cpf_paciente == DADOS_EXEMPLO[0]["cpf_paciente"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['123.456.789-09', '987.654.321-00'])
def test_cpf_paciente_valor_no_limite_e_aceito(limite):
    assert criar(cpf_paciente=limite).cpf_paciente == limite


@pytest.mark.parametrize("invalido", ['', '12345', 'abcdef', '11999999999999', 11999999999, None])
def test_telefone_contato_invalido_e_barrado_na_criacao(invalido):
    with pytest.raises(ValueError):
        criar(telefone_contato=invalido)


def test_telefone_contato_invalido_e_barrado_na_alteracao():
    obj = criar()
    with pytest.raises(ValueError):
        obj.telefone_contato = ''
    assert obj.telefone_contato == DADOS_EXEMPLO[0]["telefone_contato"]  # o valor válido foi preservado


@pytest.mark.parametrize("limite", ['1133334444', '(11) 99999-1111'])
def test_telefone_contato_valor_no_limite_e_aceito(limite):
    assert criar(telefone_contato=limite).telefone_contato == limite

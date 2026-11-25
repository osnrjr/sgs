"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from consultas.models import Consulta
from consultas.services import POLITICAS, ConsultaService


def novo(**mudancas):
    copia = {"paciente": 'Sérgio', "sala": 101, "sessoes": 2, "valor_sessao": Decimal("150.00"), "cpf_paciente": '123.456.789-09', "telefone_contato": '(11) 99999-1111', "tipo": "particular"}
    copia.update(mudancas)
    return Consulta(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("particular", 1.0), ("convenio_ouro", 0.6), ("convenio_prata", 0.75), ("empresa", 0.5)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert ConsultaService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in Consulta.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = ConsultaService().resumo([novo(), novo(tipo="convenio_ouro")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(ConsultaService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

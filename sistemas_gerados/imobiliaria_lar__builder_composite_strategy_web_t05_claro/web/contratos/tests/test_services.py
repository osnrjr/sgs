"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from contratos.models import Contrato
from contratos.services import POLITICAS, ContratoService


def novo(**mudancas):
    copia = {"locatario": 'Danilo', "imovel": 101, "meses": 2, "valor_aluguel": Decimal("1800.00"), "descricao_completa": 'Descrição detalhada de descricao completa 1.', "foto_capa": 'imagens/foto_1.png', "tipo": "residencial"}
    copia.update(mudancas)
    return Contrato(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("residencial", 1.0), ("comercial", 1.2), ("estudante", 0.9), ("corporativo", 1.1)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert ContratoService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in Contrato.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = ContratoService().resumo([novo(), novo(tipo="comercial")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(ContratoService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

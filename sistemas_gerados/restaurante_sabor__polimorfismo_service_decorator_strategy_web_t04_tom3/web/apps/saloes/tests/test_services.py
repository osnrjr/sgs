"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from apps.saloes.models import Salao
from apps.saloes.services import POLITICAS, SalaoService


def novo(**mudancas):
    copia = {"cliente": 'Márcio', "mesa": 101, "pratos": 2, "preco_prato": Decimal("58.00"), "tipo": "comum"}
    copia.update(mudancas)
    return Salao(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("comum", 1.0), ("fidelidade", 0.9), ("empresa", 0.85), ("aniversariante", 0.8)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert SalaoService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in Salao.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = SalaoService().resumo([novo(), novo(tipo="fidelidade")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(SalaoService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

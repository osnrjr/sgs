"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from receitas.models import Receita
from receitas.services import POLITICAS, ReceitaService


def novo(**mudancas):
    copia = {"cliente": 'Ana', "balcao": 101, "unidades": 2, "preco_unitario": Decimal("25.90"), "cnpj_fornecedor": '11.222.333/0001-81', "metadados": {'chave': 'metadados_1', 'ativo': True}, "tipo": "comum"}
    copia.update(mudancas)
    return Receita(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("comum", 1.0), ("convenio", 0.85), ("idoso", 0.9), ("farmacia_popular", 0.1)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert ReceitaService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in Receita.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = ReceitaService().resumo([novo(), novo(tipo="convenio")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(ReceitaService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

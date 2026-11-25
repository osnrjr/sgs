"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from fretes.models import Frete
from fretes.services import POLITICAS, FreteService


def novo(**mudancas):
    copia = {"cliente": 'Elisa', "caminhao": 101, "toneladas": 2, "valor_tonelada": Decimal("280.00"), "coordenadas": '-23.5505,-46.6333', "etiquetas": 'fragil', "tipo": "spot"}
    copia.update(mudancas)
    return Frete(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("spot", 1.0), ("contrato", 0.85), ("industria", 0.9), ("retorno", 0.6)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert FreteService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in Frete.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = FreteService().resumo([novo(), novo(tipo="contrato")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(FreteService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from parque_aerogeradores.models import ParqueAerogerador
from parque_aerogeradores.services import POLITICAS, ParqueAerogeradorService


def novo(**mudancas):
    copia = {"operador": 'Ana', "torre": 101, "megawatts": 2, "preco_mwh": Decimal("220.00"), "geoloc": '-23.5505,-46.6333', "parametros_json": {'chave': 'parametros_json_1', 'ativo': True}, "tipo": "padrao"}
    copia.update(mudancas)
    return ParqueAerogerador(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("padrao", 1.0), ("corporativo", 0.9), ("recorrente", 0.85), ("emergencial", 1.3)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert ParqueAerogeradorService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in ParqueAerogerador.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = ParqueAerogeradorService().resumo([novo(), novo(tipo="corporativo")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(ParqueAerogeradorService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

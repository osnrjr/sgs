"""Testes do SERVICE web: regra sem HTTP, reaproveitando o Strategy do núcleo."""
import ast
import inspect
import textwrap
from decimal import Decimal

import pytest

from turmas.models import Turma
from turmas.services import POLITICAS, TurmaService


def novo(**mudancas):
    copia = {"aluno": 'Márcio', "sala": 101, "meses": 2, "mensalidade": Decimal("850.00"), "portal_url": 'https://exemplo.com.br/item-1', "comprovante": 'documentos/anexo_1.pdf', "tipo": "regular"}
    copia.update(mudancas)
    return Turma(**copia)  # objeto em memória: nem precisa de banco


@pytest.mark.parametrize("tipo, fator", [("regular", 1.0), ("irmaos", 0.9), ("bolsista", 0.5), ("filho_de_professor", 0.4)])
def test_valor_final_usa_a_politica_do_nucleo(tipo, fator):
    obj = novo(tipo=tipo)
    assert TurmaService().valor_final(obj) == round(float(obj.total) * fator, 2)


def test_todo_tipo_do_model_tem_politica():
    assert set(POLITICAS) == {chave for chave, _ in Turma.TIPOS}


def test_resumo_soma_os_valores():
    itens, total = TurmaService().resumo([novo(), novo(tipo="irmaos")])
    assert len(itens) == 2 and total == round(sum(v for _, v in itens), 2)


def test_service_nao_conhece_web():
    arvore = ast.parse(textwrap.dedent(inspect.getsource(TurmaService)))
    nomes = {n.id.lower() for n in ast.walk(arvore) if isinstance(n, ast.Name)}
    nomes |= {n.attr.lower() for n in ast.walk(arvore) if isinstance(n, ast.Attribute)}
    nomes |= {n.arg.lower() for n in ast.walk(arvore) if isinstance(n, ast.arg)}
    for palavra in ("request", "http", "template", "render"):
        assert not any(palavra in nome for nome in nomes), palavra

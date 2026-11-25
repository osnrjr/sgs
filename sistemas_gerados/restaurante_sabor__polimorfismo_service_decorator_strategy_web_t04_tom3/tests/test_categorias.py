"""Testes do POLIMORFISMO: mesma saída que o if/elif, e categoria nova sem mudar a função."""
import pytest

from nucleo import antes_categorias
from nucleo.categorias import Massa, PratoChef, PratoExecutivo, PratoExecutivoPadrao, Salada, imprimir_preco


@pytest.mark.parametrize("classe, tipo", [(PratoChef, "prato_chef"), (Massa, "massa")])
def test_mesmo_texto_que_a_versao_com_if(classe, tipo):
    assert imprimir_preco(classe(1)) == antes_categorias.imprimir_preco(tipo)


def test_base_igual_ao_else_da_versao_antiga():
    assert imprimir_preco(PratoExecutivo(1)) == antes_categorias.imprimir_preco("qualquer")


@pytest.mark.parametrize("classe", [PratoChef, Massa, Salada, PratoExecutivoPadrao])
def test_todo_subtipo_e_um_prato_executivo(classe):
    assert isinstance(classe(1), PratoExecutivo)


def test_subtipo_herda_o_construtor():
    assert PratoChef(7).codigo == 7


def test_categoria_nova_sem_mudar_a_funcao():
    assert imprimir_preco(Salada(1)) == "Salada: R$ 38.00 por prato"


def test_quem_nao_sobrescreve_usa_o_metodo_da_mae():
    assert imprimir_preco(PratoExecutivoPadrao(1)) == imprimir_preco(PratoExecutivo(1))


def test_versao_com_if_erra_a_categoria_nova():
    assert antes_categorias.imprimir_preco("salada") != imprimir_preco(Salada(1))

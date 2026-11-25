"""Testes do MEMENTO: salvar, restaurar várias versões e não expor o interior."""
import pytest

from nucleo.antes_versoes import restaurar_antigo, salvar_antigo
from nucleo.versoes import EditorParqueAerogerador, HistoricoDeVersoes
from tests.fabrica import criar


def test_restaurar_volta_ao_estado_salvo():
    item = criar()
    editor = EditorParqueAerogerador(item)
    versao = editor.salvar("original")
    editor.alterar("megawatts", item.megawatts + 1)
    editor.restaurar(versao)
    assert vars(item) == vars(criar())


def test_memento_e_uma_copia():
    item = criar()
    versao = EditorParqueAerogerador(item).salvar()
    item.megawatts = item.megawatts + 1
    assert versao._estado != vars(item)


def test_historico_volta_varias_versoes():
    item = criar()
    editor, historico = EditorParqueAerogerador(item), HistoricoDeVersoes()
    q0 = item.megawatts
    for passo in (1, 2):
        historico.guardar(editor.salvar(f"antes do passo {passo}"))
        editor.alterar("megawatts", q0 + passo)
    assert historico.rotulos() == ["antes do passo 1", "antes do passo 2"]
    editor.restaurar(historico.ultima())
    assert item.megawatts == q0 + 1
    editor.restaurar(historico.ultima())
    assert item.megawatts == q0
    assert historico.ultima() is None


def test_alteracao_invalida_continua_barrada():
    with pytest.raises(ValueError):
        EditorParqueAerogerador(criar()).alterar("megawatts", 0)


def test_mesmo_resultado_da_copia_na_mao():
    a, b = criar(), criar()
    copia = salvar_antigo(a)
    versao = EditorParqueAerogerador(b).salvar()
    a.megawatts = a.megawatts + 1
    b.megawatts = b.megawatts + 1
    restaurar_antigo(a, copia)
    EditorParqueAerogerador(b).restaurar(versao)
    assert vars(a) == vars(b)

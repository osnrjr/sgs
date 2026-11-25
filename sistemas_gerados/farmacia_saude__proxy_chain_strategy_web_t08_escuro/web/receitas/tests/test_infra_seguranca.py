"""Testes de infraestrutura, segurança e bibliotecas escolhidas na geração do sistema."""
import pytest


def test_criptografia_fernet_ida_e_volta():
    from config.crypto import cifrar, decifrar
    token = cifrar("123.456.789-09")
    assert token != "123.456.789-09" and decifrar(token) == "123.456.789-09"
    with pytest.raises(ValueError):
        decifrar("enc:token-corrompido")

def test_rbac_matriz_de_permissoes_e_decorator():
    from django.http import HttpResponse
    from django.test import RequestFactory
    from config.rbac import exigir_papel, tem_permissao
    assert tem_permissao("admin", "configurar") is True
    assert tem_permissao("leitor", "apagar") is False
    view = exigir_papel("admin", "gestor")(lambda req: HttpResponse("ok"))
    rf = RequestFactory()
    assert view(rf.get("/", HTTP_X_PAPEL="leitor")).status_code == 403
    assert view(rf.get("/", HTTP_X_PAPEL="gestor")).status_code == 200

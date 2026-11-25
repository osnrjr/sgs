"""Testes de infraestrutura, segurança e bibliotecas escolhidas na geração do sistema."""
import pytest


def test_criptografia_fernet_ida_e_volta():
    from config.crypto import cifrar, decifrar
    token = cifrar("123.456.789-09")
    assert token != "123.456.789-09" and decifrar(token) == "123.456.789-09"
    with pytest.raises(ValueError):
        decifrar("enc:token-corrompido")

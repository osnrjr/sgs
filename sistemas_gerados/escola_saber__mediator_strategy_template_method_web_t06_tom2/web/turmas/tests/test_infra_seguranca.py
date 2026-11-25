"""Testes de infraestrutura, segurança e bibliotecas escolhidas na geração do sistema."""
import pytest


def test_hash_de_senha_usa_argon2id(settings):
    from django.contrib.auth.hashers import make_password
    assert "Argon2PasswordHasher" in settings.PASSWORD_HASHERS[0]
    assert make_password("SenhaForte#123").startswith("argon2$")

def test_two_factor_codigo_valido_e_expiracao(settings):
    from config.twofactor import gerar_codigo, validar_codigo
    assert settings.TWO_FACTOR_EXPIRACAO_MIN == 15
    cod = gerar_codigo("usuario@exemplo.com", agora=1000.0)
    assert len(cod) == 6 and cod.isdigit()
    assert validar_codigo("usuario@exemplo.com", "000000", agora=1010.0) is False
    assert validar_codigo("usuario@exemplo.com", cod, agora=1010.0) is True
    cod2 = gerar_codigo("expira@exemplo.com", expiracao_min=5, agora=2000.0)
    assert validar_codigo("expira@exemplo.com", cod2, agora=2000.0 + 301.0) is False

def test_antibot_barra_honeypot_e_envio_instantaneo():
    from config.antibot import validar_envio
    assert validar_envio({"nome": "Ana", "_website": ""}, tempo_segundos=4.0)[0] is True
    assert validar_envio({"nome": "Bot", "_website": "http://spam"}, tempo_segundos=4.0)[0] is False
    assert validar_envio({"nome": "Bot", "_website": ""}, tempo_segundos=0.2)[0] is False

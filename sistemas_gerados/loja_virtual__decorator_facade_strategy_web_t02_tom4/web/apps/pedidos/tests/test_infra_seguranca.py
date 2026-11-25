"""Testes de infraestrutura, segurança e bibliotecas escolhidas na geração do sistema."""
import pytest


def test_banco_de_dados_configurado(settings):
    assert settings.BANCO_DADOS_CONFIGURADO == "postgresql"

def test_cache_redis_configurado(settings):
    assert settings.REDIS_ATIVO is True and "default" in settings.CACHES

def test_ratelimit_bloqueia_apos_limite():
    from config.ratelimit import verificar_limite
    assert verificar_limite("login:teste-rl", limite=2, janela_seg=60) is True
    assert verificar_limite("login:teste-rl", limite=2, janela_seg=60) is True
    assert verificar_limite("login:teste-rl", limite=2, janela_seg=60) is False

"""Testes de infraestrutura, segurança e bibliotecas escolhidas na geração do sistema."""
import pytest


def test_banco_de_dados_configurado(settings):
    assert settings.BANCO_DADOS_CONFIGURADO == "postgresql"

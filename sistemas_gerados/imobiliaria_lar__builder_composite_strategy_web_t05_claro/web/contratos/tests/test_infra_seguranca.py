"""Testes de infraestrutura, segurança e bibliotecas escolhidas na geração do sistema."""
import pytest


@pytest.mark.django_db
def test_rota_recuperacao_de_senha_disponivel(client, settings):
    assert settings.PASSWORD_RESET_TIMEOUT == 3600
    resposta = client.get("/conta/password_reset/")
    assert resposta.status_code == 200

def test_anymail_configurado(settings):
    assert settings.ANYMAIL_ATIVO is True and "PROVIDER" in settings.ANYMAIL

def test_tinymce_configurado(settings):
    assert settings.TINYMCE_ATIVO is True and "toolbar" in settings.TINYMCE_DEFAULT_CONFIG

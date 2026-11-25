"""Configuração do projeto Django (gerada). Valores sensíveis vêm do web/.env (modelo: web/.env.example)."""
import os
import sys
from pathlib import Path

from .env import carregar_env

BASE_DIR = Path(__file__).resolve().parent.parent
# O núcleo em Python puro (pasta ../nucleo) é usado pelo app: põe a pasta do sistema no path.
sys.path.insert(0, str(BASE_DIR.parent))
# Lê web/.env (se existir) para os.environ, sem sobrescrever o que já veio do ambiente.
carregar_env(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "somente-para-estudo-troque-no-env")
DEBUG = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")
ADMIN_URL = os.environ.get("ADMIN_URL", "admin/")  # endereço do Django Admin (lido em config/urls.py)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "turmas",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # destino do `manage.py collectstatic` (publicação)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Hash de senhas com Argon2id (§16.1).
try:
    import argon2  # noqa: F401
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher",
                        "django.contrib.auth.hashers.PBKDF2PasswordHasher"]
except ImportError:
    pass

# Autenticação em dois fatores (2FA — helper em config/twofactor.py).
TWO_FACTOR_ATIVO = True
TWO_FACTOR_EXPIRACAO_MIN = int(os.environ.get("TWO_FACTOR_EXPIRACAO_MIN", "15"))

# Proteção Anti-Bot (honeypot + tempo mínimo + chave de provedor — config/antibot.py).
ANTIBOT_ATIVO = True
ANTIBOT_PROVIDER = os.environ.get("ANTIBOT_PROVIDER", "honeypot")
ANTIBOT_SITE_KEY = os.environ.get("ANTIBOT_SITE_KEY", "")
ANTIBOT_SECRET_KEY = os.environ.get("ANTIBOT_SECRET_KEY", "")
ANTIBOT_TEMPO_MIN_SEG = 2

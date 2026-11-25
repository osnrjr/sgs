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
    "apps.pedidos",
    "apps.compradores",  # módulo (sgs app)
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


# Banco de dados principal: PostgreSQL (com fallback para SQLite3 se DB_HOST não estiver definido).
BANCO_DADOS_CONFIGURADO = "postgresql"
if os.environ.get("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "app_db"),
            "USER": os.environ.get("DB_USER", "app_user"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

# Cache distribuído: Redis (com fallback para LocMemCache local/testes quando REDIS_URL estiver vazio).
REDIS_ATIVO = True
REDIS_URL = os.environ.get("REDIS_URL", "")
if REDIS_URL:
    try:
        import django_redis  # noqa: F401
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": REDIS_URL,
                "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            }
        }
    except ImportError:
        CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# Limitação de taxa na aplicação (django-ratelimit, §19 — helper em config/ratelimit.py).
RATELIMIT_ENABLE = os.environ.get("RATELIMIT_ENABLE", "1") == "1"
RATELIMIT_USE_CACHE = "default"

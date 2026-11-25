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
    "contratos",
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


# Recuperação de usuário e senha (§16.3 — rotas em /conta/ e expiração de 1h).
RECUPERACAO_SENHA_ATIVA = True
PASSWORD_RESET_TIMEOUT = 3600
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "nao-responda@exemplo.com")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Envio transacional via django-anymail (usa console backend em testes/local sem API key).
ANYMAIL_ATIVO = True
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "nao-responda@exemplo.com")
ANYMAIL = {
    "PROVIDER": os.environ.get("ANYMAIL_PROVIDER", "mailgun"),
    "API_KEY": os.environ.get("ANYMAIL_API_KEY", ""),
}
if ANYMAIL["API_KEY"]:
    try:
        import anymail  # noqa: F401
        INSTALLED_APPS.append("anymail")
        EMAIL_BACKEND = f"anymail.backends.{ANYMAIL['PROVIDER']}.EmailBackend"
    except ImportError:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Editor Rich-Text TinyMCE para campos de texto longo.
TINYMCE_ATIVO = True
TINYMCE_DEFAULT_CONFIG = {
    "height": 280,
    "menubar": False,
    "plugins": "lists link code",
    "toolbar": "undo redo | bold italic | bullist numlist | link",
}
try:
    import tinymce  # noqa: F401
    INSTALLED_APPS.append("tinymce")
except ImportError:
    pass

"""Limitação de taxa na aplicação (§19), compatível com django-ratelimit e cache do Django."""
from django.conf import settings
from django.core.cache import caches


def verificar_limite(chave, limite=5, janela_seg=60):
    if not getattr(settings, "RATELIMIT_ENABLE", True):
        return True
    cache = caches[getattr(settings, "RATELIMIT_USE_CACHE", "default")]
    chave_cache = f"rl:{chave}"
    atual = cache.get(chave_cache, 0)
    if atual >= limite:
        return False
    cache.set(chave_cache, atual + 1, timeout=janela_seg)
    return True

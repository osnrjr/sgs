"""Autenticação em dois fatores (2FA) com expiração configurável (TWO_FACTOR_EXPIRACAO_MIN)."""
import secrets
import time

from django.conf import settings

_PENDENTES = {}


def gerar_codigo(identificador, expiracao_min=None, agora=None):
    minutos = int(expiracao_min if expiracao_min is not None else getattr(settings, "TWO_FACTOR_EXPIRACAO_MIN", 10))
    instante = time.time() if agora is None else float(agora)
    codigo = f"{secrets.randbelow(1_000_000):06d}"
    _PENDENTES[str(identificador)] = (codigo, instante + minutos * 60)
    return codigo


def validar_codigo(identificador, codigo, agora=None):
    chave = str(identificador)
    registro = _PENDENTES.get(chave)
    if not registro:
        return False
    esperado, expira_em = registro
    instante = time.time() if agora is None else float(agora)
    if instante > expira_em:
        _PENDENTES.pop(chave, None)
        return False
    if secrets.compare_digest(str(codigo).strip(), esperado):
        _PENDENTES.pop(chave, None)
        return True
    return False

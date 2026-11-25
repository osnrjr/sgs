"""Proteção Anti-Bot: honeypot + tempo mínimo humano + suporte a provedor externo."""
from django.conf import settings


def validar_envio(dados, tempo_segundos=5.0):
    if str((dados or {}).get("_website", "")).strip():
        return False, "honeypot preenchido"
    minimo = float(getattr(settings, "ANTIBOT_TEMPO_MIN_SEG", 2))
    if float(tempo_segundos) < minimo:
        return False, "envio rápido demais"
    return True, "ok"

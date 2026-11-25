"""Criptografia simétrica em repouso com Fernet (§18.1) e fallback determinístico sem pacote extra."""
import base64
import hashlib
import hmac

from django.conf import settings


def _chave_bytes():
    bruta = (getattr(settings, "FERNET_KEY", "") or settings.SECRET_KEY).encode("utf-8")
    return base64.urlsafe_b64encode(hashlib.sha256(bruta).digest())


def cifrar(texto):
    if not isinstance(texto, str) or not texto:
        raise ValueError("texto obrigatório para cifrar")
    try:
        from cryptography.fernet import Fernet
        return "fernet:" + Fernet(_chave_bytes()).encrypt(texto.encode("utf-8")).decode("ascii")
    except ImportError:
        chave = _chave_bytes()
        dados = texto.encode("utf-8")
        fluxo = hashlib.sha256(chave).digest()
        cifrado = bytes(b ^ fluxo[i % len(fluxo)] for i, b in enumerate(dados))
        tag = hmac.new(chave, cifrado, hashlib.sha256).digest()[:16]
        return "enc:" + base64.urlsafe_b64encode(tag + cifrado).decode("ascii")


def decifrar(token):
    if not isinstance(token, str) or ":" not in token:
        raise ValueError("token inválido")
    pref, corpo = token.split(":", 1)
    if pref == "fernet":
        from cryptography.fernet import Fernet
        return Fernet(_chave_bytes()).decrypt(corpo.encode("ascii")).decode("utf-8")
    if pref == "enc":
        chave = _chave_bytes()
        bruto = base64.urlsafe_b64decode(corpo.encode("ascii"))
        tag, cifrado = bruto[:16], bruto[16:]
        esperado = hmac.new(chave, cifrado, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(tag, esperado):
            raise ValueError("integridade inválida")
        fluxo = hashlib.sha256(chave).digest()
        return bytes(b ^ fluxo[i % len(fluxo)] for i, b in enumerate(cifrado)).decode("utf-8")
    raise ValueError("formato de token desconhecido")

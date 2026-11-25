"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from parque_aerogeradores.models import ParqueAerogerador


def dados(**mudancas):
    copia = {"operador": 'Ana', "torre": 101, "megawatts": 2, "preco_mwh": Decimal("220.00"), "geoloc": '-23.5505,-46.6333', "parametros_json": {'chave': 'parametros_json_1', 'ativo': True}, "tipo": "padrao"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = ParqueAerogerador.objects.create(**dados())
    assert obj.total == Decimal("440.00")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    ParqueAerogerador(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("operador", ""), ("torre", 0), ("megawatts", 0), ("megawatts", 51), ("preco_mwh", Decimal("-1.00")), ("geoloc", "95.0,200.0"), ("parametros_json", None)])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        ParqueAerogerador(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    ParqueAerogerador(**dados(megawatts=0)).save()
    assert ParqueAerogerador.objects.count() == 1

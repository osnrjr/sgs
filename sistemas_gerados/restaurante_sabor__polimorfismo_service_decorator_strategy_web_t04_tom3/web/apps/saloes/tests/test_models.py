"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.saloes.models import Salao


def dados(**mudancas):
    copia = {"cliente": 'Márcio', "mesa": 101, "pratos": 2, "preco_prato": Decimal("58.00"), "tipo": "comum"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = Salao.objects.create(**dados())
    assert obj.total == Decimal("116.00")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    Salao(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("cliente", ""), ("mesa", 0), ("pratos", 0), ("pratos", 21), ("preco_prato", Decimal("-1.00"))])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        Salao(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    Salao(**dados(pratos=0)).save()
    assert Salao.objects.count() == 1

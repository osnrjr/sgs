"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from fretes.models import Frete


def dados(**mudancas):
    copia = {"cliente": 'Elisa', "caminhao": 101, "toneladas": 2, "valor_tonelada": Decimal("280.00"), "coordenadas": '-23.5505,-46.6333', "etiquetas": 'fragil', "tipo": "spot"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = Frete.objects.create(**dados())
    assert obj.total == Decimal("560.00")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    Frete(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("cliente", ""), ("caminhao", 0), ("toneladas", 0), ("toneladas", 41), ("valor_tonelada", Decimal("-1.00")), ("coordenadas", "95.0,200.0"), ("etiquetas", "opcao_inexistente")])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        Frete(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    Frete(**dados(toneladas=0)).save()
    assert Frete.objects.count() == 1

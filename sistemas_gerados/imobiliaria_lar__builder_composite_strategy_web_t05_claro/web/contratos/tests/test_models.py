"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from contratos.models import Contrato


def dados(**mudancas):
    copia = {"locatario": 'Danilo', "imovel": 101, "meses": 2, "valor_aluguel": Decimal("1800.00"), "descricao_completa": 'Descrição detalhada de descricao completa 1.', "foto_capa": 'imagens/foto_1.png', "tipo": "residencial"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = Contrato.objects.create(**dados())
    assert obj.total == Decimal("3600.00")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    Contrato(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("locatario", ""), ("imovel", 0), ("meses", 0), ("meses", 37), ("valor_aluguel", Decimal("-1.00")), ("descricao_completa", ""), ("foto_capa", "documento.pdf")])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        Contrato(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    Contrato(**dados(meses=0)).save()
    assert Contrato.objects.count() == 1

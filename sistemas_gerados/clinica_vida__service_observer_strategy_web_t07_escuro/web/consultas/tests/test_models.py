"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from consultas.models import Consulta


def dados(**mudancas):
    copia = {"paciente": 'Sérgio', "sala": 101, "sessoes": 2, "valor_sessao": Decimal("150.00"), "cpf_paciente": '123.456.789-09', "telefone_contato": '(11) 99999-1111', "tipo": "particular"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = Consulta.objects.create(**dados())
    assert obj.total == Decimal("300.00")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    Consulta(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("paciente", ""), ("sala", 0), ("sessoes", 0), ("sessoes", 13), ("valor_sessao", Decimal("-1.00")), ("cpf_paciente", "111.111.111-11"), ("telefone_contato", "12345")])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        Consulta(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    Consulta(**dados(sessoes=0)).save()
    assert Consulta.objects.count() == 1

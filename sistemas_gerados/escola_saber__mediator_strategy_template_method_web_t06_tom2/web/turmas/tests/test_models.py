"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from turmas.models import Turma


def dados(**mudancas):
    copia = {"aluno": 'Márcio', "sala": 101, "meses": 2, "mensalidade": Decimal("850.00"), "portal_url": 'https://exemplo.com.br/item-1', "comprovante": 'documentos/anexo_1.pdf', "tipo": "regular"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = Turma.objects.create(**dados())
    assert obj.total == Decimal("1700.00")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    Turma(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("aluno", ""), ("sala", 0), ("meses", 0), ("meses", 13), ("mensalidade", Decimal("-1.00")), ("portal_url", "nao-e-url"), ("comprovante", "sem_extensao")])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        Turma(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    Turma(**dados(meses=0)).save()
    assert Turma.objects.count() == 1

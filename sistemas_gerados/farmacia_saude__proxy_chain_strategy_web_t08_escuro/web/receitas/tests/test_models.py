"""Testes do MODEL: a validação mora nos validators (mundo Django) — e save() sozinho não valida."""
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from receitas.models import Receita


def dados(**mudancas):
    copia = {"cliente": 'Ana', "balcao": 101, "unidades": 2, "preco_unitario": Decimal("25.90"), "cnpj_fornecedor": '11.222.333/0001-81', "metadados": {'chave': 'metadados_1', 'ativo': True}, "tipo": "comum"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_cria_e_calcula_total():
    obj = Receita.objects.create(**dados())
    assert obj.total == Decimal("51.80")


@pytest.mark.django_db
def test_dados_validos_passam_no_full_clean():
    Receita(**dados()).full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("campo, valor", [("cliente", ""), ("balcao", 0), ("unidades", 0), ("unidades", 21), ("preco_unitario", Decimal("-1.00")), ("cnpj_fornecedor", "11.111.111/1111-11"), ("metadados", None)])
def test_full_clean_recusa_valor_invalido(campo, valor):
    with pytest.raises(ValidationError) as erro:
        Receita(**dados(**{campo: valor})).full_clean()
    assert campo in erro.value.message_dict


@pytest.mark.django_db
def test_save_sozinho_nao_valida():
    """Pegadinha dos 'dois mundos' (Aula 03): save() não chama full_clean()."""
    Receita(**dados(unidades=0)).save()
    assert Receita.objects.count() == 1

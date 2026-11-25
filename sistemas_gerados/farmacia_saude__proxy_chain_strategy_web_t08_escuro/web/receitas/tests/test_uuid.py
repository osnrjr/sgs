"""Teste do identificador UUIDv4 (Instruções §10.4)."""
import uuid
from decimal import Decimal

import pytest

from receitas.models import Receita


@pytest.mark.django_db
def test_chave_primaria_e_uuid4():
    obj = Receita.objects.create(**{"cliente": 'Ana', "balcao": 101, "unidades": 2, "preco_unitario": Decimal("25.90"), "cnpj_fornecedor": '11.222.333/0001-81', "metadados": {'chave': 'metadados_1', 'ativo': True}, "tipo": "comum"})
    assert isinstance(obj.pk, uuid.UUID) and obj.pk.version == 4

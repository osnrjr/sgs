"""Teste do identificador UUIDv4 (Instruções §10.4)."""
import uuid
from decimal import Decimal

import pytest

from consultas.models import Consulta


@pytest.mark.django_db
def test_chave_primaria_e_uuid4():
    obj = Consulta.objects.create(**{"paciente": 'Sérgio', "sala": 101, "sessoes": 2, "valor_sessao": Decimal("150.00"), "cpf_paciente": '123.456.789-09', "telefone_contato": '(11) 99999-1111', "tipo": "particular"})
    assert isinstance(obj.pk, uuid.UUID) and obj.pk.version == 4

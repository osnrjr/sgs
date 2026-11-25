"""Ligação Comanda.salao → Salao (sgs ligar): referência OPCIONAL entre classes de apps diferentes."""
import pytest

from apps.comandas.forms import ComandaForm
from apps.comandas.models import Comanda
from apps.comandas.tests.test_models import dados as dados_comandas
from apps.saloes.models import Salao
from apps.saloes.tests.test_models import dados as dados_saloes

pytestmark = pytest.mark.django_db


def test_o_campo_e_opcional_e_aponta_para_a_classe():
    campo = Comanda._meta.get_field("salao")
    assert campo.related_model is Salao and campo.null and campo.blank
    assert "salao" in ComandaForm().fields


def test_ligar_e_apagar_o_alvo_so_limpa_a_referencia():
    alvo = Salao.objects.create(**dados_saloes())
    obj = Comanda.objects.create(**dados_comandas(), salao=alvo)
    assert obj.salao == alvo and obj in alvo.comandas_salao.all()
    alvo.delete()
    obj.refresh_from_db()
    assert obj.salao is None


def test_a_api_le_e_grava_a_referencia(client, settings):
    import json

    from django.urls import reverse

    setattr(settings, "COMANDAS_API_CAMPOS", {})    # o padrão (o sgs api config pode ter ocultado)
    alvo = Salao.objects.create(**dados_saloes())
    obj = Comanda.objects.create(**dados_comandas())
    url = reverse("comandas:api_item", args=[obj.pk])
    resposta = client.patch(url, data=json.dumps({"salao": str(alvo.pk)}), content_type="application/json")
    assert resposta.status_code == 200 and str(resposta.json()["salao"]) == str(alvo.pk)

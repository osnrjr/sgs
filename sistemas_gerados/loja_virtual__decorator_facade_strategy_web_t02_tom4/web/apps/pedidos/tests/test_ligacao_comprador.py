"""Ligação Pedido.comprador → Comprador (sgs ligar): referência OPCIONAL entre classes de apps diferentes."""
import pytest

from apps.pedidos.forms import PedidoForm
from apps.pedidos.models import Pedido
from apps.pedidos.tests.test_models import dados as dados_pedidos
from apps.compradores.models import Comprador
from apps.compradores.tests.test_models import dados as dados_compradores

pytestmark = pytest.mark.django_db


def test_o_campo_e_opcional_e_aponta_para_a_classe():
    campo = Pedido._meta.get_field("comprador")
    assert campo.related_model is Comprador and campo.null and campo.blank
    assert "comprador" in PedidoForm().fields


def test_ligar_e_apagar_o_alvo_so_limpa_a_referencia():
    alvo = Comprador.objects.create(**dados_compradores())
    obj = Pedido.objects.create(**dados_pedidos(), comprador=alvo)
    assert obj.comprador == alvo and obj in alvo.pedidos_comprador.all()
    alvo.delete()
    obj.refresh_from_db()
    assert obj.comprador is None


def test_a_api_le_e_grava_a_referencia(client, settings):
    import json

    from django.urls import reverse

    setattr(settings, "PEDIDOS_API_CAMPOS", {})    # o padrão (o sgs api config pode ter ocultado)
    alvo = Comprador.objects.create(**dados_compradores())
    obj = Pedido.objects.create(**dados_pedidos())
    url = reverse("pedidos:api_item", args=[obj.pk])
    resposta = client.patch(url, data=json.dumps({"comprador": str(alvo.pk)}), content_type="application/json")
    assert resposta.status_code == 200 and str(resposta.json()["comprador"]) == str(alvo.pk)

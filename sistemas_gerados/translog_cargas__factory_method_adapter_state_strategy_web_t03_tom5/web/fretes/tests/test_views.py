"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from fretes.models import Frete


def form_data(**mudancas):
    copia = {"cliente": "Elisa", "caminhao": "101", "toneladas": "2", "valor_tonelada": "280.00", "coordenadas": "-23.5505,-46.6333", "etiquetas": "fragil", "observacao": "", "tipo": "spot"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("fretes:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("fretes:criar"), form_data())
    assert resposta.status_code == 302
    assert Frete.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("fretes:criar"), form_data(toneladas="0"))
    assert resposta.status_code == 200
    assert Frete.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("fretes:criar"), form_data(tipo="contrato"))
    html = client.get(reverse("fretes:lista")).content.decode()
    assert "R$ 476.00" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("fretes:criar"), form_data())
    dados = client.get(reverse("fretes:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 560.00"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("fretes:criar"), form_data())
    return Frete.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("fretes:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.cliente) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("fretes:editar", args=[obj.pk]), form_data(toneladas="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.toneladas == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.toneladas
    resposta = client.post(reverse("fretes:editar", args=[obj.pk]), form_data(toneladas="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.toneladas == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("fretes:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert Frete.objects.count() == 1
    assert client.post(reverse("fretes:excluir", args=[obj.pk])).status_code == 302
    assert Frete.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("fretes:detalhe", "fretes:editar", "fretes:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

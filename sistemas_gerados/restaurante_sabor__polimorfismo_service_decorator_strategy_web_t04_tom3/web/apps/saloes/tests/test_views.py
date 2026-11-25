"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from apps.saloes.models import Salao


def form_data(**mudancas):
    copia = {"cliente": "Márcio", "mesa": "101", "pratos": "2", "preco_prato": "58.00", "observacao": "", "tipo": "comum"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("saloes:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("saloes:criar"), form_data())
    assert resposta.status_code == 302
    assert Salao.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("saloes:criar"), form_data(pratos="0"))
    assert resposta.status_code == 200
    assert Salao.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("saloes:criar"), form_data(tipo="fidelidade"))
    html = client.get(reverse("saloes:lista")).content.decode()
    assert "R$ 104.40" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("saloes:criar"), form_data())
    dados = client.get(reverse("saloes:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 116.00"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("saloes:criar"), form_data())
    return Salao.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("saloes:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.cliente) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("saloes:editar", args=[obj.pk]), form_data(pratos="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.pratos == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.pratos
    resposta = client.post(reverse("saloes:editar", args=[obj.pk]), form_data(pratos="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.pratos == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("saloes:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert Salao.objects.count() == 1
    assert client.post(reverse("saloes:excluir", args=[obj.pk])).status_code == 302
    assert Salao.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("saloes:detalhe", "saloes:editar", "saloes:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

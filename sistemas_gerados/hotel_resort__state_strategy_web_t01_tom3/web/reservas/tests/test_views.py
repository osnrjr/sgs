"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from reservas.models import Reserva


def form_data(**mudancas):
    copia = {"hospede": "Ana", "quarto": "101", "diarias": "2", "valor_diaria": "200.00", "agendado_em": "2026-01-10T09:30", "email_hospede": "contato@exemplo.com.br", "observacao": "", "tipo": "comum"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("reservas:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("reservas:criar"), form_data())
    assert resposta.status_code == 302
    assert Reserva.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("reservas:criar"), form_data(diarias="0"))
    assert resposta.status_code == 200
    assert Reserva.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("reservas:criar"), form_data(tipo="fidelidade"))
    html = client.get(reverse("reservas:lista")).content.decode()
    assert "R$ 360.00" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("reservas:criar"), form_data())
    dados = client.get(reverse("reservas:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 400.00"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("reservas:criar"), form_data())
    return Reserva.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("reservas:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.hospede) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("reservas:editar", args=[obj.pk]), form_data(diarias="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.diarias == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.diarias
    resposta = client.post(reverse("reservas:editar", args=[obj.pk]), form_data(diarias="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.diarias == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("reservas:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert Reserva.objects.count() == 1
    assert client.post(reverse("reservas:excluir", args=[obj.pk])).status_code == 302
    assert Reserva.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("reservas:detalhe", "reservas:editar", "reservas:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

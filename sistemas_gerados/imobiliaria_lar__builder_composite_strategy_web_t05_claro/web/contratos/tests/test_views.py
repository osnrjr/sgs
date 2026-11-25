"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from contratos.models import Contrato


def form_data(**mudancas):
    copia = {"locatario": "Danilo", "imovel": "101", "meses": "2", "valor_aluguel": "1800.00", "descricao_completa": "Descrição detalhada de descricao completa 1.", "foto_capa": "imagens/foto_1.png", "observacao": "", "tipo": "residencial"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("contratos:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("contratos:criar"), form_data())
    assert resposta.status_code == 302
    assert Contrato.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("contratos:criar"), form_data(meses="0"))
    assert resposta.status_code == 200
    assert Contrato.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("contratos:criar"), form_data(tipo="comercial"))
    html = client.get(reverse("contratos:lista")).content.decode()
    assert "R$ 4320.00" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("contratos:criar"), form_data())
    dados = client.get(reverse("contratos:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 3600.00"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("contratos:criar"), form_data())
    return Contrato.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("contratos:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.locatario) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("contratos:editar", args=[obj.pk]), form_data(meses="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.meses == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.meses
    resposta = client.post(reverse("contratos:editar", args=[obj.pk]), form_data(meses="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.meses == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("contratos:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert Contrato.objects.count() == 1
    assert client.post(reverse("contratos:excluir", args=[obj.pk])).status_code == 302
    assert Contrato.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("contratos:detalhe", "contratos:editar", "contratos:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

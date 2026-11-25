"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from turmas.models import Turma


def form_data(**mudancas):
    copia = {"aluno": "Márcio", "sala": "101", "meses": "2", "mensalidade": "850.00", "portal_url": "https://exemplo.com.br/item-1", "comprovante": "documentos/anexo_1.pdf", "observacao": "", "tipo": "regular"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("turmas:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("turmas:criar"), form_data())
    assert resposta.status_code == 302
    assert Turma.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("turmas:criar"), form_data(meses="0"))
    assert resposta.status_code == 200
    assert Turma.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("turmas:criar"), form_data(tipo="irmaos"))
    html = client.get(reverse("turmas:lista")).content.decode()
    assert "R$ 1530.00" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("turmas:criar"), form_data())
    dados = client.get(reverse("turmas:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 1700.00"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("turmas:criar"), form_data())
    return Turma.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("turmas:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.aluno) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("turmas:editar", args=[obj.pk]), form_data(meses="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.meses == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.meses
    resposta = client.post(reverse("turmas:editar", args=[obj.pk]), form_data(meses="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.meses == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("turmas:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert Turma.objects.count() == 1
    assert client.post(reverse("turmas:excluir", args=[obj.pk])).status_code == 302
    assert Turma.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("turmas:detalhe", "turmas:editar", "turmas:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

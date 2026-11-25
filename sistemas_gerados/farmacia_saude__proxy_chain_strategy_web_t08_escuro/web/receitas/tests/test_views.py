"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from receitas.models import Receita


def form_data(**mudancas):
    copia = {"cliente": "Ana", "balcao": "101", "unidades": "2", "preco_unitario": "25.90", "cnpj_fornecedor": "11.222.333/0001-81", "metadados": '{"chave": "metadados_1", "ativo": true}', "observacao": "", "tipo": "comum"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("receitas:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("receitas:criar"), form_data())
    assert resposta.status_code == 302
    assert Receita.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("receitas:criar"), form_data(unidades="0"))
    assert resposta.status_code == 200
    assert Receita.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("receitas:criar"), form_data(tipo="convenio"))
    html = client.get(reverse("receitas:lista")).content.decode()
    assert "R$ 44.03" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("receitas:criar"), form_data())
    dados = client.get(reverse("receitas:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 51.80"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("receitas:criar"), form_data())
    return Receita.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("receitas:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.cliente) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("receitas:editar", args=[obj.pk]), form_data(unidades="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.unidades == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.unidades
    resposta = client.post(reverse("receitas:editar", args=[obj.pk]), form_data(unidades="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.unidades == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("receitas:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert Receita.objects.count() == 1
    assert client.post(reverse("receitas:excluir", args=[obj.pk])).status_code == 302
    assert Receita.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("receitas:detalhe", "receitas:editar", "receitas:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

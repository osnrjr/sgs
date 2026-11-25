"""Testes das VIEWS (MVT): finas — delegam ao Service e ao ViewModel."""
import pytest
from django.urls import reverse

from parque_aerogeradores.models import ParqueAerogerador


def form_data(**mudancas):
    copia = {"operador": "Ana", "torre": "101", "megawatts": "2", "preco_mwh": "220.00", "geoloc": "-23.5505,-46.6333", "parametros_json": '{"chave": "parametros_json_1", "ativo": true}', "observacao": "", "tipo": "padrao"}
    copia.update(mudancas)
    return copia


@pytest.mark.django_db
def test_lista_vazia(client):
    resposta = client.get(reverse("parque_aerogeradores:lista"))
    assert resposta.status_code == 200
    assert "Nenhum registro ainda" in resposta.content.decode()


@pytest.mark.django_db
def test_criar_valido_salva_e_redireciona(client):
    resposta = client.post(reverse("parque_aerogeradores:criar"), form_data())
    assert resposta.status_code == 302
    assert ParqueAerogerador.objects.count() == 1


@pytest.mark.django_db
def test_criar_invalido_nao_salva(client):
    resposta = client.post(reverse("parque_aerogeradores:criar"), form_data(megawatts="0"))
    assert resposta.status_code == 200
    assert ParqueAerogerador.objects.count() == 0


@pytest.mark.django_db
def test_lista_mostra_o_valor_com_a_politica(client):
    client.post(reverse("parque_aerogeradores:criar"), form_data(tipo="corporativo"))
    html = client.get(reverse("parque_aerogeradores:lista")).content.decode()
    assert "R$ 396.00" in html


@pytest.mark.django_db
def test_api_devolve_json(client):
    client.post(reverse("parque_aerogeradores:criar"), form_data())
    dados = client.get(reverse("parque_aerogeradores:api")).json()
    assert len(dados["itens"]) == 1 and dados["total"] == "R$ 440.00"


# ---------------------------------------------------------------- CRUD: detalhe, editar e excluir
def criado(client):
    client.post(reverse("parque_aerogeradores:criar"), form_data())
    return ParqueAerogerador.objects.get()


@pytest.mark.django_db
def test_detalhe_mostra_o_registro(client):
    obj = criado(client)
    html = client.get(reverse("parque_aerogeradores:detalhe", args=[obj.pk])).content.decode()
    assert str(obj.operador) in html and "Valor final" in html


@pytest.mark.django_db
def test_editar_altera_o_registro(client):
    obj = criado(client)
    resposta = client.post(reverse("parque_aerogeradores:editar", args=[obj.pk]), form_data(megawatts="3"))
    assert resposta.status_code == 302
    obj.refresh_from_db()
    assert obj.megawatts == 3


@pytest.mark.django_db
def test_editar_invalido_nao_altera(client):
    obj = criado(client)
    antes = obj.megawatts
    resposta = client.post(reverse("parque_aerogeradores:editar", args=[obj.pk]), form_data(megawatts="0"))
    assert resposta.status_code == 200
    obj.refresh_from_db()
    assert obj.megawatts == antes


@pytest.mark.django_db
def test_excluir_so_com_post(client):
    obj = criado(client)
    assert client.get(reverse("parque_aerogeradores:excluir", args=[obj.pk])).status_code == 200   # GET só confirma
    assert ParqueAerogerador.objects.count() == 1
    assert client.post(reverse("parque_aerogeradores:excluir", args=[obj.pk])).status_code == 302
    assert ParqueAerogerador.objects.count() == 0


@pytest.mark.django_db
def test_registro_inexistente_da_404(client):
    obj = criado(client)
    pk = obj.pk
    obj.delete()
    for rota in ("parque_aerogeradores:detalhe", "parque_aerogeradores:editar", "parque_aerogeradores:excluir"):
        assert client.get(reverse(rota, args=[pk])).status_code == 404

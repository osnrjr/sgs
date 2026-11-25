"""Testes da API REST: o mesmo ModelForm valida as telas e a API; o settings da app manda nos limites."""
import json

import pytest
from django.test import Client, override_settings
from django.urls import reverse

from turmas.models import Turma

pytestmark = pytest.mark.django_db
VALIDO = {"aluno": "Márcio", "sala": 101, "meses": 2, "mensalidade": "850.00", "portal_url": "https://exemplo.com.br/item-1", "comprovante": "documentos/anexo_1.pdf", "observacao": "", "tipo": "regular"}


@pytest.fixture(autouse=True)
def api_no_padrao(settings):
    """Estes testes conferem o PADRÃO: o que o projeto escolheu no sgs api config não muda o resultado deles."""
    settings.TURMAS_API_CAMPOS = {}


def enviar(client, metodo, url, dados):
    return getattr(client, metodo)(url, data=json.dumps(dados), content_type="application/json")


def colecao():
    return reverse("turmas:api_colecao")


def test_post_cria_e_get_lista(client):
    resposta = enviar(client, "post", colecao(), VALIDO)
    assert resposta.status_code == 201
    criado = resposta.json()
    assert criado["aluno"] == VALIDO["aluno"] and "total" in criado and "valor_final" in criado
    lista = client.get(colecao()).json()
    assert lista["total_registros"] == 1 and lista["itens"][0]["id"] == criado["id"]


def test_post_invalido_devolve_400_com_os_erros(client):
    resposta = enviar(client, "post", colecao(), {**VALIDO, "meses": 0})
    assert resposta.status_code == 400 and "meses" in resposta.json()["erros"]
    assert Turma.objects.count() == 0


def test_get_put_patch_delete_de_um_registro(client):
    criado = enviar(client, "post", colecao(), VALIDO).json()
    url = reverse("turmas:api_item", args=[criado["id"]])
    assert client.get(url).json()["id"] == criado["id"]
    parcial = enviar(client, "patch", url, {"meses": 2})           # PATCH: só o campo enviado muda
    assert parcial.status_code == 200 and parcial.json()["meses"] == 2
    assert parcial.json()["aluno"] == VALIDO["aluno"]
    inteiro = enviar(client, "put", url, {**VALIDO, "meses": 3})   # PUT: o registro inteiro
    assert inteiro.status_code == 200 and inteiro.json()["meses"] == 3
    assert enviar(client, "put", url, {**VALIDO, "meses": 0}).status_code == 400
    assert client.delete(url).status_code == 204
    assert client.get(url).status_code == 404


def test_metodo_nao_permitido_e_json_invalido(client):
    assert client.delete(colecao()).status_code == 405
    assert client.post(colecao(), data="{isto não é json", content_type="application/json").status_code == 400


def test_api_so_leitura_pelo_settings_da_app(client):
    with override_settings(TURMAS_API_ESCRITA=False):
        assert enviar(client, "post", colecao(), VALIDO).status_code == 405
        assert client.get(colecao()).status_code == 200


def test_limite_da_lista_vem_do_settings_da_app(client):
    for _ in range(3):
        enviar(client, "post", colecao(), VALIDO)
    with override_settings(TURMAS_API_LIMITE=2):
        dados = client.get(colecao()).json()
    assert len(dados["itens"]) == 2 and dados["total_registros"] == 3
    assert len(client.get(colecao(), {"limite": 1}).json()["itens"]) == 1


def test_csrf_continua_valendo_na_api():
    """Sem o token CSRF, escrever é recusado (403): a API não abre uma porta nos fundos."""
    assert enviar(Client(enforce_csrf_checks=True), "post", colecao(), VALIDO).status_code == 403


# ---------------------------------------------------------------- campos de cada endpoint (sgs api config)
def test_campos_de_cada_endpoint_vem_do_settings(client):
    enviar(client, "post", colecao(), VALIDO)
    padrao = client.get(colecao()).json()["itens"][0]
    assert "aluno" in padrao and "valor_final" in padrao and "titulo" not in padrao
    resumo = client.get(reverse("turmas:api")).json()["itens"][0]
    assert set(resumo) == {"id", "codigo", "titulo", "valor"}           # o resumo do painel (link "API")
    escolha = {"v1": {"aluno": False, "titulo": True}, "resumo": {"meses": True, "codigo": False}}
    with override_settings(TURMAS_API_CAMPOS=escolha):
        item = client.get(colecao()).json()["itens"][0]
        assert "aluno" not in item and "titulo" in item
        resumo = client.get(reverse("turmas:api")).json()["itens"][0]
        assert resumo["meses"] == VALIDO["meses"] and "codigo" not in resumo
        campos = client.get(reverse("turmas:api_campos")).json()
        assert "aluno" in campos["disponiveis"] and "aluno" not in campos["expostos"]["v1"]


def test_quem_chama_escolhe_entre_os_campos_expostos(client):
    criado = enviar(client, "post", colecao(), VALIDO).json()
    item = client.get(colecao(), {"campos": "aluno,total"}).json()["itens"][0]
    assert set(item) == {"aluno", "total"}
    um = client.get(reverse("turmas:api_item", args=[criado["id"]]), {"campos": "id"}).json()
    assert um == {"id": criado["id"]}
    with override_settings(TURMAS_API_CAMPOS={"v1": {"total": False}}):   # oculto não volta nem pedindo
        assert set(client.get(colecao(), {"campos": "aluno,total"}).json()["itens"][0]) == {"aluno"}

"""
MODEL (o "M" do MVT). Encapsulamento no MUNDO DJANGO (Aula 03):
  * a regra de cada campo vai em validators — o ModelForm, o admin e o full_clean() as executam;
  * @property aqui só para dado CALCULADO (total); setter em campo quebraria form/admin/ORM;
  * pegadinha: save() sozinho NÃO valida (ver tests/test_models.py).
"""
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Salao(models.Model):
    TIPOS = [
        ("comum", "Comum"),
        ("fidelidade", "Fidelidade"),
        ("empresa", "Empresa"),
        ("aniversariante", "Aniversariante")
    ]


    cliente = models.CharField("cliente", max_length=120)  # obrigatório: blank=False é o padrão
    mesa = models.IntegerField("mesa", validators=[MinValueValidator(1)])
    pratos = models.IntegerField("pratos", validators=[MinValueValidator(1), MaxValueValidator(20)])
    preco_prato = models.DecimalField("preco prato", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    observacao = models.CharField("observacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de cliente", max_length=30, choices=TIPOS, default="comum")

    @property
    def total(self):
        """Dado CALCULADO (pratos × preco_prato): nunca guardado, nunca desatualizado."""
        return self.pratos * self.preco_prato



    def __str__(self):
        return f"{self.cliente} - {self.pratos} prato(s)"

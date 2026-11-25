"""
MODEL (o "M" do MVT). Encapsulamento no MUNDO DJANGO (Aula 03):
  * a regra de cada campo vai em validators — o ModelForm, o admin e o full_clean() as executam;
  * @property aqui só para dado CALCULADO (total); setter em campo quebraria form/admin/ORM;
  * pegadinha: save() sozinho NÃO valida (ver tests/test_models.py).
"""
import uuid
import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

def validar_telefone(valor):
    """Validator: exige telefone com 10 ou 11 dígitos."""
    if len(re.sub(r"\D", "", str(valor))) not in (10, 11):
        raise ValidationError("Informe um telefone válido com 10 ou 11 dígitos.")

def validar_cpf(valor):
    """Validator: valida CPF com 11 dígitos e dígitos verificadores."""
    dig = re.sub(r"\D", "", str(valor))
    if len(dig) != 11 or len(set(dig)) == 1:
        raise ValidationError("CPF inválido.")
    nums = [int(d) for d in dig]
    dv1 = (sum(nums[i] * (10 - i) for i in range(9)) * 10 % 11) % 10
    dv2 = (sum(nums[i] * (11 - i) for i in range(10)) * 10 % 11) % 10
    if nums[9] != dv1 or nums[10] != dv2:
        raise ValidationError("CPF com dígitos verificadores inválidos.")
class Consulta(models.Model):
    TIPOS = [
        ("particular", "Particular"),
        ("convenio_ouro", "ConvenioOuro"),
        ("convenio_prata", "ConvenioPrata"),
        ("empresa", "Empresa")
    ]

    # Instruções §10.4: chave UUIDv4 — o próximo registro não dá para adivinhar (anti-enumeração).
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.CharField("paciente", max_length=120)  # obrigatório: blank=False é o padrão
    sala = models.IntegerField("sala", validators=[MinValueValidator(1)])
    sessoes = models.IntegerField("sessoes", validators=[MinValueValidator(1), MaxValueValidator(12)])
    valor_sessao = models.DecimalField("valor sessao", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    cpf_paciente = models.CharField("cpf paciente", max_length=14, validators=[validar_cpf], default='123.456.789-09')  # CPF com dígitos verificadores
    telefone_contato = models.CharField("telefone contato", max_length=20, validators=[validar_telefone], default='(11) 99999-1111')  # telefone com 10 ou 11 dígitos
    anotacao = models.CharField("anotacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de convênio", max_length=30, choices=TIPOS, default="particular")

    @property
    def total(self):
        """Dado CALCULADO (sessoes × valor_sessao): nunca guardado, nunca desatualizado."""
        return self.sessoes * self.valor_sessao



    def __str__(self):
        return f"{self.paciente} - {self.sessoes} sessão(ões)"

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
from django.db import IntegrityError, models, transaction

from . import lnnl

def validar_cnpj(valor):
    """Validator: valida CNPJ com 14 dígitos e dígitos verificadores."""
    dig = re.sub(r"\D", "", str(valor))
    if len(dig) != 14 or len(set(dig)) == 1:
        raise ValidationError("CNPJ inválido.")
    nums = [int(d) for d in dig]
    r1 = sum(nums[i] * p for i, p in enumerate((5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))) % 11
    dv1 = 0 if r1 < 2 else 11 - r1
    r2 = sum(nums[i] * p for i, p in enumerate((6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))) % 11
    dv2 = 0 if r2 < 2 else 11 - r2
    if nums[12] != dv1 or nums[13] != dv2:
        raise ValidationError("CNPJ com dígitos verificadores inválidos.")

# ID interno LNNL (motor-id-interno): legível por pessoas, NÃO substitui a chave primária.
TIPO_LNNL = "32"  # código de tipo desta entidade (11–99, sem zero; 93 é reservado)


def validar_codigo_lnnl(valor):
    """Validator: só aceita um LNNL válido do tipo desta entidade (verificadores módulo 79)."""
    resultado = lnnl.validar(valor, TIPO_LNNL)
    if not resultado:
        raise ValidationError(f"código LNNL inválido: {resultado.erro}")
class Receita(models.Model):
    TIPOS = [
        ("comum", "Comum"),
        ("convenio", "Convênio"),
        ("idoso", "Idoso"),
        ("farmacia_popular", "Farmácia Popular")
    ]

    # Instruções §10.4: chave UUIDv4 — o próximo registro não dá para adivinhar (anti-enumeração).
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_interno = models.CharField("ID interno", max_length=14, unique=True, editable=False, blank=True, validators=[validar_codigo_lnnl])
    cliente = models.CharField("cliente", max_length=120)  # obrigatório: blank=False é o padrão
    balcao = models.IntegerField("balcao", validators=[MinValueValidator(1)])
    unidades = models.IntegerField("unidades", validators=[MinValueValidator(1), MaxValueValidator(20)])
    preco_unitario = models.DecimalField("preco unitario", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    cnpj_fornecedor = models.CharField("cnpj fornecedor", max_length=18, validators=[validar_cnpj], default='11.222.333/0001-81')  # CNPJ com dígitos verificadores
    metadados = models.JSONField("metadados", default=dict)  # objeto ou lista JSON dinâmica
    observacao = models.CharField("observacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de cliente", max_length=30, choices=TIPOS, default="comum")

    @property
    def total(self):
        """Dado CALCULADO (unidades × preco_unitario): nunca guardado, nunca desatualizado."""
        return self.unidades * self.preco_unitario

    @property
    def id_interno_formatado(self):
        """O ID interno na máscara de exibição LNNL-LNNL-LNL-LNL (ex.: K21W-F92M-T5R-Q7L)."""
        return lnnl.formatar(self.id_interno)

    def save(self, *args, **kwargs):
        """Gera o ID interno na primeira gravação. Regra do motor: sorteia, INSERE e, se colidir
        (UNIQUE), tenta de novo — nunca "consulta antes e insere depois"."""
        if self.id_interno:
            return super().save(*args, **kwargs)
        for _ in range(5):
            self.id_interno = lnnl.gerar(TIPO_LNNL)
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.id_interno = ""
        raise IntegrityError("não foi possível gerar um ID interno LNNL único")

    def __str__(self):
        return f"{self.cliente} - {self.unidades} unidade(s)"

"""
MODEL (o "M" do MVT). Encapsulamento no MUNDO DJANGO (Aula 03):
  * a regra de cada campo vai em validators — o ModelForm, o admin e o full_clean() as executam;
  * @property aqui só para dado CALCULADO (total); setter em campo quebraria form/admin/ORM;
  * pegadinha: save() sozinho NÃO valida (ver tests/test_models.py).
"""
import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

def validar_arquivo(valor):
    """Validator: valida caminho ou URL de arquivo com extensão."""
    if not re.fullmatch(r"(?:https?://[^\s]+|[\w./-]+)\.[A-Za-z0-9]{2,6}", str(valor).strip()):
        raise ValidationError("Informe um caminho ou URL de arquivo com extensão (ex.: anexo.pdf).")
class Turma(models.Model):
    TIPOS = [
        ("regular", "Regular"),
        ("irmaos", "Irmãos"),
        ("bolsista", "Bolsista"),
        ("filho_de_professor", "Filho de Professor")
    ]


    aluno = models.CharField("aluno", max_length=120)  # obrigatório: blank=False é o padrão
    sala = models.IntegerField("sala", validators=[MinValueValidator(1)])
    meses = models.IntegerField("meses", validators=[MinValueValidator(1), MaxValueValidator(12)])
    mensalidade = models.DecimalField("mensalidade", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    portal_url = models.URLField("portal url", max_length=250, default='https://exemplo.com.br/item-1')  # URL validada
    comprovante = models.CharField("comprovante", max_length=255, validators=[validar_arquivo], default='documentos/anexo_1.pdf')  # caminho ou URL de arquivo/anexo
    observacao = models.CharField("observacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de bolsa", max_length=30, choices=TIPOS, default="regular")

    @property
    def total(self):
        """Dado CALCULADO (meses × mensalidade): nunca guardado, nunca desatualizado."""
        return self.meses * self.mensalidade



    def __str__(self):
        return f"{self.aluno} - {self.meses} mês(es)"

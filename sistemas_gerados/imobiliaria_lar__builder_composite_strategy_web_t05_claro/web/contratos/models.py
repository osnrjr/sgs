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

def validar_imagem(valor):
    """Validator: valida caminho ou URL de imagem (.png, .jpg, .webp, .gif, .svg)."""
    if not re.fullmatch(r"(?:https?://[^\s]+|[\w./-]+)\.(?:png|jpe?g|webp|gif|svg)", str(valor).strip(), re.IGNORECASE):
        raise ValidationError("Informe um caminho ou URL de imagem válida (.png, .jpg, .webp, .gif, .svg).")
class Contrato(models.Model):
    TIPOS = [
        ("residencial", "Residencial"),
        ("comercial", "Comercial"),
        ("estudante", "Estudante"),
        ("corporativo", "Corporativo")
    ]


    locatario = models.CharField("locatario", max_length=120)  # obrigatório: blank=False é o padrão
    imovel = models.IntegerField("imovel", validators=[MinValueValidator(1)])
    meses = models.IntegerField("meses", validators=[MinValueValidator(1), MaxValueValidator(36)])
    valor_aluguel = models.DecimalField("valor aluguel", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    descricao_completa = models.TextField("descricao completa", default='')  # texto longo obrigatório
    foto_capa = models.CharField("foto capa", max_length=255, validators=[validar_imagem], default='imagens/foto_1.png')  # caminho ou URL de imagem
    observacao = models.CharField("observacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de cliente", max_length=30, choices=TIPOS, default="residencial")

    @property
    def total(self):
        """Dado CALCULADO (meses × valor_aluguel): nunca guardado, nunca desatualizado."""
        return self.meses * self.valor_aluguel



    def __str__(self):
        return f"{self.locatario} - {self.meses} mês(es)"

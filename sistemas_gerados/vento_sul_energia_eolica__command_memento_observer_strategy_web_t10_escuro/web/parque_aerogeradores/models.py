"""
MODEL (o "M" do MVT). Encapsulamento no MUNDO DJANGO (Aula 03):
  * a regra de cada campo vai em validators — o ModelForm, o admin e o full_clean() as executam;
  * @property aqui só para dado CALCULADO (total); setter em campo quebraria form/admin/ORM;
  * pegadinha: save() sozinho NÃO valida (ver tests/test_models.py).
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

def validar_geolocalizacao(valor):
    """Validator: valida coordenadas latitude,longitude (-90..90, -180..180)."""
    partes = [p.strip() for p in str(valor).split(",")]
    try:
        lat, lng = (float(partes[0]), float(partes[1])) if len(partes) == 2 else (999.0, 999.0)
    except ValueError:
        lat, lng = 999.0, 999.0
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
        raise ValidationError("Informe coordenadas válidas: latitude,longitude (-90..90, -180..180).")
class ParqueAerogerador(models.Model):
    TIPOS = [
        ("padrao", "Padrao"),
        ("corporativo", "Corporativo"),
        ("recorrente", "Recorrente"),
        ("emergencial", "Emergencial")
    ]


    operador = models.CharField("operador", max_length=120)  # obrigatório: blank=False é o padrão
    torre = models.IntegerField("torre", validators=[MinValueValidator(1)])
    megawatts = models.IntegerField("megawatts", validators=[MinValueValidator(1), MaxValueValidator(50)])
    preco_mwh = models.DecimalField("preco mwh", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    geoloc = models.CharField("geoloc", max_length=50, validators=[validar_geolocalizacao], default='-23.5505,-46.6333')  # coordenadas latitude,longitude
    parametros_json = models.JSONField("parametros json", default=dict)  # objeto ou lista JSON dinâmica
    observacao = models.CharField("observacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de contrato", max_length=30, choices=TIPOS, default="padrao")

    @property
    def total(self):
        """Dado CALCULADO (megawatts × preco_mwh): nunca guardado, nunca desatualizado."""
        return self.megawatts * self.preco_mwh



    def __str__(self):
        return f"{self.operador} - {self.megawatts} MW"

"""
MODEL (o "M" do MVT). Encapsulamento no MUNDO DJANGO (Aula 03):
  * a regra de cada campo vai em validators — o ModelForm, o admin e o full_clean() as executam;
  * @property aqui só para dado CALCULADO (total); setter em campo quebraria form/admin/ORM;
  * pegadinha: save() sozinho NÃO valida (ver tests/test_models.py).
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models, transaction

from . import lnnl

def validar_geolocalizacao(valor):
    """Validator: valida coordenadas latitude,longitude (-90..90, -180..180)."""
    partes = [p.strip() for p in str(valor).split(",")]
    try:
        lat, lng = (float(partes[0]), float(partes[1])) if len(partes) == 2 else (999.0, 999.0)
    except ValueError:
        lat, lng = 999.0, 999.0
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
        raise ValidationError("Informe coordenadas válidas: latitude,longitude (-90..90, -180..180).")

def validar_multipla_etiquetas(valor):
    """Validator: múltipla escolha entre as opções permitidas."""
    itens = [p.strip() for p in str(valor).split(",") if p.strip()]
    permitidas = {'fragil', 'urgente', 'refrigerado'}
    if not itens or len(set(itens)) != len(itens) or any(p not in permitidas for p in itens):
        raise ValidationError("Escolha uma ou mais opções válidas separadas por vírgula.")

# ID interno LNNL (motor-id-interno): legível por pessoas, NÃO substitui a chave primária.
TIPO_LNNL = "24"  # código de tipo desta entidade (11–99, sem zero; 93 é reservado)


def validar_codigo_lnnl(valor):
    """Validator: só aceita um LNNL válido do tipo desta entidade (verificadores módulo 79)."""
    resultado = lnnl.validar(valor, TIPO_LNNL)
    if not resultado:
        raise ValidationError(f"código LNNL inválido: {resultado.erro}")
class Frete(models.Model):
    TIPOS = [
        ("spot", "Spot"),
        ("contrato", "Contrato"),
        ("industria", "Indústria"),
        ("retorno", "Retorno")
    ]

    id_interno = models.CharField("ID interno", max_length=14, unique=True, editable=False, blank=True, validators=[validar_codigo_lnnl])
    cliente = models.CharField("cliente", max_length=120)  # obrigatório: blank=False é o padrão
    caminhao = models.IntegerField("caminhao", validators=[MinValueValidator(1)])
    toneladas = models.IntegerField("toneladas", validators=[MinValueValidator(1), MaxValueValidator(40)])
    valor_tonelada = models.DecimalField("valor tonelada", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    coordenadas = models.CharField("coordenadas", max_length=50, validators=[validar_geolocalizacao], default='-23.5505,-46.6333')  # coordenadas latitude,longitude
    etiquetas = models.CharField("etiquetas", max_length=250, validators=[validar_multipla_etiquetas], default='fragil')  # múltipla escolha (valores separados por vírgula)
    observacao = models.CharField("observacao", max_length=200, blank=True, default="")  # sem regra
    tipo = models.CharField("tipo de cliente", max_length=30, choices=TIPOS, default="spot")

    @property
    def total(self):
        """Dado CALCULADO (toneladas × valor_tonelada): nunca guardado, nunca desatualizado."""
        return self.toneladas * self.valor_tonelada

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
        return f"{self.cliente} - {self.toneladas} tonelada(s)"

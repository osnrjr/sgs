"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import Contrato


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ["locatario", "imovel", "meses", "valor_aluguel", "descricao_completa", "foto_capa", "observacao", "tipo"]
        widgets = {"descricao_completa": forms.Textarea(attrs={"rows": 5, "data-editor": "tinymce", "class": "tinymce"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

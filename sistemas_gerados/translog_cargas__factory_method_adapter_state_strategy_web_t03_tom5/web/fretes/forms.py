"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import Frete


class FreteForm(forms.ModelForm):
    class Meta:
        model = Frete
        fields = ["cliente", "caminhao", "toneladas", "valor_tonelada", "coordenadas", "etiquetas", "observacao", "tipo"]
        widgets = {"coordenadas": forms.TextInput(attrs={"placeholder": "-23.5505,-46.6333"}), "etiquetas": forms.TextInput(attrs={"placeholder": "fragil,urgente,refrigerado"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

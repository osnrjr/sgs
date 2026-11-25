"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import ParqueAerogerador


class ParqueAerogeradorForm(forms.ModelForm):
    class Meta:
        model = ParqueAerogerador
        fields = ["operador", "torre", "megawatts", "preco_mwh", "geoloc", "parametros_json", "observacao", "tipo"]
        widgets = {"geoloc": forms.TextInput(attrs={"placeholder": "-23.5505,-46.6333"}), "parametros_json": forms.Textarea(attrs={"rows": 3, "placeholder": '{"chave": "valor"}'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

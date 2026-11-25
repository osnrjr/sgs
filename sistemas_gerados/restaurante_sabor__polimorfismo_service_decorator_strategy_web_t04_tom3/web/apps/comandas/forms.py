"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import Comanda


class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ["cliente", "mesa", "pratos", "preco_prato", "horario_pedido", "observacao", "salao", "tipo"]
        widgets = {"horario_pedido": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

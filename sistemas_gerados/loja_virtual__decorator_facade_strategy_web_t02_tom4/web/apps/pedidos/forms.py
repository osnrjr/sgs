"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["cliente", "produto", "quantidade", "preco_unitario", "frete", "cep_entrega", "observacao", "comprador", "tipo"]
        widgets = {"frete": forms.NumberInput(attrs={"step": "0.01", "min": "0"}), "cep_entrega": forms.TextInput(attrs={"placeholder": "00000-000"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import Receita


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ["cliente", "balcao", "unidades", "preco_unitario", "cnpj_fornecedor", "metadados", "observacao", "tipo"]
        widgets = {"cnpj_fornecedor": forms.TextInput(attrs={"placeholder": "00.000.000/0001-00"}), "metadados": forms.Textarea(attrs={"rows": 3, "placeholder": '{"chave": "valor"}'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

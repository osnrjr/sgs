"""ModelForm: reaproveita os validators do model (a regra mora num lugar só)."""
from django import forms

from .models import Consulta


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["paciente", "sala", "sessoes", "valor_sessao", "cpf_paciente", "telefone_contato", "anotacao", "tipo"]
        widgets = {"cpf_paciente": forms.TextInput(attrs={"placeholder": "000.000.000-00"}), "telefone_contato": forms.TextInput(attrs={"type": "tel", "placeholder": "(11) 99999-8888"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap: cada campo ganha a classe do componente (o HTML continua vindo do Django).
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-select" if isinstance(campo.widget, forms.Select) else "form-control"

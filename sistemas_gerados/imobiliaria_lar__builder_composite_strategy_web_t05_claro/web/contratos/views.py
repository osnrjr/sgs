"""
VIEWS (o "V" do MVT = a lógica/orquestração; o "Controller" do MVC). FINAS:
buscam os dados, delegam a regra ao Service e a exibição ao ViewModel, e renderizam.
"""
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContratoForm
from .models import Contrato
from .services import ContratoService
from .viewmodels import DetalheVM, PainelVM


def lista(request):
    painel = PainelVM(Contrato.objects.order_by("pk"), ContratoService())
    return render(request, "contratos/lista.html", {"painel": painel})


def criar(request):
    """CRUD · CREATE."""
    form = ContratoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():  # is_valid() executa os validators do model
        form.save()
        return redirect("contratos:lista")
    return render(request, "contratos/form.html", {"form": form})


def detalhe(request, pk):
    """CRUD · READ (um registro): o DetalheVM prepara o que a tela mostra."""
    obj = get_object_or_404(Contrato, pk=pk)
    return render(request, "contratos/detalhe.html", {"item": DetalheVM(obj, ContratoService().valor_final(obj))})


def editar(request, pk):
    """CRUD · UPDATE: o MESMO ModelForm, preenchido com o registro (as validações continuam valendo)."""
    obj = get_object_or_404(Contrato, pk=pk)
    form = ContratoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("contratos:detalhe", pk=obj.pk)
    return render(request, "contratos/form.html", {"form": form, "obj": obj})


def excluir(request, pk):
    """CRUD · DELETE: o GET só mostra a confirmação; apagar exige POST (GET nunca altera dados)."""
    obj = get_object_or_404(Contrato, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("contratos:lista")
    return render(request, "contratos/confirmar_exclusao.html", {"obj": obj})

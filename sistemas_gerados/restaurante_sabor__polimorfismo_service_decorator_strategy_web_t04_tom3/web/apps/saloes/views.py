"""
VIEWS (o "V" do MVT = a lógica/orquestração; o "Controller" do MVC). FINAS:
buscam os dados, delegam a regra ao Service e a exibição ao ViewModel, e renderizam.
"""
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SalaoForm
from .models import Salao
from .services import SalaoService
from .viewmodels import DetalheVM, PainelVM


def lista(request):
    painel = PainelVM(Salao.objects.order_by("pk"), SalaoService())
    return render(request, "saloes/lista.html", {"painel": painel})


def criar(request):
    """CRUD · CREATE."""
    form = SalaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():  # is_valid() executa os validators do model
        form.save()
        return redirect("saloes:lista")
    return render(request, "saloes/form.html", {"form": form})


def detalhe(request, pk):
    """CRUD · READ (um registro): o DetalheVM prepara o que a tela mostra."""
    obj = get_object_or_404(Salao, pk=pk)
    return render(request, "saloes/detalhe.html", {"item": DetalheVM(obj, SalaoService().valor_final(obj))})


def editar(request, pk):
    """CRUD · UPDATE: o MESMO ModelForm, preenchido com o registro (as validações continuam valendo)."""
    obj = get_object_or_404(Salao, pk=pk)
    form = SalaoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("saloes:detalhe", pk=obj.pk)
    return render(request, "saloes/form.html", {"form": form, "obj": obj})


def excluir(request, pk):
    """CRUD · DELETE: o GET só mostra a confirmação; apagar exige POST (GET nunca altera dados)."""
    obj = get_object_or_404(Salao, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("saloes:lista")
    return render(request, "saloes/confirmar_exclusao.html", {"obj": obj})

"""
VIEWS (o "V" do MVT = a lógica/orquestração; o "Controller" do MVC). FINAS:
buscam os dados, delegam a regra ao Service e a exibição ao ViewModel, e renderizam.
"""
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReceitaForm
from .models import Receita
from .services import ReceitaService
from .viewmodels import DetalheVM, PainelVM


def lista(request):
    painel = PainelVM(Receita.objects.order_by("pk"), ReceitaService())
    return render(request, "receitas/lista.html", {"painel": painel})


def criar(request):
    """CRUD · CREATE."""
    form = ReceitaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():  # is_valid() executa os validators do model
        form.save()
        return redirect("receitas:lista")
    return render(request, "receitas/form.html", {"form": form})


def detalhe(request, pk):
    """CRUD · READ (um registro): o DetalheVM prepara o que a tela mostra."""
    obj = get_object_or_404(Receita, pk=pk)
    return render(request, "receitas/detalhe.html", {"item": DetalheVM(obj, ReceitaService().valor_final(obj))})


def editar(request, pk):
    """CRUD · UPDATE: o MESMO ModelForm, preenchido com o registro (as validações continuam valendo)."""
    obj = get_object_or_404(Receita, pk=pk)
    form = ReceitaForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("receitas:detalhe", pk=obj.pk)
    return render(request, "receitas/form.html", {"form": form, "obj": obj})


def excluir(request, pk):
    """CRUD · DELETE: o GET só mostra a confirmação; apagar exige POST (GET nunca altera dados)."""
    obj = get_object_or_404(Receita, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("receitas:lista")
    return render(request, "receitas/confirmar_exclusao.html", {"obj": obj})

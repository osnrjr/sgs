"""
VIEWS (o "V" do MVT = a lógica/orquestração; o "Controller" do MVC). FINAS:
buscam os dados, delegam a regra ao Service e a exibição ao ViewModel, e renderizam.
"""
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ParqueAerogeradorForm
from .models import ParqueAerogerador
from .services import ParqueAerogeradorService
from .viewmodels import DetalheVM, PainelVM


def lista(request):
    painel = PainelVM(ParqueAerogerador.objects.order_by("pk"), ParqueAerogeradorService())
    return render(request, "parque_aerogeradores/lista.html", {"painel": painel})


def criar(request):
    """CRUD · CREATE."""
    form = ParqueAerogeradorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():  # is_valid() executa os validators do model
        form.save()
        return redirect("parque_aerogeradores:lista")
    return render(request, "parque_aerogeradores/form.html", {"form": form})


def detalhe(request, pk):
    """CRUD · READ (um registro): o DetalheVM prepara o que a tela mostra."""
    obj = get_object_or_404(ParqueAerogerador, pk=pk)
    return render(request, "parque_aerogeradores/detalhe.html", {"item": DetalheVM(obj, ParqueAerogeradorService().valor_final(obj))})


def editar(request, pk):
    """CRUD · UPDATE: o MESMO ModelForm, preenchido com o registro (as validações continuam valendo)."""
    obj = get_object_or_404(ParqueAerogerador, pk=pk)
    form = ParqueAerogeradorForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("parque_aerogeradores:detalhe", pk=obj.pk)
    return render(request, "parque_aerogeradores/form.html", {"form": form, "obj": obj})


def excluir(request, pk):
    """CRUD · DELETE: o GET só mostra a confirmação; apagar exige POST (GET nunca altera dados)."""
    obj = get_object_or_404(ParqueAerogerador, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("parque_aerogeradores:lista")
    return render(request, "parque_aerogeradores/confirmar_exclusao.html", {"obj": obj})

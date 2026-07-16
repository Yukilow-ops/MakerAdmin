from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Equipamento
from .forms import ReservaForm

@login_required
def lista_equipamentos(request): 
    equipamentos = Equipamento.objects.all()
    return render(request, 'controle/lista.html', {'equipamentos': equipamentos})

@login_required
def home(request):
    return render(request, 'controle/home.html')

@login_required
def fazer_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return redirect('home')
    else:
        form = ReservaForm()
    return render(request, 'controle/fazer_reserva.html', {'form': form})

from django.shortcuts import render, redirect
from .models import StockMovement
from .forms import StockMovementForm

def mouvement_list(request):
    mouvements = StockMovement.objects.all()
    return render(request, 'stocks/mouvement_list.html', {'mouvements': mouvements})

def mouvement_create(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mouvement_list')
    else:
        form = StockMovementForm()
    return render(request, 'stocks/mouvement_form.html', {'form': form})

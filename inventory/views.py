from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StockMovement


@login_required
def stock_movement_list(request):
    """
    Display a list of all stock movements.
    """
    movements = StockMovement.objects.all()
    return render(request, "inventory/stock_movement_log_list.html", {"movements": movements})

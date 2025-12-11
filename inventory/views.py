from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import StockMovement


@login_required
def stock_movement_list(request):
    """
    Display a list of all stock movements.
    """
    movements = StockMovement.objects.all()
    paginator = Paginator(movements, 10)  # Show 10 movements per page
    page_number = request.GET.get('page')
    movements = paginator.get_page(page_number)
    return render(request, "inventory/stock_movement_log_list.html", {"movements": movements})

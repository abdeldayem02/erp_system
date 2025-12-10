from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from customers.models import Customer
from orders.models import SalesOrder
from products.models import Product


@login_required
def home(request):
    context = {
        'total_customers': Customer.objects.count(),
        'total_orders_today': SalesOrder.objects.filter(
            order_date=timezone.now().date()
        ).count(),
        'low_stock_products': Product.objects.filter(
            stock_quantity__lt=10
        ).count(),
    }
    return render(request, 'home.html', context)

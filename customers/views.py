from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer



@login_required
def customer_list(request):
    """
    Display a list of all customers.
    """
    customers = Customer.objects.all()
    return render(request, "customers/customer_list.html", {"customers": customers})

@login_required
def customer_detail(request, pk):
    """
    Display details of a specific customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customers/customer_detail.html", {"customer": customer})

@login_required
def customer_create(request):
    """
    Create a new customer.
    """
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        email = request.POST.get("email")
        opening_balance = request.POST.get("opening_balance", 0.00)

        customer = Customer.objects.create(
            customer_id=customer_id,
            name=name,
            phone=phone,
            address=address,
            email=email,
            opening_balance=opening_balance,
        )
        return redirect("customer_detail", pk=customer.pk)

    return render(request, "customers/customer_form.html")

@admin_required
def customer_edit(request, pk):
    """
    Edit an existing customer.
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.customer_id = request.POST.get("customer_id")
        customer.name = request.POST.get("name")
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")
        customer.email = request.POST.get("email")
        customer.opening_balance = request.POST.get("opening_balance", 0.00)
        customer.save()
        return redirect("customer_detail", pk=customer.pk)

    return render(request, "customers/customer_form.html", {"customer": customer})

@admin_required
def customer_delete(request, pk):
    """
    Delete a customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect("customer_list")

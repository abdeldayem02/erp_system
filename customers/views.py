from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        try:
            customer_id = request.POST.get("customer_id", "").strip()
            name = request.POST.get("name", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            email = request.POST.get("email", "").strip()
            
            # Validate required fields
            if not all([customer_id, name, phone, address, email]):
                messages.error(request, "All fields are required")
                return redirect("customer_create")
            
            # Basic email validation
            if "@" not in email or "." not in email:
                messages.error(request, "Invalid email format")
                return redirect("customer_create")
            
            # Validate opening balance
            try:
                opening_balance = float(request.POST.get("opening_balance", 0.00))
            except (ValueError, TypeError):
                messages.error(request, "Invalid opening balance format")
                return redirect("customer_create")

            customer = Customer.objects.create(
                customer_id=customer_id,
                name=name,
                phone=phone,
                address=address,
                email=email,
                opening_balance=opening_balance,
            )
            messages.success(request, "Customer created successfully")
            return redirect("customer_detail", pk=customer.pk)
            
        except Exception as e:
            messages.error(request, f"Error creating customer: {str(e)}")
            return redirect("customer_create")

    return render(request, "customers/customer_form.html")

@admin_required
def customer_edit(request, pk):
    """
    Edit an existing customer, accessible only for admin-user.
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        try:
            customer_id = request.POST.get("customer_id", "").strip()
            name = request.POST.get("name", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            email = request.POST.get("email", "").strip()
            
            # Validate required fields
            if not all([customer_id, name, phone, address, email]):
                messages.error(request, "All fields are required")
                return redirect("customer_edit", pk=pk)
            
            # Basic email validation
            if "@" not in email or "." not in email:
                messages.error(request, "Invalid email format")
                return redirect("customer_edit", pk=pk)
            
            # Validate opening balance
            try:
                opening_balance = float(request.POST.get("opening_balance", 0.00))
            except (ValueError, TypeError):
                messages.error(request, "Invalid opening balance format")
                return redirect("customer_edit", pk=pk)
            
            customer.customer_id = customer_id
            customer.name = name
            customer.phone = phone
            customer.address = address
            customer.email = email
            customer.opening_balance = opening_balance
            customer.save()
            messages.success(request, "Customer updated successfully")
            return redirect("customer_detail", pk=customer.pk)
            
        except Exception as e:
            messages.error(request, f"Error updating customer: {str(e)}")
            return redirect("customer_edit", pk=pk)

    return render(request, "customers/customer_form.html", {"customer": customer})

@admin_required
def customer_delete(request, pk):
    """
    Delete a customer, , accessible only for admin-user.
    """
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect("customer_list")

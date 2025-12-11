from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from django.core.paginator import Paginator
from accounts.decorators import admin_required
from django.contrib import messages


@login_required
def product_list(request):
    """
    Display a list of all products.
    """
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, "products/product_list.html", {"products": products})


@login_required
def product_detail(request, pk):
    """
    Display details of a specific product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


@admin_required
def product_create(request):
    """
    Create a new product. Only accessible by admin users.
    """
    if request.method == "POST":
        try:
            sku = request.POST.get("sku", "").strip()
            name = request.POST.get("name", "").strip()
            category = request.POST.get("category", "").strip()
            
            # Validate required fields
            if not all([sku, name, category]):
                messages.error(request, "All fields are required")
                return redirect("product_create")
            
            # Validate and convert numeric fields
            try:
                cost_price = float(request.POST.get("cost_price"))
                selling_price = float(request.POST.get("selling_price"))
                stock_quantity = int(request.POST.get("stock_quantity"))
                
                if cost_price < 0 or selling_price < 0 or stock_quantity < 0:
                    messages.error(request, "Prices and quantity cannot be negative")
                    return redirect("product_create")
                    
            except (ValueError, TypeError):
                messages.error(request, "Invalid price or quantity format")
                return redirect("product_create")
            
            product = Product.objects.create(
                sku=sku,
                name=name,
                category=category,
                cost_price=cost_price,
                selling_price=selling_price,
                stock_quantity=stock_quantity,
            )
            messages.success(request, "Product created successfully")
            return redirect("product_detail", pk=product.pk)
            
        except Exception as e:
            messages.error(request, f"Error creating product: {str(e)}")
            return redirect("product_create")

    return render(request, "products/product_form.html")


@admin_required
def product_edit(request, pk):
    """
    Edit an existing product. Only accessible by admin users.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        try:
            sku = request.POST.get("sku", "").strip()
            name = request.POST.get("name", "").strip()
            category = request.POST.get("category", "").strip()
            
            # Validate required fields
            if not all([sku, name, category]):
                messages.error(request, "SKU, Name, and Category are required")
                return redirect("product_edit", pk=product.pk)
            
            # Validate and convert numeric fields
            try:
                cost_price = float(request.POST.get("cost_price"))
                selling_price = float(request.POST.get("selling_price"))
                stock_quantity = int(request.POST.get("stock_quantity"))
                
                if cost_price < 0 or selling_price < 0 or stock_quantity < 0:
                    messages.error(request, "Prices and quantity cannot be negative")
                    return redirect("product_edit", pk=product.pk)
                    
            except (ValueError, TypeError):
                messages.error(request, "Invalid price or quantity format")
                return redirect("product_edit", pk=product.pk)
            
            # Update product fields
            product.sku = sku
            product.name = name
            product.category = category
            product.cost_price = cost_price
            product.selling_price = selling_price
            product.stock_quantity = stock_quantity
            product.save()
            
            messages.success(request, "Product updated successfully")
            return redirect("product_detail", pk=product.pk)
        except Exception as e:
            messages.error(request, f"Error updating product: {str(e)}")
            return redirect("product_edit", pk=product.pk)
    return render(request, "products/product_form.html", {"product": product})


@admin_required
def product_delete(request, pk):
    """
    Delete a product. Only accessible by admin users.
    """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("product_list")

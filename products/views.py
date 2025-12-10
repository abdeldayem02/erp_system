from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from accounts.decorators import admin_required


def product_list(request):
    """
    Display a list of all products.
    """
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


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
        sku = request.POST.get("sku")
        name = request.POST.get("name")
        category = request.POST.get("category")
        cost_price = request.POST.get("cost_price")
        selling_price = request.POST.get("selling_price")
        stock_quantity = request.POST.get("stock_quantity")

        product = Product.objects.create(
            sku=sku,
            name=name,
            category=category,
            cost_price=cost_price,
            selling_price=selling_price,
            stock_quantity=stock_quantity,
        )
        return redirect("product_detail", pk=product.pk)

    return render(request, "products/product_form.html")


@admin_required
def product_edit(request, pk):
    """
    Edit an existing product. Only accessible by admin users.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.sku = request.POST.get("sku")
        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.cost_price = request.POST.get("cost_price")
        product.selling_price = request.POST.get("selling_price")
        product.stock_quantity = request.POST.get("stock_quantity")
        product.save()
        return redirect("product_detail", pk=product.pk)

    return render(request, "products/product_form.html", {"product": product})


@admin_required
def product_delete(request, pk):
    """
    Delete a product. Only accessible by admin users.
    """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("product_list")

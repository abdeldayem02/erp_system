from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SalesOrder, SalesOrderItem
from products.models import Product
from customers.models import Customer
from django.core.paginator import Paginator
from accounts.decorators import admin_required


@login_required
def order_list(request):
    """
    Display a list of all sales orders, ordered by date (newest first).
    """
    orders = SalesOrder.objects.all().order_by('-order_date', '-id')
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    """
    Display details of a specific sales order.
    """
    order = get_object_or_404(SalesOrder, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_create(request):
    """
    Create a new sales order.
    Both admin and sales users can create orders.
    """
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        
        # Create order with created_by set to current user
        order = SalesOrder.objects.create(
            customer_id=customer_id,
            total_amount=0, 
            status='pending',
            created_by=request.user
        )
        messages.success(request, f"Order {order.order_number} created successfully!")
        return redirect("order_detail", pk=order.pk)

    customers = Customer.objects.all()
    return render(request, "orders/order_form.html", {"customers": customers})


@admin_required
def order_edit(request, pk):
    """
    Edit an existing sales order. Only admin can edit.
    """
    order = get_object_or_404(SalesOrder, pk=pk)

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        order.customer_id = customer_id
        order.save()
        messages.success(request, "Order updated successfully!")
        return redirect("order_detail", pk=order.pk)

    customers = Customer.objects.all()
    return render(request, "orders/order_form.html", {"order": order, "customers": customers})


@admin_required
def order_confirm(request, pk):
    """
    Confirm an order. Only admin can confirm.
    This will trigger stock reduction via signals.
    """
    order = get_object_or_404(SalesOrder, pk=pk)
    
    # Validate order has items before confirming
    if not order.items.exists():
        messages.error(request, "Cannot confirm an order with no items. Please add items first.")
        return redirect("order_detail", pk=order.pk)
    
    if order.status == 'pending':
        try:
            order.status = 'confirmed'
            order.save()
            messages.success(request, f"Order {order.order_number} confirmed! Stock has been updated.")
        except ValueError as e:
            messages.error(request, str(e))
    else:
        messages.warning(request, "Only pending orders can be confirmed.")
    
    return redirect("order_detail", pk=order.pk)


@admin_required
def order_cancel(request, pk):
    """
    Cancel an order. Only admin can cancel.
    This will trigger stock restoration via signals if order was confirmed.
    """
    order = get_object_or_404(SalesOrder, pk=pk)
    
    if order.status != 'cancelled':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"Order {order.order_number} cancelled.")
    else:
        messages.warning(request, "Order is already cancelled.")
    
    return redirect("order_detail", pk=order.pk)


@login_required
def order_item_add(request, order_pk):
    """
    Add an item to a sales order.
    """
    order = get_object_or_404(SalesOrder, pk=order_pk)
    
    # Can't modify confirmed or cancelled orders
    if order.status != 'pending':
        messages.error(request, "Cannot modify items of a confirmed or cancelled order.")
        return redirect("order_detail", pk=order.pk)

    if request.method == "POST":
        try:
            product_id = request.POST.get("product_id")
            
            # Validate product_id
            if not product_id:
                messages.error(request, "Please select a product")
                return redirect("order_item_add", order_pk=order.pk)
            
            # Validate and convert quantity
            try:
                quantity = int(request.POST.get("quantity"))
                if quantity <= 0:
                    messages.error(request, "Quantity must be greater than zero")
                    return redirect("order_item_add", order_pk=order.pk)
            except (ValueError, TypeError):
                messages.error(request, "Invalid quantity format")
                return redirect("order_item_add", order_pk=order.pk)
            
            product = get_object_or_404(Product, pk=product_id)
            
            # Check stock availability
            if product.stock_quantity < quantity:
                messages.warning(request, 
                    f"Insufficient stock for {product.name}. Only {product.stock_quantity} units available.")
                return redirect("order_item_add", order_pk=order.pk)
            
            # Create order item
            item = SalesOrderItem.objects.create(
                sales_order=order,
                product=product,
                quantity=quantity,
                unit_price=product.selling_price,
            )
            
            # Recalculate total amount
            order.total_amount = sum(item.total_price for item in order.items.all())
            order.save()
            
            messages.success(request, f"Added {product.name} to order.")
            return redirect("order_detail", pk=order.pk)
            
        except Exception as e:
            messages.error(request, f"Error adding item: {str(e)}")
            return redirect("order_item_add", order_pk=order.pk)

    products = Product.objects.all()
    return render(request, "orders/order_item_form.html", {"order": order, "products": products})


@login_required
def order_item_remove(request, order_pk, item_pk):
    """
    Remove an item from a sales order.
    """
    order = get_object_or_404(SalesOrder, pk=order_pk)
    item = get_object_or_404(SalesOrderItem, pk=item_pk, sales_order=order)
    
    # Can't modify confirmed or cancelled orders
    if order.status != 'pending':
        messages.error(request, "Cannot modify items of a confirmed or cancelled order.")
        return redirect("order_detail", pk=order.pk)
    
    item.delete()
    
    # Recalculate total amount
    order.total_amount = sum(item.total_price for item in order.items.all())
    order.save()
    
    messages.success(request, "Item removed from order.")
    return redirect("order_detail", pk=order.pk)


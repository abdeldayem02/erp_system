from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import SalesOrder
from inventory.models import StockMovement


@receiver(pre_save, sender=SalesOrder)
def handle_order_status_change(sender, instance, **kwargs):
    """
    Handle stock changes when order status changes.
    - Pending -> Confirmed: Reduce stock and log movement
    - Confirmed -> Cancelled: Restore stock and log movement
    """
    if instance.pk:  # Only for existing orders (not new ones)
        try:
            old_order = SalesOrder.objects.get(pk=instance.pk)
            old_status = old_order.status
            new_status = instance.status
            
            # Status changed from pending to confirmed - reduce stock
            if old_status == 'pending' and new_status == 'confirmed':
                # First, validate ALL items have sufficient stock
                for item in instance.items.all():
                    product = item.product
                    if product.stock_quantity < item.quantity:
                        raise ValueError(
                            f"Insufficient stock for {product.name}. "
                            f"Available: {product.stock_quantity}, Required: {item.quantity}"
                        )
                
                # Only if all items passed validation, reduce stock
                for item in instance.items.all():
                    product = item.product
                    
                    # Reduce stock
                    product.stock_quantity -= item.quantity
                    product.save()
                    
                    # Log stock movement
                    StockMovement.objects.create(
                        product=product,
                        quantity=-item.quantity,  # Negative for reduction
                        created_by=instance.created_by,
                    )
            
            # Status changed to cancelled - restore stock if it was confirmed
            elif new_status == 'cancelled' and old_status == 'confirmed':
                for item in instance.items.all():
                    product = item.product
                    
                    # Restore stock
                    product.stock_quantity += item.quantity
                    product.save()
                    
                    # Log stock movement
                    StockMovement.objects.create(
                        product=product,
                        quantity=item.quantity,  # Positive for addition
                        created_by=instance.created_by,
                    )
        except SalesOrder.DoesNotExist:
            pass  # New order, nothing to do

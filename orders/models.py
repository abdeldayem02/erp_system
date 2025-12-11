from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator



class SalesOrder(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # Total amount with validation to ensure non-negative values
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ], default='pending')


    def __str__(self):
        return f"Order {self.order_number} - {self.customer.name}"


    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Orders'
    
    def save(self, *args, **kwargs):
        """
        Auto-generate order number if not provided.
        """
        if not self.order_number:
            today = timezone.now().strftime("%Y%m%d")
            last_order = SalesOrder.objects.filter(order_number__startswith=f'SO-{today}').order_by('order_number').last()

            if last_order:
                last_sequence = int(last_order.order_number.split('-')[-1])
                new_sequence = last_sequence + 1
            else:
                new_sequence = 1

            self.order_number = f'SO-{today}-{new_sequence:04d}'
        super().save(*args, **kwargs)

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # Unit price and total price with validation to ensure non-negative values
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )


    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.sales_order.order_number}"


    class Meta:
        verbose_name = 'Sales Order Item'
        verbose_name_plural = 'Sales Order Items'

    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs) 
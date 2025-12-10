from django.db import models



class SalesOrder(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
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



class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.sales_order.order_number}"


    class Meta:
        verbose_name = 'Sales Order Item'
        verbose_name_plural = 'Sales Order Items'

    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        
        if self.sales_order == 'confirmed':
            self.product.stock_quantity -= self.quantity
            self.product.save()
        elif self.sales_order == 'canceled':
            self.product.stock_quantity += self.quantity
            self.product.save()
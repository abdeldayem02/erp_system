from django.db import models
from django.conf import settings



class StockMovement(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity} by {self.created_by}"


    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
from django.db import models



class StockMovement(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type.capitalize()} - {self.product.name} x {self.quantity}"


    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
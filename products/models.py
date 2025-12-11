from django.db import models
from django.core.validators import MinValueValidator



class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    # Prices with validation to ensure non-negative values
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    selling_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    # Current stock quantity, ensuring it cannot be negative
    stock_quantity = models.PositiveIntegerField(default=0)



    def __str__(self):
        return f"{self.name} ({self.sku})"
    

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        permissions = [
            ("view_product_details", "Can view product details"),
            ("edit_product", "Can edit product information"),
        ]
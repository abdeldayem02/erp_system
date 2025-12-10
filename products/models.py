from django.db import models



class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()



    def __str__(self):
        return f"{self.name} ({self.sku})"
    

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        permissions = [
            ("view_product_details", "Can view product details"),
            ("edit_product", "Can edit product information"),
            ("delete_product", "Can delete product"),
            ("add_product", "Can add new product"),
        ]
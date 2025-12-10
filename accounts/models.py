from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SALES = "SALES", "Sales User"


    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ADMIN,
    )


    def is_admin(self):
        return self.role == self.Roles.ADMIN
    
    def is_sales(self):
        return self.role == self.Roles.SALES
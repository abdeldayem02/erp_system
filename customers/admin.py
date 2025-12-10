from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("customer_id", "name", "phone", "email", "opening_balance")
    search_fields = ("customer_id", "name", "phone", "email")
    
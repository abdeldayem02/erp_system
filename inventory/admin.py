from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "created_by", "quantity", "timestamp",)
    list_filter = ("created_by", "timestamp",)
    search_fields = ("product__name", "product__sku", "created_by__username",)
    readonly_fields = ("product", "quantity", "created_by", "timestamp")
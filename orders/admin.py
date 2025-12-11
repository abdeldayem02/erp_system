from django.contrib import admin
from .models import SalesOrder, SalesOrderItem


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer", "order_date", "status", "total_amount", "created_by")
    list_filter = ("status", "order_date")
    search_fields = ("order_number", "customer__name", "customer__customer_id")
    readonly_fields = ("order_number", "total_amount", "order_date")



@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ("sales_order", "product", "quantity", "unit_price", "total_price")
    search_fields = ("sales_order__order_number", "product__name")
    readonly_fields = ("total_price",)
from django.contrib import admin
from .models import Product, Order, OrderProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'total_cost')
    list_filter = ('start_date', 'end_date')
    search_fields = ('id',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'rental_price', 'rental_duration')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')

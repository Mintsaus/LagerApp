from django.contrib import admin
from .models import Product, Warehouse, Saldo, Sales
# Register your models here.

admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Saldo)
admin.site.register(Sales)

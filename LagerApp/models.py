from __future__ import unicode_literals
from django.db import models


# Create your models here.

#ludwig, demodemo


class Product(models.Model):
    prodnr = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    nr = models.IntegerField()
    name = models.CharField(max_length=128)
    products = models.ManyToManyField(Product, through='Saldo')

    def __str__(self):
        return self.name


class Saldo(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.warehouse.name + self.product.name


class Transactions(models.Model):
    product = models.ForeignKey(Product)
    warehouse = models.ForeignKey(Warehouse)
    date = models.DateField()
    quantity = models.IntegerField(blank=False)
    user = models.CharField(max_length=128)

    def __str__(self):
        return 'product: ' + self.product.name + ' warehouse: ' + self.warehouse.name

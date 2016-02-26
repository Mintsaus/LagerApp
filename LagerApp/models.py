from __future__ import unicode_literals
from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=128)


class Warehouse(models.Model):
    name = models.CharField(max_length=128)
    products = models.ManyToManyField(Product, through='Saldo')


class Saldo(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Sales(models.Model):
    product = models.ForeignKey(Product)
    warehouse = models.ForeignKey(Warehouse)
    date = models.DateTimeField()
    quantity = models.IntegerField
    user = models.CharField(max_length=128)

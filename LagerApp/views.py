from django.shortcuts import render
from .models import Product, Sales, Warehouse
import datetime

# Create your views here.


def startpage(request):
    return render(request, 'LagerApp/index.html')


def products(request):
    prods = Product.objects.all()
    return render(request, 'LagerApp/products.html', {'products': prods})


def add_order(request):
    return render(request, 'LagerApp/add_order.html')


def transaction(request):
    if request.method == 'POST':
        prod = Product.objects.get(name=request.POST[u'product'])
        wh = Warehouse.objects.get(name=request.POST[u'warehouse'])

        date = datetime.date(int(request.POST[u'year']), int(request.POST[u'month']), int(request.POST[u'day']))
        print date
        sale = Sales.objects.create(product=prod, warehouse=wh, date=date)
        sale.save()

        return render(request, 'LagerApp/index.html')

from django.shortcuts import render, redirect
from .models import Product, Sales, Warehouse
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate
#from .forms import AddForm

# Create your views here.


@login_required()
def startpage(request):
    return render(request, 'LagerApp/index.html')


@login_required()
def transactions(request):
    trans = Sales.objects.all()
    paginator = Paginator(trans, 5)
    page = request.GET.get('page')
    print page
    try:
        tosee = paginator.page(page)
    except PageNotAnInteger:
        tosee = paginator.page(1)
    except EmptyPage:
        tosee = paginator.page(paginator.num_pages)
    return render(request, 'LagerApp/transactions.html', {'transactions': tosee})


@login_required()
def add_order(request):
    #form = AddForm()
    if request.method == 'POST':
        #form = AddForm(request.POST)
        print 'posted'
    return render(request, 'LagerApp/add_order.html')#, {'form': form})

@login_required()
def transaction(request):
    if request.method == 'POST':
        prod = Product.objects.get(name=request.POST[u'product'])
        wh = Warehouse.objects.get(name=request.POST[u'warehouse'])
        quant = int(request.POST[u'quantity'])
        if request.POST[u'tofrom'] == "from":
            quant = quant*(-1)
        date = datetime.date(int(request.POST[u'year']), int(request.POST[u'month']), int(request.POST[u'day']))
        sale = Sales.objects.create(product=prod, warehouse=wh, date=date, quantity=quant)
        sale.save()

        return render(request, 'LagerApp/index.html')

@login_required()
def saldo(request):
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    saldon = [products, warehouses]
    saldos =[]

    for p in products:
        for w in warehouses:
            quant_dict = Sales.objects.filter(product=p, warehouse=w).aggregate(Sum('quantity'))
            quant = quant_dict.get('quantity__sum')
            saldos.append({'prod': p.name, 'warehouse': w.name, 'quant': quant})

    return render(request, 'LagerApp/saldo.html', {'saldos': saldos})





























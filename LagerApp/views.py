# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .models import Product, Transactions, Warehouse
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate
from .forms import AddForm

# Create your views here.


@login_required()
def startpage(request):
    return render(request, 'LagerApp/index.html')


@login_required()
def transactions(request):
    page = request.GET.get('page')
    order_by = request.GET.get('order_by', 'id')
    if not page:  #Don't want to flip order on each new page
        old_order = request.session.get('old_order', 'id')
        if order_by == old_order:
            order_by = '-' + old_order
            old_order = 'foobar'
        else:
            old_order = order_by
        request.session['old_order'] = old_order

    print order_by
    trans = Transactions.objects.order_by(order_by)
    paginator = Paginator(trans, 10)
    try:
        tosee = paginator.page(page)
    except PageNotAnInteger:
        tosee = paginator.page(1)
    except EmptyPage:
        tosee = paginator.page(paginator.num_pages)
    return render(request, 'LagerApp/transactions.html', {'transactions': tosee})




@login_required()
def add_order(request):
    if request.method == 'POST':
        date = datetime.strptime(request.POST[u'datepicker'], '%d-%m-%Y')
        prod = Product.objects.get(name=request.POST[u'product'])
        wh = Warehouse.objects.get(name=request.POST[u'warehouse'])
        quant = int(request.POST[u'quantity'])
        if request.POST[u'tofrom'] == 'from':
            quant = quant*(-1)
        sale = Transactions.objects.create(product=prod, warehouse=wh, date=date, quantity=quant)
        sale.save()
        if sale.pk:
            msg = "Your transaction has been received, thank you!"
        else:
            msg = "Something went wrong, please make sure all fields are filled in properly"
        return render(request, 'LagerApp/add_order.html', {'msg': msg})

    return render(request, 'LagerApp/add_order.html', {'msg': ''})


@login_required()
def saldo(request):
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    saldos = []

    for p in products:
        for w in warehouses:
            quant_dict = Transactions.objects.filter(product=p, warehouse=w).aggregate(Sum('quantity'))
            quant = quant_dict.get('quantity__sum')
            saldos.append({'prod': p.name, 'warehouse': w.name, 'quant': quant})

    return render(request, 'LagerApp/saldo.html', {'saldos': saldos})




# def add_form(request):
#     if request.method == 'POST':
#         form = AddForm(request.POST)
#         if form.is_valid():
#             trans = form.save(commit=False)
#             trans.user = request.user
#             trans.save()
#             # date = form.cleaned_date['date']
#             # wh = form.cleaned_date['warehouse']
#             # prod = form.cleaned_date['prod']
#             # quant = form.cleaned_date['quantity']
#             #
#             # trans = Transactions.objects.create(product=prod, warehouse=wh, date=date, quantity=quant)
#             print trans
#         return render(request, 'LagerApp/add_form.html', {'form': form})
#     else:
#         form = AddForm()
#     return render(request, 'LagerApp/add_form.html', {'form': form})
























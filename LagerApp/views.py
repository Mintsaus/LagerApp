# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .models import Product, Transactions, Warehouse
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required()
def transactions(request):
    """ This view shows the table of all transactions made.
    table can be sorted (desc or asc) according to any column """
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
    return render(request, 'LagerApp/transactions.html', {'transactions': tosee, 'order_by': order_by})




@login_required()
def add_order(request):
    """ This view the form where new transactions can be made and
    handles form posts and updates the db"""
    if request.method == 'POST':
        try:
            date = datetime.strptime(request.POST[u'datepicker'], '%d-%m-%Y')
            # dependant on correctly formatted datepicker
        except ValueError:
            msg = "Date input incorrect. "
        try:
            prod = Product.objects.get(name=request.POST[u'product'])
        except Product.DoesNotExist:
            msg = msg + 'Product is incorrect. '
        try:
            wh = Warehouse.objects.get(name=request.POST[u'warehouse'])
        except Warehouse.DoesNotExist:
            msg = msg + 'Warehouse is incorrect. '
        quant = int(request.POST[u'quantity'])
        if quant and request.POST[u'tofrom'] == 'from':
            quant = quant*(-1)
        if date and prod and wh and quant:
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
    """ This view shows the table of current warehouse stock"""
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    saldos = []

    for p in products:
        for w in warehouses:
            quant_dict = Transactions.objects.filter(product=p, warehouse=w).aggregate(Sum('quantity'))
            quant = quant_dict.get('quantity__sum')
            saldos.append({'prod': p.name, 'warehouse': w.name, 'quant': quant})

    return render(request, 'LagerApp/saldo.html', {'saldos': saldos})






















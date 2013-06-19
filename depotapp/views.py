
# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

# app specific files

from models import *
from forms import *


def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    t = get_template('depotapp/create_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def list_product(request):
  
    # Product.objects.all()[:10] = SQL Limit 10
    # Product.objects.all().count()
    list_items = Product.objects.all()
    paginator = Paginator(list_items ,1)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depotapp/list_product.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def view_product(request, id):
    product_instance = Product.objects.get(id = id)

    t=get_template('depotapp/view_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def edit_product(request, id):

    product_instance = Product.objects.get(id=id)

    form = ProductForm(request.POST or None, instance = product_instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/depotapp/product/list/')
    else:
        t=get_template('depotapp/edit_product.html')
        c=RequestContext(request,locals())
        return HttpResponse(t.render(c))


import datetime
def store_view(request):
    date = datetime.datetime.now().date()
    #products = Product.objects.filter(date_available__gt =date).order_by("-date_available")
    products = Product.objects.order_by('-date_available')
    t = get_template('depotapp/store.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_cart(request):
    cart = request.session.get('cart', None)
    t = get_template('depotapp/view_cart.html')

    if not cart:
        cart = Cart()
        request.session['cart'] = cart
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get('cart', None)
    if not cart:
        cart = Cart()
        request.session['cart'] = cart
    cart.add_product(product)
    request.session['cart'] = cart
    return view_cart(request)


def clean_cart(request):
    request.session['cart'] = Cart()
    return view_cart(request)


from django.db import transaction
# reference:
# file:///home/kuroro/learn_space/django/django-docs-1.4-en/topics/db/transactions.html
@transaction.commit_on_success
def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        for item in request.session['cart'].items:
            item.order = order
            item.save()
        clean_cart(request)
        return store_view(request)

    t = get_template('depotapp/create_order.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def list_order(request):
  
    list_items = Order.objects.all()
    paginator = Paginator(list_items ,10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depotapp/list_order.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


def view_order(request, id):
    order_instance = Order.objects.get(id = id)

    t=get_template('depotapp/view_order.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def edit_order(request, id):

    order_instance = Order.objects.get(id=id)

    form = OrderForm(request.POST or None, instance = order_instance)
    if form.is_valid():
        form.save()

    t=get_template('depotapp/edit_order.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

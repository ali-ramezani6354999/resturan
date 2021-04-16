from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cartt import Cartt
from .forms import CarttAddProductForm


@require_POST
def cartt_add(request, product_id):
    cartt = Cartt(request)
    product = get_object_or_404(Product, id=product_id)
    form = CarttAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cartt.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cartt:cartt_detail')


@require_POST
def cartt_remove(request, product_id):
    cartt = Cartt(request)
    product = get_object_or_404(Product, id=product_id)
    cartt.remove(product)
    return redirect('cartt:cartt_detail')


def cartt_detail(request):
    cartt = Cartt(request)
    for item in cartt:
        item['update_quantity_form'] = CarttAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cartt/detail.html', {'cartt': cartt})
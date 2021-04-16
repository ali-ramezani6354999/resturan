from django.shortcuts import render
from .models import Product
from cartt.forms import CarttAddProductForm
from django.shortcuts import render, get_object_or_404
from .models import Category

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context = {
    "products" : products,
    "category": category,
    "categories": categories,
    }
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,'shop/index.html',context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cartt_product_form = CarttAddProductForm()

    return render(request,'shop/product/detail.html',{'product': product,'cartt_product_form': cartt_product_form})



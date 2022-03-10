from django.shortcuts import render
from .models import Category
from shop.models import Product, Series
from .utils import filter_product, sort_product
# Create your views here.


def store(request, slug_category=None, slug_series=None):
    if slug_category is None:
        products = Product.objects.all()
        series = Series.objects.all()
        try:
            keyword = request.GET['q']
            products = filter_product(request, products)
            products = sort_product(request, products)
        except:
            try:
                products = sort_product(request, products)
            except:
                pass
    else:
        series = Series.objects.filter(category__slug__icontains=slug_category)        
        if slug_series is not None:
            products = Product.objects.filter(version__series__slug=slug_series)
        else:
            products = Product.objects.filter(version__category__slug=slug_category)
            try:
                products = filter_product(request, products)
            except:
                try:
                    products = sort_product(request, products)
                except:
                    pass
    categories = Category.objects.all()
    context = { 'products': products,
                'categories': categories,
                'slug_category':slug_category,
                'series':series,
                }
    return render(request, 'shop/store.html', context)
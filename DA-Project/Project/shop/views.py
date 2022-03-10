from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product, Variation, ReviewRating, Version
from django.http import Http404
from django.db.models import Q
from account.models import User
# Create your views here.


def home(request):
    products = Product.objects.filter(capacity__icontains="128")|Product.objects.filter(capacity__icontains="64").order_by("?")
    context = {'products': products}
    return render(request, 'shop/home.html', context)

def detail(request, slug_pro=None):
    try:
        product = Product.objects.get(slug=slug_pro)
        productVers = Product.objects.filter(version=product.version, is_active=True)
        variations = product.variation_set.all()
        productRelateds = Product.objects.filter(version__category__name=product.version.category.name).exclude(slug=slug_pro)
        review_ratings = ReviewRating.objects.filter(version=product.version).order_by('-created_at')
    except:
        return Http404('Error')
    context = {'product':product,
                'variations': variations, 
                'productVers':productVers, 
                'productRelateds': productRelateds,
                'review_ratings': review_ratings,
                }
    return render(request, 'shop/detail.html', context)

def search(request, products=None):
    keyword = request.GET['q']
    if keyword:
        products = Product.objects.filter(Q(version__name__icontains=keyword))
        product_count = products.count()
    else:
        product_count = 0
    context = {'products': products, 'product_count': product_count}
    return render(request, 'shop/store.html', context)

def reviewJson(request):
    data = list(ReviewRating.objects.all().order_by("-created_at").values())
    for i in data:
        version = Version.objects.get(id=i['version_id']).name
        name = User.objects.get(id=i['user_id']).full_name
        i['user_id'] = name
        i['version_id'] = version
    return JsonResponse(data, safe=False)
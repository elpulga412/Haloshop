from django.shortcuts import render
from django.http.response import JsonResponse, json
from shop.models import Product
from .models import Cart, CartItem
from .utils import getCookies
from shop.models import Product, Variation
# Create your views here.

def cart(request):
    if request.user.is_authenticated:
        my_cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
        my_items = my_cart.cartitem_set.all()
        # Get product in cookies
        items, order = getCookies(request)
        print(items)
        if items:
            for item in items:
                product = Product.objects.get(version__name=item['product']['name'], capacity=item['product']['capacity'])
                cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
                cartItem, created = CartItem.objects.get_or_create(product=product, cart=cart, color=item['color'])
                cartItem.quantity = item['quantity']
                cartItem.save()
        context = {'my_cart': my_cart, 'my_items':my_items}   
    else:
        my_items, my_order = getCookies(request)
        context = {'my_items': my_items, 'my_order': my_order}
    return render(request, 'shop/cart.html', context)


def updateCart(request):
    try:
        data = json.loads(request.body)
    except:
        pass
    productId = data['productId']
    productColor = data['productColor']
    action = data['action']
    product = Product.objects.get(id=productId)
    items, order = getCookies(request)
    cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
    cartItem, created = CartItem.objects.get_or_create(product=product, cart=cart, color=productColor)
    variation = Variation.objects.get(product=product, color=productColor)
    if action == 'add':
        if cartItem.quantity < variation.stock:
            cartItem.quantity = cartItem.quantity + 1
        else:
            cartItem.quantity = variation.stock
    elif action == 'remove':
        cartItem.quantity = cartItem.quantity - 1
    cartItem.save()
    if cartItem.quantity <= 0:
        cartItem.delete()
    return JsonResponse('Update success', safe=False)
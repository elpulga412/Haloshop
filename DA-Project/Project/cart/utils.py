from django.http.response import json
from shop.models import Variation

def getCookies(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        order = {'get_total_pay': 0}
        items = []
        for i in cart:
            variation = Variation.objects.get(product__id=cart[i]['productId'], color=cart[i]['productColor'])
            print(variation)
            get_total_per_product = cart[i]['quantity'] * variation.product.price # Tổng Giá mỗi sản phẩm
            order['get_total_pay'] += get_total_per_product #Tổng giá phải trả
            item = {
                'product': {
                    'id': variation.product.id,
                    'name': variation.product.version.name,
                    'capacity': variation.product.capacity,
                    'price': variation.product.price,
                    'image': variation.imageURL,
                },
                'color': variation.color,
                'quantity': cart[i]['quantity'],
                'get_total_per_product': get_total_per_product,             
            }
            items.append(item)
    except:
        items = {}
        order = {}
    return (items, order)
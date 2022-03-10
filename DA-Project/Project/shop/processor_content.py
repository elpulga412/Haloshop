from category.models import Category
from cart.models import Cart, CartItem
from cart.utils import getCookies


def processor_link(request):
    total_items_cart = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user, complete=False)
        total_items_cart = cart.cartitem_set.all().count()
    else:
        items, order = getCookies(request)
        total_items_cart = len(items)
    categories = Category.objects.all()
    content = {'categories': categories, 'total_items_cart': total_items_cart}
    return content
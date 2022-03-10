from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
import datetime
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from shop.models import Variation
from django.contrib import messages
from account.models import User
from account.decorators import allowed_users

# Create your views here.

@login_required(login_url='account:login')
@allowed_users(allowed_roles=["customer", "admin"])
def checkout(request):
    obj = User.objects.get(email=request.user)
    form = OrderForm(instance=obj)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=obj)
        if form.is_valid():       
            order = Order.objects.create(
                full_name = form.cleaned_data['full_name'],
                phone = form.cleaned_data['phone'],
                address = form.cleaned_data['address'],
                state = form.cleaned_data['state'],
                city = form.cleaned_data['city'],
                note = form.cleaned_data['note'],
            )
            order.save()
            order.customer = request.user
            time = datetime.datetime.now() 
            current_date = time.strftime("%Y%m%d")
            order.transaction_id = current_date + str(order.id)
            order.save()
            
            current_transaction = order.transaction_id
            cart = Cart.objects.get(customer=request.user, complete=False)
            cartitem = CartItem.objects.filter(cart=cart, is_active=True)
            order = Order.objects.get(customer=request.user, transaction_id=current_transaction)
            for item in cartitem:
                orderitem = OrderItem.objects.create(
                    customer = request.user,
                    product = item.product,
                    order = order,
                    color = item.color,
                    quantity = item.quantity,
                    price = item.product.price * item.quantity,
                )
                orderitem.save()
                variation = Variation.objects.get(product=item.product, color=item.color)
                variation.stock -= item.quantity
                variation.save()  
            cart.delete()
            messages.success(request, 'Bạn đã đặt hàng thành công')
            return redirect('shop:checkorder')
    context = {'form':form}
    return render(request, 'shop/checkout.html', context)

@login_required(login_url='account:login')
@allowed_users(allowed_roles=["customer", "admin"])
def checkorder(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer=request.user)
        context = {'orders': orders}
    return render(request, 'account/checkorder.html', context)
from django.db import models
from shop.models import Product
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.customer)
    
    def get_total_pay(self):
        cartitems = self.cartitem_set.filter(is_active=True)
        prices = []
        for item in cartitems:
            prices.append(item.get_each_total())
        return sum(prices)
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)

    def get_each_total(self):
        each_product = self.quantity * self.product.price
        return each_product

    
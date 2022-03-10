from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Product, Variation
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    transaction_id = models.CharField(max_length=10, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.transaction_id)
    
    def get_total(self):
        orders = self.orderitem_set.all()
        total = 0
        for order in orders:
            total += int(order.get_amount)
        return total

class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer)
    
    @property
    def get_amount(self):
        return (int(self.quantity) * int(self.price))
    
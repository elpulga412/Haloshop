from django.contrib import admin
from .models import *

# Register your models here.

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'date_added', 'complete')
#     list_editable = ('complete',)


# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('product', 'cart', 'color', 'quantity', 'is_active')
#     list_editable = ('is_active',)

# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem, CartItemAdmin)
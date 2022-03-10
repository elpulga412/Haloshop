from django.contrib import admin
from .models import *
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer', 'full_name', 'phone', 'address', 'state', 'city','updated_at', 'status')
    search_fields = ('status',)
    list_editable = ('status', )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
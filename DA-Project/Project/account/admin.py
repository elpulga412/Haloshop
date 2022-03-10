from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'last_login', 'date_joined', 'is_active', 'is_staff')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    list_filter = ()
    fieldsets = ()
    
admin.site.register(User, AccountAdmin)
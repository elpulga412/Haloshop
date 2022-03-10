from django.contrib import admin
from .models import Product, Variation, Series, Version, ReviewRating
from .forms import VersionAdminForm
# Register your models here.




class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','color', 'stock', 'is_available')
    list_editable = ('is_available',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('version', 'capacity', 'price', 'is_active')
    list_editable = ('is_active',)

class VersionAdmin(admin.ModelAdmin):
    form = VersionAdminForm
    


admin.site.register(Version)
admin.site.register(Series)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
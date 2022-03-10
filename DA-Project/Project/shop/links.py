
from django.urls import reverse


def category_link(instance):
    return reverse('shop:category:store', kwargs={'slug_category': instance.slug})

def series_link(instance):
    return reverse('shop:category:store', kwargs={'slug_category': instance.category.slug, 'slug_series': instance.slug})

def product_link(instance):
    return reverse('shop:detail', kwargs={'slug_pro': instance.slug})
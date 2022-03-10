from django.urls import path, re_path
from . import views

app_name = 'category'
urlpatterns =  [
    re_path(r'^(?:(?P<slug_category>[\w-]+)/)?(?:(?P<slug_series>[\w-]+)/)?$', views.store, name='store'),
]

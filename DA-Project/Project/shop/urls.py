from django.urls import path, include
from . import views
from account import views as viewsAccount

app_name = 'shop'
urlpatterns =  [
    path('', views.home, name='home'),
    path('tim-kiem/', views.search, name='search'),
    path('dien-thoai/', include('category.urls')),
    path('dienthoai/<str:slug_pro>/', views.detail, name='detail'),
    path('gio-hang/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('API-comments/', views.reviewJson, name="comments"),
]       
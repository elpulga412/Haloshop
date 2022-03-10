from django.urls import path
from . import views

app_name="account"

urlpatterns = [
    path('dang-nhap/', views.loginPage, name='login'),
    path('dang-ky/', views.registerPage, name='register'),
    path('dang-xuat/', views.logoutPage, name='logout'),
    path('thong-tin-tai-khoan/', views.update, name='update'),   
]

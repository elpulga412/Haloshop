from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.list_news, name="list_news"),
    path('<str:slug>/', views.detail_news, name="detail_news"),
]

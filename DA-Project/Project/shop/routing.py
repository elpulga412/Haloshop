# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'dienthoai/(?P<slug_pro>[\w-]+)/$', consumers.ReviewConsumer.as_asgi()),
]
from django.urls import re_path

from .consumers import MovieConsumer

websocket_urlpatterns = [
    re_path(r'ws/start/$', MovieConsumer.as_asgi()),
]
from django.urls import path
from app.consumer import MyChaApp


websocket_urlpattrns = [
    path('ws/wsc/',MyChaApp.as_asgi())
]
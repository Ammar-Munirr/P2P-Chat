from django.urls import path

from app.consumer import MyChaApp2

websocket_urlpattrns = [
    path("ws/wsc/<int:id>", MyChaApp2.as_asgi()),
]

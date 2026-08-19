from django.urls import path

from .consumers import TicketConsumer


websocket_urlpatterns = [
    path(
        "ws/tickets/<int:ticket_id>/",
        TicketConsumer.as_asgi(),
    ),
]
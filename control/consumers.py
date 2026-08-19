import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Ticket


class TicketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.ticket_id = self.scope["url_route"]["kwargs"][
            "ticket_id"
        ]

        self.user = self.scope["user"]

        # 1. Authentication
        if not self.user.is_authenticated:
            await self.close(code=4001)
            return

        # 2. Ticket mavjudligini tekshirish
        self.ticket = await self.get_ticket(
            self.ticket_id
        )

        if self.ticket is None:
            await self.close(code=4004)
            return

        # 3. Ticketga kirish huquqini tekshirish
        has_access = await self.user_can_access_ticket()

        if not has_access:
            await self.close(code=4003)
            return

        # 4. Ticket uchun umumiy room
        self.room_group_name = (
            f"ticket_{self.ticket_id}"
        )

        # 5. Roomga ulanish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Noto'g'ri JSON format."
            }))
            return

        message_text = data.get("message")

        if not isinstance(message_text, str):
            await self.send(text_data=json.dumps({
                "error": "message matn bo'lishi kerak."
            }))
            return

        message_text = message_text.strip()

        if not message_text:
            await self.send(text_data=json.dumps({
                "error": "Xabar bo'sh bo'lishi mumkin emas."
            }))
            return

        message = await self.create_message(
            message_text
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "ticket_message",
                "id": message.id,
                "ticket_id": self.ticket_id,
                "sender": self.user.username,
                "message": message.message,
                "created_at": (
                    message.created_at.isoformat()
                ),
            },
        )

    async def ticket_message(self, event):
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "ticket_id": event["ticket_id"],
            "sender": event["sender"],
            "message": event["message"],
            "created_at": event["created_at"],
        }))

    @sync_to_async
    def get_ticket(self, ticket_id):
        try:
            return Ticket.objects.select_related(
                "client",
                "operator",
            ).get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return None

    @sync_to_async
    def user_can_access_ticket(self):
        if self.user.is_staff:
            return True

        if self.ticket.client_id == self.user.id:
            return True

        if self.ticket.operator_id == self.user.id:
            return True

        return False

    @sync_to_async
    def create_message(self, message_text):
        return Message.objects.create(
            ticket=self.ticket,
            sender=self.user,
            message=message_text,
        )
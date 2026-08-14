from django.contrib import admin
from django.contrib.auth.models import User

from control.models import Category, Ticket, Message, TicketHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(TicketHistory)
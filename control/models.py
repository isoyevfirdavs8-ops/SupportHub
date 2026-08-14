
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        OPERATOR = "operator", "Operator"
        ADMIN = "admin", "Admin"

    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField( max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField(max_length=15,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)





class Ticket(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "new","Yangi"
        IN_PROGRESS ="in_progres","Jarayonda"
        RESOLVED ="resolved","Hal qilingan"
        CLOSED = "closed","Yopilgan"
    class PriorityChoices(models.TextChoices):
        LOW = "low","Past"
        MEDIUM = "medium","O'rta"
        HIGH = "high","Baland"
        URGENT = "urgent","Tezkor"

    title = models.CharField(max_length=100)
    description = models.TextField()
    client = models.ForeignKey(User,on_delete=models.CASCADE,related_name='client_tickets')
    operator = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='operator_tickets',)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='category_tasks')
    status = models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.NEW,verbose_name='holati')
    priority = models.CharField(max_length=10,choices=PriorityChoices.choices,default=PriorityChoices.MEDIUM,verbose_name='Muhumlik darajasi')


class Message(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="message")
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    text = models.TextField()
    is_read =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name='ticket_history')
    changed_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="chenged_tickets")
    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)



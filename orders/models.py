from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Order(models.Model):
    class StatusChoice(models.TextChoices):
        DELIVERED= 'delivered'
        SHIPPED= 'shipped'
        PENDING='pending'
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    status= models.CharField(max_length=255, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.user.email} {self.status}'
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import re 

def validate_phone(value):
    pattern = r"^8\(\d{3}\)-\d{3}-\d{2}-\d{2}$"
    if not re.match(pattern, value):
        raise ValidationError("Телефон должен быть в формате 8(XXX)-XXX-XX-XX")

def validate_full_name(value):
    pattern = r"^[A-Za-zА-Яа-яЁё\s]+$"
    if not re.match(pattern, value):
        raise ValidationError("ФИО может содержать только буквы и пробелы")

class User(AbstractUser):
    full_name = models.CharField(max_length=100, validators=[validate_full_name])
    phone = models.CharField(max_length=20, validators=[validate_phone])

    def __str__(self):
        return self.username


class RepairRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.CharField(max_length=100)
    problem = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.car} — {self.user.username} — {self.status}"

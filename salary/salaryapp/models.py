from django.db import models
from django.contrib.auth.models import User


# Эта модель будет использоваться в REST-сервисе для работы с данными сотрудников.
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_grow = models.DateField()


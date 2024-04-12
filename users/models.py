from django.db import models
from django_celery_beat.models import PeriodicTask

from django.contrib.auth.models import AbstractUser

"""Модель пользователя"""

class User(AbstractUser):

    # group_account_id = models.ForeignKey(GroupAccounts, on_delete=models.CASCADE, null=True, default=None)
    active_balance = models.IntegerField(verbose_name="Активный баланс", db_default=0)
    # safe_balance = models.IntegerField(verbose_name="Сбережения", db_default=0)
    periodic_tasks = models.ManyToManyField(PeriodicTask)
    class Meta:
        db_table = 'users'

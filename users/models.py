from django.db import models

from django.contrib.auth.models import AbstractUser
from app.models import GroupAccounts


class User(AbstractUser):
    group_account_id = models.ForeignKey(GroupAccounts, on_delete=models.CASCADE)
    active_balance = models.FloatField(verbose_name="Активный баланс")
    safe_balance = models.FloatField(verbose_name="Сбережения")


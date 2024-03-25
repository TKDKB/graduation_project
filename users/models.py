from django.db import models

from django.contrib.auth.models import AbstractUser


class GroupAccounts(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")


class User(AbstractUser):
    group_account_id = models.ForeignKey(GroupAccounts, on_delete=models.CASCADE)
    active_balance = models.FloatField(verbose_name="Активный баланс")
    safe_balance = models.FloatField(verbose_name="Сбережения")

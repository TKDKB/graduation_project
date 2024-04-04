from django.db import models

from django.contrib.auth.models import AbstractUser


class GroupAccounts(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    class Meta:
        db_table = 'group_accounts'


class User(AbstractUser):
    group_account_id = models.ForeignKey(GroupAccounts, on_delete=models.CASCADE, null=True, default=None)
    active_balance = models.IntegerField(verbose_name="Активный баланс", db_default=0)
    safe_balance = models.IntegerField(verbose_name="Сбережения", db_default=0)
    class Meta:
        db_table = 'users'
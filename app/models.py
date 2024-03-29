import datetime
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

"""
Модели категорий, изменений баланса, групповых аккаунтов и отчётов
"""


class Category(models.Model):
    class Meta:
        db_table = 'categories'

    name = models.CharField(max_length=255, verbose_name="Название")
    is_private = models.BooleanField(verbose_name="Приватность")

    class Type(models.TextChoices):
        income = ('I', 'Income')
        expence = ('E', 'Expence')

    type = models.CharField(max_length=1, choices=Type.choices, verbose_name="Тип изменения баланса")
    user = models.ManyToManyField(get_user_model(), related_name='users')


class BalanceChange(models.Model):
    class Meta:
        db_table = 'balance_changes'

    sum = models.IntegerField(verbose_name="Сумма")
    necessity = models.BooleanField(null=True, blank=True, verbose_name="Необходимость траты")
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    class Type(models.TextChoices):
        income = ('I', 'Income')
        expence = ('E', 'Expence')

    type = models.CharField(max_length=1, choices=Type.choices, verbose_name="Тип изменения баланса")


class RegularBalanceChange(models.Model):
    class Meta:
        db_table = 'regular_balance_changes'

    sum = models.IntegerField(verbose_name="Сумма")
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    regularity = models.DateTimeField(verbose_name="Регулярность")

    class Type(models.TextChoices):
        income = ('I', 'Income')
        expence = ('E', 'Expence')

    type = models.CharField(max_length=1, choices=Type.choices, verbose_name="Тип изменения баланса")



class Reports(models.Model):
    class Meta:
        db_table = 'reports'

    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    context = models.TextField(verbose_name="Содержание")
    time_period_start = models.DateTimeField(verbose_name="Начало промежутка времени")
    time_period_end = models.DateTimeField(verbose_name="Конец промежутка времени")

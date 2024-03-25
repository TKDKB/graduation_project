import datetime
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

"""
Модели категорий, изменений баланса, групповых аккаунтов и отчётов
"""


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")


class BalanceChange(models.Model):
    sum = models.FloatField(verbose_name="Сумма")

    class Type(models.TextChoices):
        breakfast = ('I', 'Income')
        lunch = ('E', 'Expence')

    type = models.CharField(max_length=1, choices=Type.choices, verbose_name="Тип изменения баланса")
    necessity = models.BooleanField(null=True, blank=True, verbose_name="Необходимость траты")
    regularity = models.BooleanField(verbose_name="Регулярность")
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание")


class Reports(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    context = models.TextField(verbose_name="Содержание")
    time_period_start = models.DateTimeField(verbose_name="Начало промежутка времени")
    time_period_end = models.DateTimeField(verbose_name="Конец промежутка времени")

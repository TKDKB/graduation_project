import datetime
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class ExpecesCategories(models.Model):
    name = models.CharField(max_length=255)


class IncomeSources(models.Model):
    name = models.CharField(max_length=255)


class Expences(models.Model):
    sum = models.IntegerField()
    date = models.DateTimeField()
    category_id = models.ForeignKey(ExpecesCategories, on_delete=models.CASCADE)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    necessity = models.CharField(max_length=255)


class Incomes(models.Model):
    sum = models.IntegerField()
    date = models.DateTimeField()
    source_id = models.ForeignKey(IncomeSources, on_delete=models.CASCADE)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    regularity = models.CharField(max_length=255)

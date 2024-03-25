from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.decorators import login_required
from .models import BalanceChange, Category

#
# @login_required
# def home_page_view(request: WSGIRequest):
#     balance_changes = BalanceChange.objects.all().select_related("user_id").prefetch_related("category_id")
#     context: dict = {
#         "balance_changes": balance_changes,
#     }
#     print(balance_changes)
#     return
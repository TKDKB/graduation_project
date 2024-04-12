import json

from django.core.exceptions import ObjectDoesNotExist

from .models import BalanceChange, Category
from .forms import IncomeForm, ExpenceForm, CategoryForm, RegularIncomeForm
import pandas as pd
from datetime import datetime, timedelta
from django.http import FileResponse, HttpResponse
import os
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.core.handlers.wsgi import WSGIRequest



def get_statistics_for_graph(request: WSGIRequest):
    """
    Функция для формирования данных для отображения страницы пользователя, в частности, для графика анализа доходов и расходов
    :param request:
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    balance_changes = BalanceChange.objects.filter(user=request.user, date__range=[start_date, end_date]).select_related("user").prefetch_related(
        "category")
    categories = Category.objects.filter(user=request.user)

    balance_changes_list = list(balance_changes.values())
    categories_list = list(categories.values())


    final_income_statistics_dict = {}
    final_expense_statistics_dict = {}
    current_category_sum = 0

    for category in categories_list:

        for balance_change in balance_changes_list:
            if balance_change["category_id"] == category["id"]:
                print(balance_change["category_id"])
                print(category["id"])
                current_category_sum += balance_change["sum"]
        if category["type"] == "I":
            print(category["type"])
            final_income_statistics_dict[category["name"]] = current_category_sum
        else:
            print(category["type"])
            final_expense_statistics_dict[category["name"]] = current_category_sum

        current_category_sum = 0

    print(final_income_statistics_dict)
    print(final_expense_statistics_dict)

    income_labels_list = list(final_income_statistics_dict.keys())
    income_values_list = list(final_income_statistics_dict.values())
    print(income_values_list)

    expense_labels_list = list(final_expense_statistics_dict.keys())
    expence_values_list = list(final_expense_statistics_dict.values())

    income_non_zero = False
    expense_non_zero = False

    for income in income_values_list:
        if income > 0:
            income_non_zero = True

    for expense in expence_values_list:
        if expense > 0:
            expense_non_zero = True

    income_labels = json.dumps(income_labels_list)
    income_values = json.dumps(income_values_list)
    print(income_values)

    expense_labels = json.dumps(expense_labels_list)
    expense_values = json.dumps(expence_values_list)
    income_non_zero = json.dumps(income_non_zero)
    expense_non_zero = json.dumps(expense_non_zero)
    return income_labels, income_values, expense_labels, expense_values, income_non_zero, expense_non_zero


def create_dataframe_for_excel_export(request: WSGIRequest):
    """
    Функция для формирования файла для экспорта
    :param request:
    """
    data = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    balance_changes = BalanceChange.objects.filter(user=request.user, date__range=[start_date, end_date]).select_related("user").prefetch_related(
        "category")

    data = list(balance_changes.values("sum", "category__name", "date", "description", "type"))
    df = pd.DataFrame(data)
    df['date'] = df['date'].dt.tz_localize(None)
    df.to_excel('data.xlsx', index=False)


def create_regular_income_celery(request: WSGIRequest, name:str, sum: int, recharge_day: int):
    """
    Функция для создания регулярного дохода
    :param request:
    :param name:
    :param sum:
    :param recharge_day:
    """
    try:
        crontab = CrontabSchedule.objects.get(
            day_of_month=recharge_day,
            minute='0',
            hour='0',
            day_of_week=1,
            month_of_year='*'
        )
    except ObjectDoesNotExist:
        crontab = CrontabSchedule.objects.create(
            minute='0',
            hour='0',
            day_of_week=1,
            day_of_month=recharge_day,
            month_of_year='*'
        )

    task_name = f"user_{request.user.id}_income_{sum}_name_{name}"
    task_args = f"[{request.user.id}, {sum}]"

    p_task = PeriodicTask.objects.create(
        name=task_name,
        task="tasks.regular_balance_update",
        args=task_args,
        queue="income",
        crontab=crontab
    )

    request.user.periodic_tasks.add(p_task)

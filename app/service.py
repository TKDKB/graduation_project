import json

from django.core.handlers.wsgi import WSGIRequest
from .models import BalanceChange, Category
# from .forms import IncomeForm, ExpenceForm, CategoryForm, RegularIncomeForm
import pandas as pd
from datetime import datetime, timedelta
from django.http import FileResponse, HttpResponse
import os


def get_statistics_for_graph(request: WSGIRequest):
    balance_changes = BalanceChange.objects.filter(user=request.user).select_related("user").prefetch_related(
        "category")
    categories = Category.objects.filter(user=request.user)

    balance_changes_list = list(balance_changes.values())
    categories_list = list(categories.values())
    # print(balance_changes_list)
    # print(categories_list)

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

    income_labels = json.dumps(income_labels_list)  # Преобразование списка Python в JSON-строку
    income_values = json.dumps(income_values_list)  # Преобразование списка Python в JSON-строку
    print(income_values)

    expense_labels = json.dumps(expense_labels_list)  # Преобразование списка Python в JSON-строку
    expense_values = json.dumps(expence_values_list)  # Преобразование списка Python в JSON-строку
    return income_labels, income_values, expense_labels, expense_values


def create_dataframe_for_excel_export(request: WSGIRequest):
    data = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    balance_changes = BalanceChange.objects.filter(user=request.user, date__range=[start_date, end_date]).select_related("user").prefetch_related(
        "category")

    data = list(balance_changes.values("sum", "necessity", "category__name", "date", "description", "type"))
    df = pd.DataFrame(data)
    df['date'] = df['date'].dt.tz_localize(None)
    df.to_excel('data.xlsx', index=False)


# def download_and_delete_file(request: WSGIRequest):
#     create_dataframe_for_excel_export(request)
#     file_path = 'data.xlsx'
#     file_name = os.path.basename(file_path)
#
#     try:
#         with open(file_path, 'rb') as file:
#             response = HttpResponse(file, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename=' + file_name
#
#             # Удаляем файл после отправки
#             os.remove(file_path)
#
#             return response
#     except FileNotFoundError:
#         return HttpResponse("Файл не найден", status=404)

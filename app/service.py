import json

from django.core.handlers.wsgi import WSGIRequest
from .models import BalanceChange, Category
from .forms import IncomeForm, ExpenceForm, CategoryForm, RegularIncomeForm

def get_statistics_for_graph(request: WSGIRequest):
    balance_changes = BalanceChange.objects.filter(user=request.user).select_related("user").prefetch_related(
        "category")
    categories = Category.objects.filter(user=request.user)

    balance_changes_list = list(balance_changes.values())
    categories_list = list(categories.values())
    print(categories_list)

    final_income_statistics_dict = {}
    final_expense_statistics_dict = {}
    current_category_sum = 0

    for category in categories_list:

        for balance_change in balance_changes_list:
            if balance_change["category_id"] == category["id"]:
                current_category_sum += balance_change["sum"]
        if category["type"] == "I":
            # print(category["type"])
            final_income_statistics_dict[category["name"]] = current_category_sum
        else:
            # print(category["type"])
            final_expense_statistics_dict[category["name"]] = current_category_sum

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


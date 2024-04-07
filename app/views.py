from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import QuerySet, Q
from django.contrib.auth.decorators import login_required
from .models import BalanceChange, Category
from .forms import IncomeForm, ExpenceForm, CategoryForm, RegularIncomeForm
from .service import get_statistics_for_graph, create_dataframe_for_excel_export
from django.http import FileResponse, HttpResponse
import os


@login_required
def home_page_view(request: WSGIRequest):
    balance_changes = BalanceChange.objects.filter(user=request.user.id).select_related("user").prefetch_related("category")
    categories = Category.objects.filter(user=request.user)
    context: dict = {
        "balance_changes": balance_changes,
        "categories": categories,
    }
    print(balance_changes)
    return render(request, "home.html", context)


@login_required
def create_income(request: WSGIRequest):
    if request.method == 'POST':
        form = IncomeForm(request.user, request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.type = "I"
            income.user = request.user
            income.save()
            request.user.active_balance += income.sum
            request.user.save()
            # return render(request, 'create-income-form.html', {'form': form})  # Перенаправление на страницу об успешном создании объекта
            return HttpResponseRedirect(reverse('home-page'))

    else:
        form = IncomeForm(request.user)

    return render(request, 'create-income-form.html', {'form': form})


@login_required
def create_expence(request: WSGIRequest):
    if request.method == 'POST':
        form = ExpenceForm(request.user, request.POST)
        if form.is_valid():
            expence = form.save(commit=False)
            expence.type = "E"
            expence.user = request.user
            expence.save()
            request.user.active_balance -= expence.sum
            request.user.save()
            return HttpResponseRedirect(reverse('home-page'))
            # return render(request, 'create-expense-form.html', {'form': form})  # Перенаправление на страницу об успешном создании объекта
    else:
        form = ExpenceForm(request.user)

    return render(request, 'create-expense-form.html', {'form': form})


# @login_required
# def create_category(request: WSGIRequest):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.is_private = True
#             category.save()
#             category.user.set([request.user])
#             return render(request, 'temporary_message.html')
#     else:
#         form = CategoryForm()
#
#     return render(request, 'create_category_form.html', {'form': form})


@login_required
def create_category(request: WSGIRequest):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            user = request.user

            existing_category = Category.objects.filter(name=category_name).first()

            if existing_category:
                existing_category.user.add(user)
            else:
                new_category = form.save(commit=False)
                new_category.is_private = True
                new_category.save()
                new_category.user.add(user)

            return HttpResponseRedirect(reverse('home-page'))

    else:
        form = CategoryForm()

    return render(request, 'create-category-form.html', {'form': form})


# TODO: тут есть вопросы по реализации
@login_required
def create_regular_income(request: WSGIRequest):
    if request.method == 'POST':
        form = RegularIncomeForm(request.POST)
        if form.is_valid():
            r_income = form.save(commit=False)
            r_income.type = "E"
            r_income.user = request.user
            r_income.save()
            return render(request, 'temporary_message.html')
    else:
        form = RegularIncomeForm()

    return render(request, 'create_income_form.html', {'form': form})


@login_required
def filter_balance_changes(request):
    selected_type = request.GET.get('type')
    selected_category = request.GET.get('category')

    balance_changes = BalanceChange.objects.filter(user=request.user.id).select_related("user").prefetch_related("category")
    categories = Category.objects.filter(user=request.user)

    if selected_type:
        balance_changes = balance_changes.filter(type=selected_type)

    if selected_category:
        balance_changes = balance_changes.filter(category=selected_category)

    return render(request, 'home.html',
                  {'balance_changes': balance_changes, 'selected_type': selected_type,
                   'selected_category': selected_category, "categories": categories})


@login_required
def test(request: WSGIRequest):
    create_dataframe_for_excel_export(request)
    return render(request, template_name='test.html')

@login_required
def export(request: WSGIRequest):
    create_dataframe_for_excel_export(request)
    file_path = 'data.xlsx'
    file_name = os.path.basename(file_path)

    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=' + file_name

            # Удаляем файл после отправки
            os.remove(file_path)

            return response
    except FileNotFoundError:
        return HttpResponse("Файл не найден", status=404)
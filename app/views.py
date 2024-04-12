from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import QuerySet, Q
from django.contrib.auth.decorators import login_required
from .models import BalanceChange, Category
from django_celery_beat.models import PeriodicTask
from .forms import IncomeForm, ExpenceForm, CategoryForm, RegularIncomeForm
from .service import get_statistics_for_graph, create_dataframe_for_excel_export, create_regular_income_celery
from django.http import FileResponse, HttpResponse
import os



def greeting(request:WSGIRequest):
    """
    Функция отображения приветственной обложки
    :param request:
    """
    return render(request, 'greeting.html')

@login_required
def home_page_view(request: WSGIRequest):
    """
    Функция отображения домашней страницы
    :param request:
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    balance_changes = BalanceChange.objects.filter(user=request.user.id, date__range=[start_date, end_date]).select_related("user").prefetch_related("category")
    categories = Category.objects.filter(user=request.user)
    for balance_change in balance_changes:
        balance_change.sum = balance_change.sum / 100
    context: dict = {
        "balance_changes": balance_changes,
        "categories": categories,
    }
    print(balance_changes)
    return render(request, "home.html", context)


@login_required
def create_income(request: WSGIRequest):
    """
    Функция создания дохода
    :param request:
    """
    if request.method == 'POST':
        form = IncomeForm(request.user, request.POST)
        if form.is_valid():
            sum = int(form.cleaned_data['sum'] * 100)
            income = form.save(commit=False)
            income.type = "I"
            income.user = request.user
            income.sum = sum
            income.save()
            request.user.active_balance += income.sum
            request.user.save()
            return HttpResponseRedirect(reverse('home-page'))

    else:
        form = IncomeForm(request.user)

    return render(request, 'create-income-form.html', {'form': form})


@login_required
def create_expence(request: WSGIRequest):
    """
    Функция создания расхода
    :param request:
    """
    if request.method == 'POST':
        form = ExpenceForm(request.user, request.POST)
        if form.is_valid():
            sum = int(form.cleaned_data['sum'] * 100)
            expence = form.save(commit=False)
            expence.type = "E"
            expence.user = request.user
            expence.sum = sum
            expence.save()
            request.user.active_balance -= expence.sum
            request.user.save()
            return HttpResponseRedirect(reverse('home-page'))
    else:
        form = ExpenceForm(request.user)

    return render(request, 'create-expense-form.html', {'form': form})


@login_required
def delete_category(request: WSGIRequest, id: int):
    """
    Функция удаления категории
    :param request:
    :param id:
    """
    category = get_object_or_404(Category, id=id)
    user = request.user

    if category.user.count() > 1:
        user.categories.remove(category)
        return HttpResponseRedirect(reverse('profile'))
    else:
        category.delete()
        return HttpResponseRedirect(reverse('profile'))

@login_required
def delete_balance_change(request: WSGIRequest, id: int):
    """
    Функция удаления изменения баланса
    :param request:
    :param id:
    """
    balance_change = get_object_or_404(BalanceChange, id=id)
    user = request.user

    if balance_change.type == 'I':
        user.active_balance -= balance_change.sum
    elif balance_change.type == 'E':
        user.active_balance += balance_change.sum

    user.save()

    balance_change.delete()
    return HttpResponseRedirect(reverse('home-page'))

@login_required
def create_category(request: WSGIRequest):
    """
    Функция создания категории
    :param request:
    """
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

@login_required
def filter_balance_changes(request):
    """
    Функция фильтрации изменений баланса
    :param request:
    """
    selected_type = request.GET.get('type')
    selected_category = request.GET.get('category')

    balance_changes = BalanceChange.objects.filter(user=request.user.id).select_related("user").prefetch_related("category")
    categories = Category.objects.filter(user=request.user)

    if selected_type:
        balance_changes = balance_changes.filter(type=selected_type)

    if selected_category:
        balance_changes = balance_changes.filter(category=selected_category)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        balance_changes = balance_changes.filter(date__range=[start_date, end_date])

    return render(request, 'home.html', {'balance_changes': balance_changes,
                                         'selected_type': selected_type,
                                         'selected_category': selected_category,
                                         'categories': categories,
                                         'start_date': start_date,
                                         'end_date': end_date})


@login_required
def test(request: WSGIRequest):
    create_dataframe_for_excel_export(request)
    return render(request, template_name='test.html')

@login_required
def export(request: WSGIRequest):
    """
    Функция экспорта в excel
    :param request:
    """
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



@login_required
def create_regular_income(request: WSGIRequest):
    """
    Функция создания регулярного дохода
    :param request:
    """
    if request.method == 'POST':
        form = RegularIncomeForm(request.user, request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sum = form.cleaned_data['replenishment_amount'] * 100
            recharge_day = form.cleaned_data['recharge_day']
            create_regular_income_celery(request, name, sum, recharge_day)
            return HttpResponseRedirect(reverse('home-page'))
    else:
        form = RegularIncomeForm(request.user)

    return render(request, 'create-regular-income-form.html', {'form': form})

@login_required
def delete_regular_income(request: WSGIRequest, id: int):
    """
    Функция удаления регулярного дохода
    :param request:
    :param id:
    """
    PeriodicTask.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('profile'))


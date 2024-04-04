from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import QuerySet, Q
from django.contrib.auth.decorators import login_required
from .models import BalanceChange, Category
from .forms import IncomeForm, ExpenceForm, CategoryForm, RegularIncomeForm
from .service import get_statistics_for_graph


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
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.type = "I"
            income.user = request.user  # Назначение пользователя из запроса
            income.save()
            # Дополнительные действия после успешного создания объекта
            return render(request, 'temporary_message.html')  # Перенаправление на страницу об успешном создании объекта
    else:
        form = IncomeForm()

    return render(request, 'create_income_form.html', {'form': form})


@login_required
def create_expence(request: WSGIRequest):
    if request.method == 'POST':
        form = ExpenceForm(request.POST)
        if form.is_valid():
            expence = form.save(commit=False)
            expence.type = "E"
            expence.user = request.user  # Назначение пользователя из запроса
            expence.save()
            # Дополнительные действия после успешного создания объекта
            return render(request, 'temporary_message.html')  # Перенаправление на страницу об успешном создании объекта
    else:
        form = ExpenceForm()

    return render(request, 'create_income_form.html', {'form': form})


@login_required
def create_category(request: WSGIRequest):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.is_private = True
            category.save()
            category.user.set([request.user])
            return render(request, 'temporary_message.html')
    else:
        form = CategoryForm()

    return render(request, 'create_category_form.html', {'form': form})


# TODO: тут есть вопросы по реализации
@login_required
def create_regular_income(request: WSGIRequest):
    if request.method == 'POST':
        form = RegularIncomeForm(request.POST)
        if form.is_valid():
            r_income = form.save(commit=False)
            r_income.type = "E"
            r_income.user = request.user  # Назначение пользователя из запроса
            r_income.save()
            # Дополнительные действия после успешного создания объекта
            return render(request, 'temporary_message.html')  # Перенаправление на страницу об успешном создании объекта
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
    get_statistics_for_graph(request)
    return render(request, template_name='test.html')

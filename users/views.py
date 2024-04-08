import json

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest
from .models import User
from app.models import Category
from django_celery_beat.models import PeriodicTask
from .forms import RegisterForm, PasswordResetForm, ActiveBalanceForm
from django.contrib.auth.decorators import login_required
from .email_senders import PasswordResetEmailSender, RegistrationConfirmEmailSender
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from app.service import get_statistics_for_graph


""" Регистрация """

def register_view(request: WSGIRequest):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                active_balance=form.cleaned_data['active_balance'],
                # safe_balance=form.cleaned_data['safe_balance'],
                is_active=False,
            )
            RegistrationConfirmEmailSender(request, user).send_mail()  # отправка письма для подтверждения
            return render(request, "registration/message.html")

    return render(request, 'registration/register.html', {'form': form})


""" Открыть профиль пользователя """

@login_required
def show_user(request: WSGIRequest):
    user = get_object_or_404(User, username=request.user.username)
    categories = Category.objects.filter(user=user)
    regular_incomes = PeriodicTask.objects.filter(user=user)
    print("FFF", regular_incomes)
    for reg_inc in regular_incomes:
        reg_inc.name = reg_inc.name.split('name_')[1]
        task_args_list = reg_inc.args.strip('[]').split(',')
        task_args_list = [int(arg.strip()) for arg in task_args_list]
        reg_inc.args = task_args_list[1] / 100
    labels_values = get_statistics_for_graph(request)
    return render(request, 'registration/show-user.html',
                  {
                      "user": user,
                      "categories": categories,
                      "regular_incomes": regular_incomes,
                      "income_labels": labels_values[0],
                      "income_values": labels_values[1],
                      "expense_labels": labels_values[2],
                      "expense_values": labels_values[3],
                      "income_non_zero": labels_values[4],
                      "expense_non_zero": labels_values[5]
                  }
            )


""" Изменить пользователя """

# @login_required
# def edit_user(request: WSGIRequest):
#     user = get_object_or_404(User, username=request.user.username)
#     # if request.user != user:
#     #     return HttpResponseForbidden("У вас нет доступа к аккаунту этого пользователя!")
#     if request.method == 'GET':
#         form = UserProfileForm()
#         context = {
#             "form": form,
#             "user": request.user,
#         }
#
#         return render(request, "user_profile.html", context)
#
#     elif request.method == "POST":
#
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#
#             if form.cleaned_data['first_name']:
#                 request.user.first_name = form.cleaned_data['first_name']
#
#             if form.cleaned_data['last_name']:
#                 request.user.last_name = form.cleaned_data['last_name']
#
#             request.user.save()
#
#             return HttpResponseRedirect(reverse('show-profile', args=[request.user.username]))
#
#         return render(request, 'user_profile.html', {'form': form})


""" Отправить письмо для смены пароля """

@login_required
def send_email_password_change(request: WSGIRequest):
    PasswordResetEmailSender(request, request.user).send_mail()

    return render(request, "registration/message.html")


""" Обработчик перехода по ссылке из письма для смены пароля """
def change_password_receiver(request: WSGIRequest, token: str, uidb: str):
    user_id = force_str(urlsafe_base64_decode(uidb))
    user = get_object_or_404(User, id=user_id)
    if default_token_generator.check_token(user, token):
        form = PasswordResetForm()
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data["password1"])
                user.save(update_fields=["password"])
                update_session_auth_hash(request, request.user)
                return HttpResponseRedirect(reverse("login"))
        return render(request, 'registration/password-reset-form.html', {'form': form})

    return render(request, "registration/invalid-password-reset.html")


""" Обработчик перехода по ссылке из письма для подтверждения регистрации """
def confirm_registration_receiver(request: WSGIRequest, token: str, uidb: str):
    user_id = force_str(urlsafe_base64_decode(uidb))
    user = get_object_or_404(User, id=user_id)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        return HttpResponseRedirect(reverse("login"))

    return render(request, "registration/invalid-password-reset.html")


@login_required
def alter_active_balance(request: WSGIRequest):
    if request.method == 'POST':
        form = ActiveBalanceForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            request.user.active_balance = amount
            request.user.save()

            return HttpResponseRedirect(reverse('profile'))

    else:
        form = ActiveBalanceForm()

    return render(request, 'alter_active_balance.html', {'form': form})

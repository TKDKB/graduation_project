from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import register_view, show_user, send_email_password_change, change_password_receiver, confirm_registration_receiver, alter_active_balance

"""Роутер для приложения пользователя"""
urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", show_user, name="profile"),
    # path("edit-profile/", edit_user, name="edit-profile"),
    path("change-password-send/", send_email_password_change, name="change-password-sender"),
    path("change-password-proceed/<uidb>/<token>", change_password_receiver, name="change-password-proceed"),
    path("confirm-registration-proceed/<uidb>/<token>", confirm_registration_receiver, name="confirm-registration-proceed"),
    path("alter-active-balance", alter_active_balance, name="alter-active-balance"),
]

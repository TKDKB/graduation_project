"""
URL configuration for graduation_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import home_page_view, create_income, create_expence, create_category, create_regular_income, filter_balance_changes, test, export, delete_balance_change, delete_category, delete_regular_income


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("users.urls")),
    path('api/balance_changes/', include("app.api.urls")),
    path('home/', home_page_view, name="home-page"),
    path('create-income/', create_income, name="create-income"),
    path('create-expence/', create_expence, name="create-expence"),
    path('create-category/', create_category, name="create-category"),
    path('create-regular-income/', create_regular_income, name="create-regular-income"),
    path('filter-balance-changes/', filter_balance_changes, name="filter-balance-changes"),
    path('delete-balance-change/<id>', delete_balance_change, name="delete-balance-change"),
    path('delete-category/<id>', delete_category, name="delete-category"),
    path('delete-regular-income/<id>', delete_regular_income, name="delete-regular-income"),
    path('test/', test, name="test"),
    path('export/', export, name="export")
]

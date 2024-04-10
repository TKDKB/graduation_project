from django.urls import path

from app.api.views import BalanceChangeListAPIView, IncomeListCreateAPIView, ExpenseListCreateAPIView

"""Router for API"""

app_name = "api"

urlpatterns = [
    path('', BalanceChangeListAPIView.as_view(), name="balance-changes"),
    path('create/income/', IncomeListCreateAPIView.as_view(), name="create-income"),
    path('create/expense/', ExpenseListCreateAPIView.as_view(), name="create-expense"),
]
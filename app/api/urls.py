from django.urls import path

from app.api.views import BalanceChangeListAPIView, IncomeListCreateAPIView, ExpenseListCreateAPIView, CategoryListCreateAPIView, PeriodicTaskListCreateAPIView, BalanceChangeDeleteAPIView, RegularIncomeDeleteAPIView, CategoryDeleteAPIView

"""Router for API"""

app_name = "api"

urlpatterns = [
    path('', BalanceChangeListAPIView.as_view(), name="balance-changes"),
    path('income/', IncomeListCreateAPIView.as_view(), name="income"),
    path('expense/', ExpenseListCreateAPIView.as_view(), name="expense"),
    path('category/', CategoryListCreateAPIView.as_view(), name="category"),
    path('regular-income/', PeriodicTaskListCreateAPIView.as_view(), name="regular-income"),
    path('<int:pk>', BalanceChangeDeleteAPIView.as_view(), name="delete-balance-change"),
    path('regular-income/<int:pk>', RegularIncomeDeleteAPIView.as_view(), name="delete-regular-income"),
    path('category/<int:pk>', CategoryDeleteAPIView.as_view(), name="delete-category"),

]

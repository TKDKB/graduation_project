from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from app.models import BalanceChange, Category
from .serializers import BalanceChangesSerializer, IncomeCreateSerializer, ExpenseCreateSerializer


class BalanceChangeListAPIView(generics.ListAPIView):
    # queryset = BalanceChange.objects.all()

    def get_queryset(self):
        return BalanceChange.objects.filter(user=self.request.user)

    serializer_class = BalanceChangesSerializer
    permission_classes = [IsAuthenticated]



class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    # queryset = BalanceChange.objects.filter(type='E')  # Фильтруем только расходы
    def get_queryset(self):
        return BalanceChange.objects.filter(type='E', user=self.request.user)

    serializer_class = ExpenseCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeListCreateAPIView(generics.ListCreateAPIView):
    # queryset = BalanceChange.objects.filter(type='I')  # Фильтруем только доходы

    def get_queryset(self):
        return BalanceChange.objects.filter(type='I', user=self.request.user)
    serializer_class = IncomeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


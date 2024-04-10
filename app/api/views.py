from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from app.models import BalanceChange, Category
from .serializers import BalanceChangesSerializer, IncomeCreateSerializer, ExpenseCreateSerializer


class BalanceChangeListAPIView(generics.ListAPIView):
    queryset = BalanceChange.objects.all()
    serializer_class = BalanceChangesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = BalanceChange.objects.filter(type='E')  # Фильтруем только расходы
    serializer_class = ExpenseCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeListCreateAPIView(generics.ListCreateAPIView):
    queryset = BalanceChange.objects.filter(type='I')  # Фильтруем только доходы
    serializer_class = IncomeCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from django_celery_beat.models import PeriodicTask
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service import create_regular_income_celery

from app.models import BalanceChange, Category
from .serializers import BalanceChangesSerializer, IncomeSerializer, ExpenseSerializer, CategorySerializer, PeriodicTaskSerializer


class BalanceChangeListAPIView(generics.ListAPIView):

    def get_queryset(self):
        # return BalanceChange.objects.filter(user=self.request.user)
        queryset = BalanceChange.objects.filter(user=self.request.user)

        change_type = self.request.query_params.get('change_type')
        category_id = self.request.query_params.get('category_id')

        if change_type:
            queryset = queryset.filter(type=change_type)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    filter_backends = [OrderingFilter]
    serializer_class = BalanceChangesSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ["date"]
    pagination_class = PageNumberPagination



class BalanceChangeDeleteAPIView(generics.DestroyAPIView):
    queryset = BalanceChange.objects.all()
    serializer_class = BalanceChangesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'



class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    # queryset = BalanceChange.objects.filter(type='E')  # Фильтруем только расходы
    def get_queryset(self):
        return BalanceChange.objects.filter(type='E', user=self.request.user)

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeListCreateAPIView(generics.ListCreateAPIView):
    # queryset = BalanceChange.objects.filter(type='I')  # Фильтруем только доходы

    def get_queryset(self):
        return BalanceChange.objects.filter(type='I', user=self.request.user)
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('name')
        category_type = request.data.get('type')
        user = request.user

        existing_category = Category.objects.filter(name=category_name, user=user).first()

        if existing_category:
            return Response(CategorySerializer(existing_category).data, status=status.HTTP_200_OK)
        else:
            existing_category_other_users = Category.objects.filter(name=category_name).exclude(user=user).first()

            if existing_category_other_users:
                existing_category_other_users.user.add(user)
                return Response(CategorySerializer(existing_category_other_users).data, status=status.HTTP_200_OK)
            else:
                new_category = Category.objects.create(name=category_name, is_private=True, type=category_type)
                new_category.user.add(user)
                return Response(CategorySerializer(new_category).data, status=status.HTTP_201_CREATED)


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        instance.user.remove(user)
        if not instance.user.exists():
            self.perform_destroy(instance)
            return Response({"message": "Category and its associations deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Category association with user deleted successfully"}, status=status.HTTP_200_OK)


class PeriodicTaskListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        return PeriodicTask.objects.filter(user=self.request.user)

    serializer_class = PeriodicTaskSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        name = request.data.get('name', None)
        sum = request.data.get('amount', None)
        # recharge_day = request.data.get('crontab.day_of_month', None)
        recharge_day = request.data.get('day_of_month', None)
        print(name, sum, recharge_day)

        create_regular_income_celery(request, name, sum, recharge_day)

        return Response(status=status.HTTP_201_CREATED)


class RegularIncomeDeleteAPIView(generics.DestroyAPIView):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

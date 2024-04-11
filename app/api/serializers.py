from django_celery_beat.models import PeriodicTask, CrontabSchedule
from rest_framework import serializers
from app.models import BalanceChange, Category


class BalanceChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceChange
        fields = ['id', 'sum', 'category', 'user', 'date', 'description', 'type']


class IncomeSerializer(serializers.ModelSerializer):
    sum = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = BalanceChange
        fields = ['id', 'sum', 'category', 'user', 'date', 'description', 'type']
        read_only_fields = ['id', 'user', 'date', 'type']

    def create(self, validated_data):
        validated_data['type'] = "I"

        validated_data['sum'] = int(validated_data['sum'] * 100)
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(type='I')


class ExpenseSerializer(serializers.ModelSerializer):
    sum = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = BalanceChange
        fields = ['id', 'sum', 'category', 'user', 'date', 'description', 'type']
        read_only_fields = ['id', 'user', 'date', 'type']

    def create(self, validated_data):
        validated_data['type'] = "E"
        validated_data['sum'] = int(validated_data['sum'] * 100)
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(type='E')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_private', 'type', 'user']
        read_only_fields = ['id', 'user', 'is_private']


class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = ['day_of_month']  # Используйте кортеж для указания поля


class PeriodicTaskSerializer(serializers.ModelSerializer):
    crontab = CrontabScheduleSerializer(read_only=True)
    amount = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)
    day_of_month = serializers.IntegerField(min_value=1, max_value=31, write_only=True)

    class Meta:
        model = PeriodicTask
        fields = ['name', 'args', 'crontab', 'amount', 'day_of_month']
        read_only_fields = ['args', 'crontab']

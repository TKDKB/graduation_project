from rest_framework import serializers
from app.models import BalanceChange, Category


class BalanceChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceChange
        fields = ['id', 'sum', 'category', 'user', 'date', 'description', 'type']


class IncomeCreateSerializer(serializers.ModelSerializer):
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


class ExpenseCreateSerializer(serializers.ModelSerializer):
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

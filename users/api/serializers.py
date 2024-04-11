from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'active_balance', 'periodic_tasks', 'email', 'password']
        read_only_fields = ['id', 'username', 'periodic_tasks', 'email', 'password']
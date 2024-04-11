from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from ..email_senders import PasswordResetEmailSender, RegistrationConfirmEmailSender



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'active_balance', 'periodic_tasks', 'email', 'password']
        read_only_fields = ['id', 'username', 'periodic_tasks', 'email', 'password']


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )


    username = serializers.CharField(
        style={'input_type': 'username'}, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'password',
        )

    def validate_email(self, value):
        email = value.lower()
        if get_user_model().objects.filter(email=email).exists():
            raise ParseError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )
        return email
    def validate_username(self, value):
        username = value
        if get_user_model().objects.filter(username=username).exists():
            raise ParseError(
                'Пользователь с таким именем уже зарегистрирован.'
            )
        return username

    def validate_password(self, value):
        validate_password(value)
        return value


class UserPasswordResetSerializer(serializers.Serializer):
    # password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = get_user_model()

        class Meta:
            model = get_user_model()
            fields = ['id', 'username', 'active_balance', 'periodic_tasks', 'email', 'password']
            read_only_fields = ['id', 'username', 'active_balance', 'periodic_tasks', 'email', 'password']


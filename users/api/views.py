from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework.views import APIView

from .serializers import UserSerializer, UserRegistrationSerializer, UserPasswordResetSerializer
from ..email_senders import RegistrationConfirmEmailSender, PasswordResetEmailSender


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        new_active_balance = request.data.get('active_balance')

        if new_active_balance is not None:
            user.active_balance = new_active_balance
            user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data)


# class UserRegistrationAPIView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        user = get_user_model().objects.create_user(
            **validated_data,
            is_active=False,
        )
        RegistrationConfirmEmailSender(self.request, user).send_mail()
        return user



class UserPasswordUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPasswordResetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        PasswordResetEmailSender(request, request.user).send_mail()
        return Response({"message": "Message sent"}, status=status.HTTP_200_OK)

from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer


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

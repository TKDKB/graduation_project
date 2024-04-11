from django.urls import path
from users.api.views import UserDetailView, UserRegistrationAPIView, UserPasswordUpdateView

urlpatterns = [
    path('profile/', UserDetailView.as_view(), name="profile-info"),
    path('', UserRegistrationAPIView.as_view(), name="registration"),
    path('profile/password-update', UserPasswordUpdateView.as_view(), name="update-password"),
]
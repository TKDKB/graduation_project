from django.urls import path
from users.api.views import UserDetailView

urlpatterns = [
    path('profile/', UserDetailView.as_view(), name="profile"),
]